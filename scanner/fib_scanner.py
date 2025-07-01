# --- fib_scanner.py ---
import pandas as pd
import numpy as np
from kite_auth import get_kite
from instrument_lookup import get_token
from datetime import datetime, timedelta
from scipy.signal import argrelextrema
import os

kite = get_kite()

def scan_fibonacci(symbols):
    fib_output = []

    for symbol in symbols:
        print(f"Scanning (FIB): {symbol}")
        try:
            token = get_token(symbol)
            from_date = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")

            candles = kite.historical_data(token, from_date, to_date, interval="day")
            df = pd.DataFrame(candles)

            if len(df) < 60:
                print(f"Not enough data for {symbol}")
                continue

            last = df.iloc[-1]

            # --- Fib retracement logic ---
            df.reset_index(drop=True, inplace=True)
            local_max = argrelextrema(df["high"].values, np.greater, order=5)[0]
            local_min = argrelextrema(df["low"].values, np.less, order=5)[0]

            if len(local_min) == 0 or len(local_max) == 0:
                continue

            recent_low = local_min[-1]
            recent_high = local_max[local_max > recent_low]
            if len(recent_high) == 0:
                continue

            # Ensure swing covers enough candles
            if (recent_high[-1] - recent_low) < 10:
                continue

            swing_low = df.iloc[recent_low]
            swing_high = df.iloc[recent_high[-1]]

            # Require the swing to be strong
            swing_strength = (swing_high["close"] - swing_low["close"]) / swing_low["close"]
            if swing_strength < 0.1:
                continue

            fib_38 = swing_high["close"] - 0.382 * (swing_high["close"] - swing_low["close"])
            fib_50 = swing_high["close"] - 0.5 * (swing_high["close"] - swing_low["close"])
            fib_618 = swing_high["close"] - 0.618 * (swing_high["close"] - swing_low["close"])

            if fib_618 <= last["close"] <= fib_38:
                score = (
                    (1 - abs(last["close"] - fib_50) / fib_50) * 0.6 +
                    0.4  # placeholder boost for hitting fib zone
                )
                fib_output.append({
                    "Symbol": symbol,
                    "Swing Low": round(swing_low["close"], 2),
                    "Swing High": round(swing_high["close"], 2),
                    "Fib Zone": f"{round(fib_618,2)} - {round(fib_38,2)}",
                    "Current Price": round(last["close"], 2),
                    "Confidence": round(score * 100, 2)
                })

        except Exception as e:
            print(f"Error for {symbol}: {e}")

    if fib_output:
        df_fib = pd.DataFrame(fib_output)
        os.makedirs("output", exist_ok=True)
        df_fib.to_csv("output/fib_scan_results.csv", index=False)
        print("✅ Fib Scan completed. Results saved to output/fib_scan_results.csv")
    else:
        print("⚠️ No Fib matches found.")


if __name__ == "__main__":
    symbols = ["RELIANCE", "TCS", "INFY", "SBIN", "TATAMOTORS", "TATASTEEL", "IRFC", "IRCTC", "ITC", "IOC", "BATAINDIA",
               "RAYMOND", "TITAN", "TRIDENT", "PNB", "BHARATWIRE", "HIGHENE", "HINDUNILVR", "PAYTM", "TATATECH",
               "IREDA", "ONGC", "HDFCBANK", "LT", "NHPC", "UCOBANK", "SUZLON", "YESBANK", "TATAPOWER", "INDHOTEL",
               "RVNL", "HAL", "BEL", "ETERNAL", "GAIL", "ADANIPOWER", "ADANIENT", "BAJAJHFL", "AXISBANK", "SWIGGY",
               "AETHER"]
    scan_fibonacci(symbols)
