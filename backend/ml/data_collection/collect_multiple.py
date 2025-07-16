# backend/ml/data_collection/collect_multiple.py

import os
import pandas as pd
from datetime import datetime, timedelta
from kite_auth.kite_session import get_kite
from scanner.instrument_lookup import get_token

kite = get_kite()

def fetch_and_save(symbol, years=4, interval="day", output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Fetching: {symbol}")
    try:
        token = get_token(symbol)
        from_date = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        candles = kite.historical_data(token, from_date, to_date, interval=interval)
        df = pd.DataFrame(candles)
        df = df[["date", "open", "high", "low", "close", "volume"]]
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df.to_csv(f"{output_dir}/{symbol}.csv", index=False)

        print(f"✅ Saved: {symbol} ({len(df)} rows)")
        return True
    except Exception as e:
        print(f"❌ Failed: {symbol} → {e}")
        return False

def fetch_batch(symbols, years=4, interval="day", output_dir="data"):
    results = {}
    for symbol in symbols:
        success = fetch_and_save(symbol, years, interval, output_dir)
        results[symbol] = success
    return results
