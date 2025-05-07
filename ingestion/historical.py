import os
import requests
import pandas as pd

API_KEY = "f015bfcc1a314e30bd6e84258644f866"  # Replace with your actual API key

def fetch_and_save_historical_data(symbol: str, start_date: str, end_date: str) -> str:
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "start_date": start_date,
        "end_date": end_date,
        "apikey": API_KEY,
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        print(f"[Error] Failed to fetch data: {data.get('message', 'Unknown error')}")
        return None

    df = pd.DataFrame(data["values"])
    df = df.sort_values("datetime")  # ascending by date

    os.makedirs("data", exist_ok=True)
    filename = f"data/{symbol.replace('.', '_')}_historical_data.csv"
    df.to_csv(filename, index=False)
    print(f"[Success] Data saved to {filename}")
    return filename