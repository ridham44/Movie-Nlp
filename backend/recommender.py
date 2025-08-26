import re
import pandas as pd
from fuzzywuzzy import process


# 🔞 Blocked words for adult/NSFW filtering
ADULT_KEYWORDS = [
    "sex", "porn", "xxx", "nude", "erotic", "18+", "adult",
    "desire", "escort", "lust", "doll", "sensual", "hardcore"
]


class MovieRecommender:
    def __init__(self, movies_df: pd.DataFrame):
        # Apply adult filter at load time to be safe
        self.movies_df = self.remove_adult_content(movies_df)

    def normalize_text(self, text):
        """
        Lowercase, remove special characters (like - and .)
        for better matching in keyword search.
        """
        if pd.isna(text):
            return ""
        return re.sub(r'[^a-z0-9 ]', '', str(text).lower())

    def remove_adult_content(self, df: pd.DataFrame):
        """
        Remove adult/NSFW movies based on title, overview, or genre keywords.
        """
        pattern = re.compile("|".join(ADULT_KEYWORDS), re.IGNORECASE)

        safe_df = df[~(
            df["title"].astype(str).str.contains(pattern, na=False) |
            df["overview"].astype(str).str.contains(pattern, na=False) |
            df["genres"].astype(str).str.contains(pattern, na=False)
        )]

        return safe_df

    def recommend_by_genres(self, genres, top_n=12):
        """
        Recommend movies that match any of the given genres.
        Filters adult content automatically.
        """
        if isinstance(genres, str):
            genres = [genres]

        mask = self.movies_df["genres"].apply(
            lambda g: any(genre.lower() in str(g).lower() for genre in genres)
        )

        results = self.movies_df[mask].sort_values(
            by="release_date", ascending=False
        ).head(top_n)


        return results

    def recommend_by_keyword(self, keyword, top_n=12):

        titles = self.movies_df["title"].astype(str).tolist()
        matches = process.extract(keyword, titles, limit=top_n)

        
        matched_titles = [title for title, score in matches if score > 60]
        results = self.movies_df[self.movies_df["title"].isin(matched_titles)]

       
        results = results.sort_values(by="release_date", ascending=False)
        return results.head(top_n)

    def recommend_by_person(self, person_name, top_n=12):
        """
        Recommend movies by actor/director/writer name.
        Only works if dataset has 'cast' or 'crew'.
        """
        if "crew" not in self.movies_df.columns and "cast" not in self.movies_df.columns:
            return pd.DataFrame()  

        person_name = self.normalize_text(person_name)

        mask = False
        if "crew" in self.movies_df.columns:
            mask = mask | self.movies_df["crew"].astype(str).apply(
                lambda x: person_name in self.normalize_text(x)
            )
        if "cast" in self.movies_df.columns:
            mask = mask | self.movies_df["cast"].astype(str).apply(
                lambda x: person_name in self.normalize_text(x)
            )

        results = self.movies_df[mask].sort_values(
            by="vote_average", ascending=False
        ).head(top_n)

        return results
