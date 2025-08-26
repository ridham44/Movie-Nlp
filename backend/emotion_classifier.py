import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "emotion_model.pkl")

def _pick_columns(df: pd.DataFrame):
    """
    Try common column names for text/emotion pairs.
    """
    text_cols = ["text", "Text", "sentence", "Sentence", "content", "Content"]
    label_cols = ["Emotion", "emotion", "label", "Label", "category", "Category"]

    text_col = next((c for c in text_cols if c in df.columns), None)
    label_col = next((c for c in label_cols if c in df.columns), None)
    if not text_col or not label_col:
        raise ValueError(
            f"Could not find text/label columns. Have columns: {list(df.columns)}. "
            "Ensure your CSV has columns like Text, Emotion."
        )
    return text_col, label_col

class EmotionClassifier:
    def __init__(self, csv_path: str):
        os.makedirs(MODEL_DIR, exist_ok=True)
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            df = pd.read_csv(csv_path).dropna()
            text_col, label_col = _pick_columns(df)
            X = df[text_col].astype(str).tolist()
            y = df[label_col].astype(str).tolist()

            self.model = Pipeline([
                ("tfidf", TfidfVectorizer(stop_words="english", max_features=30000)),
                ("clf", LogisticRegression(max_iter=500, n_jobs=None))
            ])
            self.model.fit(X, y)
            joblib.dump(self.model, MODEL_PATH)

    def predict(self, text: str) -> str:
        return self.model.predict([text])[0]
