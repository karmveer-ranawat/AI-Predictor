# backend/scanner/scanners/ma44.py
import pandas as pd
import numpy as np
from kite_auth.kite_session import get_kite
from scanner.instrument_lookup import get_token
from datetime import datetime, timedelta
import os

def run_ma44_scanner(symbols=None):
    kite = get_kite()
    output_rows = []

    if symbols is None:
        symbols = [ ... ]  # full symbol list here

    for symbol in symbols:
        try:
            token = get_token(symbol)
            from_date = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")

            candles = kite.historical_data(token, from_date, to_date, interval="day")
            df = pd.DataFrame(candles)

            if len(df) < 60:
                continue

            df["ma44"] = df["close"].rolling(window=44).mean()
            df.dropna(inplace=True)

            last = df.iloc[-1]
            ma_slope = df["ma44"].iloc[-1] - df["ma44"].iloc[-10]
            proximity = abs(last["close"] - last["ma44"]) / last["ma44"]
            above_pct = (df.tail(20)["close"] > df.tail(20)["ma44"]).mean()
            recent = df.tail(5)
            range_pct = (recent["high"].max() - recent["low"].min()) / recent["close"].mean()
            recent_touch = df.iloc[-2]
            bullish_touch = (
                recent_touch["low"] <= recent_touch["ma44"] and
                recent_touch["close"] > recent_touch["open"]
            )

            if (
                last["close"] > last["ma44"]
                and proximity < 0.02
                and ma_slope > 0.3
                and above_pct >= 0.6
                and range_pct > 0.03
                and bullish_touch
            ):
                entry = round(last["close"], 2)
                sl = round(last["ma44"], 2)
                risk = round(entry - sl, 2)
                target = round(entry + 2 * risk, 2)
                score = (
                    (1 - proximity) * 0.4 +
                    (ma_slope / last["ma44"]) * 0.3 +
                    above_pct * 0.3
                )

                output_rows.append({
                    "Symbol": symbol,
                    "Entry": entry,
                    "SL": sl,
                    "Target": target,
                    "Proximity_to_MA": round(proximity * 100, 2),
                    "MA_Slope": round(ma_slope, 2),
                    "Strength": f"{int(above_pct * 100)}% above MA (last 20)",
                    "Confidence": round(score * 100, 2)
                })

        except Exception as e:
            print(f"Error for {symbol}: {e}")

    if output_rows:
        df_out = pd.DataFrame(output_rows)
        os.makedirs("scanner/output", exist_ok=True)
        df_out.to_csv("scanner/output/scan_results.csv", index=False)
        print("✅ Scan results saved.")
        return df_out
    else:
        print("⚠️ No stocks matched.")
        return pd.DataFrame()
