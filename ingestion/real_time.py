import requests
import pandas as pd
import time
import os
from datetime import datetime
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Updated headers to closely mimic a real browser request
NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.nseindia.com/"
}

BASE_URL = "https://www.nseindia.com/api/quote-equity"

# Custom cookies from the previous input
CUSTOM_COOKIES = {
   "_abck": "B0C130E6630ADCE054CADAD039F8FB11~0~YAAQZF06FxsQIn6WAQAAybUyqA1ni4AgZxVqKh5MelD8eISgBPdbAFOZ7nJ8PGR3ZMBDiSprkbe6Z0Mfnyqf/j7opNMEiBvbn2h3rhUDKGWIIqOK7/3U692zy2C8+gx77GBkVheDDWEf2YVAnNeuDUIJCsDEc1l3npoi44eQxkdv3H5iSdljsJX67evsk3G7+PlwbC+6RiMeSu6nHwu4RKvFv72uGN3h+JP3TPiuMzr6Ov2LlOEIxTIKVhUl6mg0IhTW2jBA9U8wrTCfsmRIdn8x3nWHvKl0JdCOen4wa7UT96OQxZTrcYZISdB+NBenDz92D+8lbjzgIe3tVx08QaFxQ0QRUmqU0fNrpVR2nqMauvqvIre7pJvrhgpnMWZLwmcsXPuu6B+PxZq03q+fE/NJGLukAuUo5WgaXAxcmsYswnAvBrrUsLZBw7W6JLZtrzinnNPG3oKGK8erZ1ARuocek9UlKk1IlvMTAcs1ARZZreg/tTtB25UjcTh4/dZ3ISvZyXKAPFUylIGxjXFa10vxtN0hUYY1tq6dlxJi5OQhcS11iapL761E55Vd7c7L8aEJzf0m9m2WKEdYimZn5DMo8Sf1~-1~-1~-1",
    "ak_bmsc": "1C74C42D389BF3D665DC32D35E30C89D~000000000000000000000000000000~YAAQZF06FxwQIn6WAQAAybUyqBugfCn83LMv6Ta5oVrow9+4FZ7+vOC76BvdA2O9qct7TFLTVXoHleUfJMlReZbFDzz43XDxyo4h+oETIlquTI9IKtBl3ajTtqBYTxZsM09HEJYPrP/dF39JieHoF5q+aqtZdNDQhr4lf+gyE05m7mVgCYw2kBoZabqwVnlmxmjyapZElyDFKSe7Uei20mjxh0XlQN4psN4cf+7ZwJEnUy6Lr7UoDrasYLR6qu6OndqC++4X2M5i1/Aeo6vPH7cT/Cf0GefT/MWBTbqacB+OSjP4Xu13nfzqwLzOZBXkIMt7agk/UY8CSjKAvFhbegMJ6fVn3jIQX1FACRVA968SmlxdByhy3FAuDYQSMC/iMKVfGSTsASn4m7Vd",
    "bm_mi": "B150746CB99A77AB2F40086756CF6E87~YAAQZF06FyEQIn6WAQAAUbkyqBth/ziNWl13RGZ912IkhaVZNshKvbPRvE8cXy2LB6ifV3BpCqTIDwITKlVopgi5RB4cUpyrb1LMxCRdZ88Z7TRKWhE1ZYv2OCq3Zqnp44KS2muwTgkF8WZBAI2IYXUF7mKus5QlFqEIwnxpVyIGFuURM53idgVT1fHRKMEl0rJqztJM7uSrN0ukUjcMXWlW6KhrTRNnf1hhKmm8NOXsH9KGRvBmV6Ak3Uvw1C1FtKplUPz0LOGbTFUaqv9AYTAwalgtgSigDYsl+PW2/KylQD8G+qE9W79vw6uC2inrbtvNTYQOUY3s+5afqXj75GewvsWgOxCKV3m2rs6xxsvSHV5jHBF7JH2YNr1k~1",
    "bm_sv": "0B32A4F30769EEB8C04F42D3CF2674B7~YAAQZF06FyIQIn6WAQAAUbkyqBvw4iP8LK5Qn5rP3CCDsNrMy0b4yYKfHjt7X8t7yG/d5mMp7aDKMN46BkxsEVbU0ugq4R5EvsYJuX6GbqHxRi6IemFVphcOsDCytdIizniG+4zSfdvcKuJE1t4/8+rcmiL3ZJ7Lqftirrtn7iTuUvMSmy3kQE4PtKbYYUqwqUwInz/6b+AEO+FOoJGItIFtonzkH0uwZJVSFoEq8f/IB3jX2Bm+wMfq0yGP0ri3d14=~1",
    "bm_sz": "CA13C8C1E58D5D7B03866A1164799624~YAAQZF06Fx4QIn6WAQAAybUyqBtPOaaNphzdkcbs7on4EjbR6CdVQQmPo2UAaQop61ml4OdXWxc3ZCG6H2vtaev4zTvMsVNRvs5rdyeiXGruK+1h7Q3Dz7mlBdRJZmWyPFYveYhhrqLGo0tvxzDgmDheCOTwYHHq2KJnlrkOh32h0vFutLFEeYC2vMqlW0wyKJ+g1HfQmLdTBJbXJJXJM9Ks1LQSpPtECBmvPrI5pEq17zXha0Vpy8fKLG7Ii+wxfMKDWUCVicZc4YKDaKh46hEG97x4vgJFuYwXNMk6KKHQFb1Da05YlsWqvEuLS2+emUAgGOtig1O3dkL2bAUbn/3zrIBAXxTwcjnIC7OGGbznmjgLO8zacQ==~3289145~3420993",
    "nseappid": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc0NjU3ODYxNiwiZXhwIjoxNzQ2NTg1ODE2fQ.YIc7lxy0yjW3uPsM6Vd7qzITrxNDD6HBHZ7pYRQ1MJw",
    "nsit": "ylcCiJZMU5VSv2EMqkgDmI_x"
}

# Global session
session = requests.Session()
session.headers.update(NSE_HEADERS)
session.cookies.update(CUSTOM_COOKIES)

def setup_nse_session():
    try:
        print("[~] Initializing session with NSE homepage...")
        response = session.get("https://www.nseindia.com", timeout=10)
        cookies = session.cookies.get_dict()
        print(f"[✓] Session initialized successfully. Cookies: {cookies}")
        time.sleep(5)
    except Exception as e:
        print(f"[!] Failed to initialize session: {e}")

def get_realtime_data(symbol):
    url = f"{BASE_URL}?symbol={symbol.upper()}"
    try:
        response = session.get(url, timeout=10)

        if response.status_code == 401:
            print(f"[!] {symbol} - Unauthorized. Check your session or headers.")
            return None
        elif response.status_code == 429:
            print(f"[!] Rate limit hit for {symbol}. Sleeping for 60 seconds...")
            time.sleep(60)
            return get_realtime_data(symbol)
        
        if response.status_code != 200:
            print(f"[!] {symbol} - Unexpected response status: {response.status_code}")
            return None

        data = response.json()
        quote = data.get("priceInfo", {})
        meta = data.get("metadata", {})

        return {
            "symbol": symbol.upper(),
            "companyName": meta.get("companyName"),
            "lastPrice": quote.get("lastPrice"),
            "change": quote.get("change"),
            "pChange": quote.get("pChange"),
            "dayHigh": quote.get("intraDayHighLow", {}).get("max"),
            "dayLow": quote.get("intraDayHighLow", {}).get("min"),
            "totalTradedVolume": quote.get("totalTradedVolume"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"[!] Error fetching {symbol}: {e}")
        return None

def poll_realtime_quotes(symbols, interval_seconds=5, duration_minutes=1, output_csv=None):
    """
    Polls real-time data for a list of symbols every 'interval_seconds' for 'duration_minutes'.
    Appends data to CSV after each poll.
    """
    if output_csv is None:
        output_csv = os.path.join(DATA_DIR, "realtime_feed.csv")
    else:
        if not os.path.isabs(output_csv):
            output_csv = os.path.join(DATA_DIR, output_csv)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    total_polls = int((duration_minutes * 60) / interval_seconds)
    print(f"[✓] Starting real-time polling for {symbols} every {interval_seconds}s for {duration_minutes} minutes...")

    for i in range(total_polls):
        batch = []
        print(f"[~] Poll {i+1}/{total_polls} at {datetime.now().strftime('%H:%M:%S')}")

        for symbol in symbols:
            quote = get_realtime_data(symbol)
            if quote:
                print(f"  → {symbol}: ₹{quote['lastPrice']} ({quote['pChange']}%)")
                batch.append(quote)

        if batch:
            df = pd.DataFrame(batch)
            write_header = not os.path.exists(output_csv) or os.stat(output_csv).st_size == 0
            df.to_csv(output_csv, mode='a', index=False, header=write_header)

        time.sleep(interval_seconds)

    print(f"[✓] Polling finished. Output saved to {output_csv}")

if __name__ == "__main__":
    setup_nse_session()

    # User input: comma-separated symbols
    user_input = input("Enter comma-separated NSE symbols (e.g., TCS, INFY, RELIANCE): ")
    symbols = [s.strip().upper() for s in user_input.split(",") if s.strip()]

    poll_realtime_quotes(
        symbols=symbols,
        interval_seconds=5,
        duration_minutes=1
        # No need to pass output_csv; will default to data/realtime_feed.csv
    )
