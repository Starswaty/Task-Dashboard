import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
from ingestion.news import fetch_news
from ingestion.sentiment import analyze_sentiment
from ingestion.fx import fetch_live_fx_rates
from ingestion.historical import fetch_and_save_historical_data
from ingestion.real_time import poll_realtime_quotes
from ingestion.pdf_summarizer import extract_text_from_pdf
from rag.query_handler import generate_synthesis_with_cohere
from ingestion.sentiment_analysis import sentiment_analysis
import os

# Page config
st.set_page_config(page_title="Unified RAG Portal", layout="wide", page_icon="📊")

st.title("📊 Unified RAG Intelligence Dashboard")

# --- 1. Live FX Rates ---
st.header("💱 Live Currency Exchange Rates")
fx_data = fetch_live_fx_rates()
st.dataframe(fx_data)
csv_fx = fx_data.to_csv(index=False).encode()
st.download_button("Download FX Rates as CSV", csv_fx, "fx_rates.csv", "text/csv")

fx_long = fx_data.melt(id_vars='Timestamp', var_name='Currency', value_name='Rate')
fig_fx = px.bar(fx_long, x='Currency', y='Rate', color='Currency', title="Live INR Currency Rates")
st.plotly_chart(fig_fx, use_container_width=True)

# --- 2. Real-Time Stock Data ---
REALTIME_CSV = os.path.join("data", "realtime_feed.csv")

st.header("📈 Real-Time Stock Prices")

# User input: comma-separated symbols
user_input = st.text_input("Enter company names separated by commas (e.g., TCS, INFY, RELIANCE):")

if user_input:
    tickers = [ticker.strip().upper() for ticker in user_input.split(",") if ticker.strip()]
    poll_realtime_quotes(user_input)
    # Check if the CSV file exists
    if os.path.exists(REALTIME_CSV):
        # Read the CSV file
        real_time_df = pd.read_csv(REALTIME_CSV)

        # Filter the data based on the entered symbols
        filtered_df = real_time_df[real_time_df['symbol'].isin(tickers)]

        if not filtered_df.empty:
            st.dataframe(filtered_df)

            csv_rt = filtered_df.to_csv(index=False).encode()
            st.download_button("Download Real-Time Stock Data as CSV", csv_rt, "real_time.csv", "text/csv")

            # Plot data
            import plotly.express as px
            fig_rt = px.line(filtered_df, x='timestamp', y='lastPrice', color='symbol', title="Real-Time Stock Movement")
            st.plotly_chart(fig_rt, use_container_width=True)
        else:
            st.warning("No data found for the selected tickers.")
    else:
        st.warning(f"[!] No real-time data found. Please ensure the real-time script is running.")

# --- 3. Historical Stock Data ---
st.title("📊 Stock Historical Data Viewer (Twelve Data API)")

symbol = st.text_input("Enter Stock Symbol (e.g., TCS.BSE, INFY.NSE)", "TCS.BSE")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Fetch Historical Data"):
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    csv_path = fetch_and_save_historical_data(symbol, start_str, end_str)

    if csv_path:
        df = pd.read_csv(csv_path)
        st.dataframe(df)

        with open(csv_path, "rb") as f:
            st.download_button(
                label="📥 Download CSV",
                data=f,
                file_name=os.path.basename(csv_path),
                mime="text/csv"
            )
    else:
        st.error("Failed to fetch or save stock data.")

# --- 4. Deal News Aggregation ---
st.header("📰 IT Deal News")
news_df = fetch_news()
st.dataframe(news_df)
news_df = pd.DataFrame(news_df)
csv_news = news_df.to_csv(index=False).encode()
st.download_button("Download News as CSV", csv_news, "deal_news.csv", "text/csv")

# --- 5. News Sentiment Analysis ---
REALTIME_CSV1 = os.path.join("data", "news_feed.csv")
st.header("🧠 News + Sentiment Analysis")
sentiment_results = analyze_sentiment(REALTIME_CSV1)
combined_df = pd.DataFrame(sentiment_results)
st.dataframe(combined_df)

fig_sent = px.histogram(combined_df, x='sentiment', color='sentiment', title="News Sentiment Distribution")
st.plotly_chart(fig_sent, use_container_width=True)
csv_combined = combined_df.to_csv(index=False).encode()
st.download_button("Download News + Sentiment as CSV", csv_combined, "news_sentiment.csv", "text/csv")

# --- 6. RAG Query Interface ---
st.header("🤖 RAG-Based Answer Engine")
query = st.text_input("Ask your question (e.g., 'Latest FX and sentiment for TCS')", "")
if st.button("Run RAG Query"):
    with st.spinner("Thinking..."):
        answer = generate_synthesis_with_cohere(query)
        st.success(answer)

# --- 7. PDF Summarizer ---
def convert_summary_to_txt(summary_text):
    return BytesIO(summary_text.encode("utf-8"))

st.title("📄 PDF Summarizer & Exporter")

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
if pdf_file is not None:
    extracted_text = extract_text_from_pdf(pdf_file)

    st.subheader("📄 Summary")
    st.write(extracted_text)

    # Buttons to download summary
    txt_buffer = convert_summary_to_txt(extracted_text)

    st.download_button("📄 Download Summary as TXT", data=txt_buffer, file_name="summary.txt", mime="text/plain")   

# --- 8. Custom Text Sentiment Analysis ---
st.header("🗣️ Analyze Sentiment of Your Own Text")
user_input = st.text_area("Enter text:")
if st.button("Analyze Sentiment"):
    user_sentiment = sentiment_analysis(user_input)
    st.write(f"**Sentiment:** {user_sentiment}")


