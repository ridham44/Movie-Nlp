from datasets import load_dataset
import pandas as pd

# Load Hugging Face dataset
dataset = load_dataset("dair-ai/emotion")

# Convert to Pandas DataFrame (train split for example)
df = pd.DataFrame(dataset["train"])

# Map numeric labels to emotion names
label2emotion = {0: "sad", 1: "joy", 2: "love", 3: "anger", 4: "fear", 5: "surprise"}
df["emotion"] = df["label"].map(label2emotion)

# Save to CSV
df[["text", "emotion"]].to_csv("emotion_dataset.csv", index=False)

print("CSV saved as emotion_dataset.csv with columns: text, emotion")
