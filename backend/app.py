from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from data_loader import load_movie_data
from recommender import MovieRecommender
from emotion_classifier import EmotionClassifier

app = Flask(__name__)
CORS(app)

# ---------- Load Data & Models ----------
EMOTION_CSV = "data/emotion_dataset.csv"

movies_df = load_movie_data()
recommender = MovieRecommender(movies_df)
classifier = EmotionClassifier(EMOTION_CSV)

# Map moods → genres
mood_to_genres = {
    "happy": ["Comedy", "Romance"],
    "curious": ["Mystery", "Adventure"],
    "neutral": ["Drama", "Documentary"],
    "excited": ["Action", "Adventure"],
    "angry": ["Action", "Crime"],
    "fear": ["Thriller", "Horror"],
    "surprise": ["Adventure", "Fantasy"]
}

# Emoji mapping
mood_emojis = {
    "happy": "😄",
    "joy": "😊",
    "sad": "😢",
    "angry": "😡",
    "fear": "😨",
    "surprise": "😲",
    "neutral": "😐",
    "curious": "🤔",
    "excited": "😍"
}

def shorten_text(text, word_limit=10):
    words = str(text).split()
    if len(words) <= word_limit:
        return text
    return " ".join(words[:word_limit]) + "..."

# ---------- Helper ----------
def shape_movie_payload(rows):
    movies = []

    if rows is None or len(rows) == 0:
        return movies

    # Case 1: Pandas DataFrame
    if hasattr(rows, "iterrows"):
        for _, row in rows.iterrows():
            movies.append({
                "title": row["title"] if "title" in row and pd.notna(row["title"]) else "N/A",
                "poster_url": row["poster_url"] if "poster_url" in row and pd.notna(row["poster_url"]) else "https://via.placeholder.com/240x360.png?text=No+Poster",
                "overview": shorten_text(row["overview"]) if "overview" in row and pd.notna(row["overview"]) else "No description available",
                "release_date": (
                    pd.to_datetime(row.get("release_date"), errors="coerce").strftime("%a, %d %b %Y")
                    if pd.notna(row.get("release_date")) else "N/A"
                ),

                "genres": row["genres"] if "genres" in row and pd.notna(row["genres"]) else "N/A"
            })

    # Case 2: List of dicts
    elif isinstance(rows, list):
        for row in rows:
            movies.append({
                "title": row.get("title", "N/A"),
                "poster_url": row.get("poster_url", "https://via.placeholder.com/240x360.png?text=No+Poster"),
                "overview": shorten_text(row.get("overview", "No description available")),
                "release_date": (
                    pd.to_datetime(row.get("release_date"), errors="coerce").strftime("%a, %d %b %Y")
                    if pd.notna(row.get("release_date")) else "N/A"
                ),
                "genres": row.get("genres", "N/A")
            })

    return movies


# ---------- Routes ----------
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    search_type = (data.get("type") or "").strip()
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "No input provided"}), 400

    mood_display = None
    rows = []

    if search_type == "Mood":
        emotion = classifier.predict(query)
        genres = mood_to_genres.get(emotion.lower(), ["Drama"])
        rows = recommender.recommend_by_genres(genres, top_n=12)

        # Fallback if no mood match found
        if rows is None or len(rows) == 0:
            rows = recommender.recommend_by_genres("Drama", top_n=12)

        emoji = mood_emojis.get(emotion.lower(), "🎭")
        mood_display = f"{emotion.capitalize()} {emoji}"

    elif search_type == "Keyword":
        rows = recommender.recommend_by_keyword(query, top_n=12)

        # Fallback if keyword not found
        if rows is None or len(rows) == 0:
            rows = recommender.recommend_by_genres("Drama", top_n=12)

    elif search_type == "Actor/Entity":
        rows = recommender.recommend_by_person(query, top_n=12)

        # Fallback if no actor found
        if rows is None or len(rows) == 0:
            rows = recommender.recommend_by_genres("Comedy", top_n=12)

    else:
        return jsonify({"error": "Invalid search type"}), 400

    return jsonify({
        "mood": mood_display,
        "movies": shape_movie_payload(rows)
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
