import os
import pandas as pd
from datetime import datetime, timedelta
from scanner.kite_auth import get_kite
from scanner.instrument_lookup import get_token

kite = get_kite()

# --- CONFIG ---
SYMBOLS = ["RELIANCE", "TCS", "INFY", "SBIN", "TATAMOTORS", "TATASTEEL", "IRFC", "IRCTC", "ITC", "IOC", "BATAINDIA",
           "RAYMOND", "TITAN", "TRIDENT", "PNB", "BHARATWIRE", "HIGHENE", "HINDUNILVR", "PAYTM", "TATATECH", "IREDA",
           "ONGC", "HDFCBANK", "LT", "NHPC", "UCOBANK", "SUZLON", "YESBANK", "TATAPOWER", "INDHOTEL", "RVNL", "HAL",
           "BEL", "ETERNAL", "GAIL", "ADANIPOWER", "ADANIENT", "BAJAJHFL", "AXISBANK", "SWIGGY", "AETHER" ]

START_YEARS = 4  # years of past data
DATA_DIR = "data"
INTERVAL = "day"

os.makedirs(DATA_DIR, exist_ok=True)


def fetch_and_save(symbol):
    print(f"Fetching: {symbol}")
    try:
        token = get_token(symbol)
        from_date = (datetime.now() - timedelta(days=START_YEARS * 365)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        candles = kite.historical_data(
            token,
            from_date,
            to_date,
            interval=INTERVAL
        )

        df = pd.DataFrame(candles)
        df = df[["date", "open", "high", "low", "close", "volume"]]
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df.to_csv(f"{DATA_DIR}/{symbol}.csv", index=False)
        print(f"✅ Saved: {symbol} ({len(df)} rows)")

    except Exception as e:
        print(f"❌ Failed: {symbol} → {e}")


if __name__ == "__main__":
    for sym in SYMBOLS:
        fetch_and_save(sym)
