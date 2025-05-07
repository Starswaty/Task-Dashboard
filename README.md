# 📊 Real-Time Financial RAG Dashboard

Welcome to the **Real-Time Financial RAG Portal**—a web-accessible, intelligent dashboard built using **Streamlit** that integrates:
- 📈 Stock Market Data (Historical + Real-Time)
- 💹 Live Currency Exchange Rates
- 📰 Deal-News Aggregation
- 🧠 Sentiment Analysis
- 📄 PDF Summarization
- 🔍 RAG (Retrieval-Augmented Generation) Interface

> 🔗 **Live App**: [task-dashboard.streamlit.app](https://task-dashboard.streamlit.app)  
> 🚀 No installation required—runs directly in the browser!

---

## 📌 Project Overview

This project combines multiple data ingestion pipelines with RAG-based querying to generate financial insights, visualizations, and summaries—all in a unified, interactive interface.

### 🎯 Key Features

| Module              | Description |
|---------------------|-------------|
| **📜 News Feed Aggregation** | Fetches and stores news related to companies like TCS, INFY, etc. |
| **📊 Sentiment Analysis** | Analyzes news sentiment using NLP models and visualizes market sentiment shifts. |
| **💸 FX Rates** | Live exchange rates for USD/INR, EUR/INR, JPY/INR, and CHF/INR using a free API. |
| **📈 Historical Stock Data** | Pulls historical data for companies using the NSE India API. |
| **📉 Real-Time Quotes** | Subscribes to real-time feeds and updates selected tickers dynamically. |
| **📄 PDF Summarizer** | Extracts key summaries from uploaded or ingested financial reports. |
| **🧠 RAG Query Handler** | Accepts free-form queries and returns synthesized insights from indexed sources using FAISS. |
| **📊 Interactive Dashboard** | Built using Streamlit and Plotly for real-time visualizations and CSV downloads. |

---

## 🗂️ Project Structure

.
├── data/ # Ingested raw and processed data files
│ ├── TCS_historical_data.csv
│ ├── fx_rates.csv
│ ├── news_feed.csv
│ └── ...
│
├── ingestion/ # Data ingestion and preprocessing pipelines
│ ├── fx.py
│ ├── news.py
│ ├── real_time.py
│ ├── sentiment.py
│ ├── pdf_summarizer.py
│ └── ...
│
├── rag/ # Retrieval-Augmented Generation layer
│ ├── faiss_index.py
│ └── query_handler.py
│
├── streamlit/ # Main app and config
│ ├── app.py
│ └── config.toml
│
├── requirements.txt # Project dependencies
└── README.md # You're here!


## 🔍 How It Works

1. **Ingestion Pipelines** pull real-time data from APIs, RSS feeds, and PDFs.
2. **Processing Modules** clean, analyze, and store data (sentiment, FX rates, stocks).
3. **FAISS-based Indexing** allows semantic search over processed content.
4. **Streamlit UI** provides an easy-to-use dashboard to view, interact, and query all modules.

---

## 💻 Usage Instructions

### 🔗 Access the Live Dashboard

> 🌐 [Click here to launch the app](https://task-dashboard.streamlit.app)

You can:
- Select stock symbols to view historical or real-time data.
- Analyze sentiment for major deal/news headlines.
- View summarized PDFs of financial reports.
- Export processed data as CSVs.
- Submit natural language queries and receive generated summaries.

### 🧪 Try Sample Queries

"Latest deals, sentiment shifts, FX rates, and earnings highlights for TCS"
"Summarize the real-time performance and sentiment for INFY"
"Give a summary of the latest PDF report uploaded"
## ⚙️ Tech Stack

 - Python 3.x
 - Streamlit – Frontend Dashboard
 - FAISS – Vector search
 - yfinance / NSE API – Market data
 - feedparser – News ingestion
 - nltk, textblob, transformers – NLP + Sentiment
 - pdfplumber / PyPDF2 / sumy – PDF summarization
 - Plotly / Matplotlib – Visualization
 - Cohere API – (Optional) LLM-based enhancements

### 📦 Dependencies
Install all dependencies using:

''bash
pip install -r requirements.txt

### 📤 Data Output
Each module generates a .csv or .txt file under the /data directory. The final insights and user queries are handled through the RAG system and visualized on the Streamlit dashboard.

### 🛠️ Developer Notes
Modular design allows you to plug or unplug modules easily.
config.toml is used to store API keys and global settings.
All code is optimized for online deployment; no local setup required by end-users.

### 📬 Contact
For queries, contributions, or enhancements, feel free to open issues or pull requests.

