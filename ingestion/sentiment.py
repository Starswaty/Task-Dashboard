# ingestion/sentiment.py

import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon", quiet=True)

# Dynamically get path to data/ directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "news_feed.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "news_sentiment.csv")
OUTPUT_TXT = os.path.join(DATA_DIR, "news_sentiment_summary.txt")

os.makedirs(DATA_DIR, exist_ok=True)

def analyze_sentiment(input_file=INPUT_FILE, output_csv=OUTPUT_CSV, output_txt=OUTPUT_TXT):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} not found. Run news.py first.")

    df = pd.read_csv(input_file)
    sid = SentimentIntensityAnalyzer()
    sentiments = []

    for title in df["title"]:
        score = sid.polarity_scores(title)["compound"]
        if score >= 0.05:
            sentiment = "Positive"
        elif score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiments.append(sentiment)

    df["sentiment"] = sentiments
    df.to_csv(output_csv, index=False)

    with open(output_txt, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"[{row['sentiment']}] {row['title']} ({row['source']})\n")

    return df  # Return result for use in Streamlit or other modules
