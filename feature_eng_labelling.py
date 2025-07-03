# --- prepare_ml_dataset.py (Updated with S/R Detection) ---
import os
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
from scipy.signal import argrelextrema

DATA_DIR = "data"
OUTPUT_DIR = "ml_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOOKAHEAD_DAYS = 20  # 4 weeks swing window
RISK_REWARD_RATIO = 3
NUM_SR_ZONES = 8


def engineer_features(df):
    df = df.copy()
    df["returns_1d"] = df["close"].pct_change()
    df["returns_5d"] = df["close"].pct_change(5)
    df["volatility_5d"] = df["returns_1d"].rolling(5).std()
    df["avg_volume_10d"] = df["volume"].rolling(10).mean()

    df["sma_20"] = df["close"].rolling(20).mean()
    df["sma_50"] = df["close"].rolling(50).mean()
    df["above_20ma"] = (df["close"] > df["sma_20"]).astype(int)

    df["candle_body_ratio"] = (df["close"] - df["open"]) / (df["high"] - df["low"] + 1e-6)

    df["rsi_14"] = RSIIndicator(close=df["close"], window=14).rsi()
    df["atr_14"] = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range()

    return df


def detect_sr_levels(df):
    df = df.copy()
    closes = df["close"].values
    idx_max = argrelextrema(closes, np.greater, order=5)[0]
    idx_min = argrelextrema(closes, np.less, order=5)[0]

    resistance_levels = sorted(df.iloc[idx_max].close.values)[-NUM_SR_ZONES:]
    support_levels = sorted(df.iloc[idx_min].close.values)[:NUM_SR_ZONES]

    # Fallback
    if not resistance_levels:
        resistance_levels = [df["high"].max()]
    if not support_levels:
        support_levels = [df["low"].min()]

    sr_distances = []
    for price in df["close"]:
        nearest_res = min(resistance_levels, key=lambda x: abs(x - price))
        nearest_sup = min(support_levels, key=lambda x: abs(x - price))

        res_dist = (nearest_res - price) / price
        sup_dist = (price - nearest_sup) / price
        zone_width = (nearest_res - nearest_sup) / price

        sr_distances.append((res_dist, sup_dist, zone_width))

    df[["resistance_distance", "support_distance", "sr_band_width"]] = sr_distances
    return df


def label_by_risk_reward(df):
    df = df.copy()
    labels = []
    closes = df["close"].values
    lows = df["low"].values
    highs = df["high"].values
    n = len(df)

    for i in range(n):
        entry = closes[i]
        stoploss = lows[i]
        risk = entry - stoploss

        if risk <= 0:
            labels.append(0)
            continue

        target = entry + risk * RISK_REWARD_RATIO
        sl_hit = False
        tp_hit = False

        for j in range(i+1, min(i + LOOKAHEAD_DAYS + 1, n)):
            if lows[j] <= stoploss:
                sl_hit = True
                break
            if highs[j] >= target:
                tp_hit = True
                break

        if tp_hit:
            labels.append(1)
        else:
            labels.append(0)

    df = df.iloc[:len(labels)]
    df["label"] = labels
    return df


def process_stock(file_path):
    symbol = os.path.basename(file_path).replace(".csv", "")
    print(f"Processing {symbol}")

    df = pd.read_csv(file_path)
    df = engineer_features(df)
    df = detect_sr_levels(df)
    df = label_by_risk_reward(df)

    df.dropna(inplace=True)
    df["symbol"] = symbol
    df.to_csv(f"{OUTPUT_DIR}/{symbol}.csv", index=False)


if __name__ == "__main__":
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    for f in files:
        process_stock(os.path.join(DATA_DIR, f))

    print("✅ ML dataset generated with support/resistance features included.")