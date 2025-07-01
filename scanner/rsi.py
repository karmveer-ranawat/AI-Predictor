import pandas as pd
import numpy as np
from kite_auth import get_kite
from instrument_lookup import get_token
from datetime import datetime, timedelta
import os

kite = get_kite()


def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def scan_rsi(symbols):
    rsi_output = []

    for symbol in symbols:
        print(f"Scanning (RSI): {symbol}")
        try:
            token = get_token(symbol)
            from_date = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")

            candles = kite.historical_data(token, from_date, to_date, interval="day")
            df = pd.DataFrame(candles)

            if len(df) < 100:
                continue

            df["rsi"] = calculate_rsi(df["close"])
            df["ma200"] = df["close"].rolling(window=200).mean()
            latest = df.iloc[-1]

            # Filter: RSI < 30 AND close > 200MA (stock in long-term uptrend)
            if latest["rsi"] < 30 and latest["close"] > latest["ma200"]:
                rsi_output.append({
                    "Symbol": symbol,
                    "Latest RSI": round(latest["rsi"], 2),
                    "Close": round(latest["close"], 2),
                    "200 MA": round(latest["ma200"], 2)
                })

        except Exception as e:
            print(f"Error for {symbol}: {e}")

    if rsi_output:
        df_rsi = pd.DataFrame(rsi_output)
        os.makedirs("output", exist_ok=True)
        df_rsi.to_csv("output/rsi_scan_results.csv", index=False)
        print("✅ RSI Scan completed. Results saved to output/rsi_scan_results.csv")
    else:
        print("⚠️ No RSI matches found.")


if __name__ == "__main__":
    symbols = ["RELIANCE", "TCS", "INFY", "SBIN", "TATAMOTORS", "TATASTEEL", "IRFC", "IRCTC", "ITC", "IOC", "BATAINDIA",
               "RAYMOND", "TITAN", "TRIDENT", "PNB", "BHARATWIRE", "HIGHENE", "HINDUNILVR", "PAYTM", "TATATECH",
               "IREDA", "ONGC", "HDFCBANK", "LT", "NHPC", "UCOBANK", "SUZLON", "YESBANK", "TATAPOWER", "INDHOTEL",
               "RVNL", "HAL", "BEL", "ETERNAL", "GAIL", "ADANIPOWER", "ADANIENT", "BAJAJHFL", "AXISBANK", "SWIGGY",
               "AETHER"]
    scan_rsi(symbols)
