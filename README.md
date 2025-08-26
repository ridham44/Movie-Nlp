## Movie NLP – MoodyMovies

An end-to-end demo that recommends movies from your mood or keywords using NLP-based emotion detection on the backend and a lightweight frontend UI.

### Features

-   **Mood-based recommendations**: Classifies free-text input into an emotion and maps it to genres.
-   **Keyword search**: Finds movies by title/overview keywords.
-   **Simple UI**: Clean HTML/CSS/JS with a toggle between Mood and Title search.
-   **Flask API**: CORS-enabled endpoints with JSON responses.

---

## Project Structure

```
Movie-Nlp/
  backend/
    app.py
    data_loader.py
    emotion_classifier.py
    recommender.py
    ui_utils.py
    requirements.txt
    data/
      emotion_dataset.csv
      addData.py
      dataToCsv.py
    models/
      emotion_model.pkl
  frontend/
    index.html
    about.html
    contact.html
    app.js
    style.css
    Icon.png
    Default.png
  README.md
```

---

## Prerequisites

-   Python 3.9+ (3.10+ recommended)
-   pip
-   Node/npm not required (plain static frontend)

---

## How It Works (Backend)

1. `EmotionClassifier.predict(text)` infers an emotion label from the input text using data in `data/emotion_dataset.csv` (and the model artifact in `models/`).
2. A mood-to-genre map converts the predicted emotion into candidate genres.
3. `MovieRecommender` retrieves top matches by genre or by keyword/person, returning a Pandas DataFrame or list.
4. Results are normalized to a UI-friendly JSON via `shape_movie_payload`.

---

## Development Notes

-   Logging/observability, tests, and stricter input validation are good next steps.
-   Consider restricting CORS origins for production deployments.
-   Document model provenance and training data for `emotion_model.pkl`.

---

## Troubleshooting

-   Backend not reachable
    -   Ensure it’s running on `127.0.0.1:5000` and no firewall is blocking it.
    -   Hit `/health` to verify: `http://127.0.0.1:5000/health`.
-   CORS errors in browser
    -   Serve the frontend via a local server (e.g., `python -m http.server`).
    -   Keep backend and frontend on localhost to avoid mixed-origin issues.
-   Empty recommendations
    -   For rare moods/keywords, fallbacks revert to broad genres (e.g., Drama/Comedy). Try another input.

---

## License

Educational/demo purposes. Adapt as needed for coursework or experiments.
