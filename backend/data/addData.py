import pandas as pd
import random

# 1. Load your dataset (from Hugging Face converted CSV)
df = pd.read_csv(r"D:\Lj_University\AI\Nlp-Moive\backend\data\emotion_dataset.csv")

# 2. Map Hugging Face emotions to your moods
map_dict = {
    "joy": "happy",
    "love": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "fear",
    "surprise": "surprise"
}

df["mood"] = df["emotion"].map(map_dict)

# 3. Generate synthetic data for missing moods
neutral_samples = [
    "I don’t feel anything special today.",
    "It’s just another ordinary day.",
    "Nothing much is happening.",
    "I am neither happy nor sad, just neutral.",
    "It feels like a regular moment.",
    "Life is moving at its usual pace.",
    "Everything feels calm and steady.",
    "There’s nothing unusual about today.",
    "I feel indifferent about this.",
    "I don’t really care one way or another.",
    "This day feels plain and normal.",
    "I’m not particularly excited or upset.",
    "It’s a balanced and simple mood.",
    "I feel okay, nothing more, nothing less.",
    "Things are just average right now.",
    "I don’t feel strongly about it.",
    "I’m in a steady state of mind.",
    "It feels like a routine day.",
    "My mood is stable and unbothered.",
    "I feel neutral about the outcome.",
    "This doesn’t really affect me.",
    "I’m not leaning towards good or bad.",
    "I feel neither positive nor negative.",
    "It’s just the usual flow of life.",
    "There’s nothing remarkable happening.",
    "I feel blank inside, just plain.",
    "My emotions are flat today.",
    "Nothing excites or bothers me right now.",
    "I feel like I’m in between emotions.",
    "I’m steady and unaffected."
]

curious_samples = [
    "I wonder what will happen next.",
    "That sounds interesting, tell me more!",
    "I’m curious about how this works.",
    "I want to explore and learn more.",
    "What could be the reason behind this?",
    "I’d like to know more details about it.",
    "That sparks my interest instantly.",
    "I’m eager to discover the answer.",
    "I want to figure out how this happens.",
    "This makes me ask so many questions.",
    "I can’t stop thinking about it.",
    "I feel like digging deeper into this.",
    "I need to understand the full story.",
    "I want to know what comes after this.",
    "That idea makes me really intrigued.",
    "I can’t help but wonder about it.",
    "My mind is filled with questions.",
    "That mystery excites me.",
    "I feel drawn to explore this further.",
    "I want to investigate it closely.",
    "This is puzzling, I want answers.",
    "I’d love to see the other side of it.",
    "This topic is fascinating to me.",
    "I keep wondering about the possibilities.",
    "I feel an urge to learn more.",
    "This makes me want to search for more clues.",
    "I’m so invested in finding the truth.",
    "I get lost in curiosity sometimes.",
    "The unknown excites me.",
    "This is something I must understand."
]


excited_samples = [
    "I can’t wait for the weekend!",
    "This is the best day ever!",
    "I’m thrilled about the news!",
    "Wow, this is so exciting!",
    "I feel super pumped right now!",
    "I’m buzzing with energy!",
    "I can’t sit still, I’m so happy!",
    "This opportunity makes me so excited!",
    "I feel on top of the world!",
    "This makes my heart race!",
    "I’m filled with positive energy!",
    "I can’t believe how amazing this is!",
    "This moment is pure joy!",
    "I feel ecstatic and alive!",
    "I’m thrilled beyond words!",
    "This is the highlight of my week!",
    "I can’t stop smiling from excitement!",
    "This feels absolutely amazing!",
    "I’m charged up with excitement!",
    "I feel unstoppable right now!",
    "This makes me jump with joy!",
    "I’m bursting with happiness!",
    "This experience is electrifying!",
    "I feel an adrenaline rush!",
    "This news has me over the moon!",
    "I can’t wait to share this!",
    "I’m so thrilled it finally happened!",
    "I feel a rush of excitement!",
    "This is more than I ever imagined!",
    "I’m so glad to be here right now!"
]


# Create DataFrames for each new mood
extra_data = []
for sentence in neutral_samples:
    extra_data.append((sentence, "neutral"))
for sentence in curious_samples:
    extra_data.append((sentence, "curious"))
for sentence in excited_samples:
    extra_data.append((sentence, "excited"))

# Expand by duplicating random variations (optional)
extra_data = extra_data * 100  # ~500 synthetic examples

extra_df = pd.DataFrame(extra_data, columns=["text", "mood"])

# 4. Combine original + extra data
final_df = pd.concat([df[["text", "mood"]], extra_df], ignore_index=True)

# 5. Save final dataset
final_df.to_csv("emotion_dataset_full.csv", index=False)

print("✅ Final dataset saved as emotion_dataset_full.csv")
print("Moods distribution:\n", final_df["mood"].value_counts())
