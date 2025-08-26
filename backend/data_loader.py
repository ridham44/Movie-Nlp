import pandas as pd
from datasets import load_dataset

def load_movie_data():
    """
    Load movies dataset from HuggingFace (Pablinho/movies-dataset)
    and standardize column names.
    """
    dataset = load_dataset("Pablinho/movies-dataset", split="train")
    df = dataset.to_pandas()

    # Standardize column names (lowercase for consistency)
    df = df.rename(columns={
        "Release_Date": "release_date",
        "Title": "title",
        "Overview": "overview",
        "Popularity": "popularity",
        "Vote_Count": "vote_count",
        "Vote_Average": "vote_average",
        "Original_Language": "original_language",
        "Genre": "genres",
        "Poster_Url": "poster_url"
    })

    # Fill NAs safely
    for col in ["title", "overview", "genres", "original_language", "release_date"]:
        df[col] = df[col].fillna("N/A")
        
    # Convert release_date to datetime (safe)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")


    return df
