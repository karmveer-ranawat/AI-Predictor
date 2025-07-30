import os
import json
import argparse
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import layers, models, optimizers, callbacks

# ──────────────────────────────── Grid search config
EPOCHS = [20, 30, 50]
BATCH_SIZES = [16, 32, 64]
LAYER_CONFIGS = [
    [64, 32],
    [128, 64],
    [128, 64, 32]
]
DROPOUT_RATES = [0.2, 0.3, 0.4]

FEATURES = [
    'returns_1d', 'returns_5d', 'volatility_5d', 'avg_volume_10d',
    'sma_20', 'sma_50', 'above_20ma', 'candle_body_ratio',
    'rsi_14', 'atr_14', 'support_distance',
    'resistance_distance', 'sr_band_width', 'symbol_encoded'
]

# ──────────────────────────────── Grid training loop
def run_grid_search(input_csv, output_dir, test_ratio=0.2):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    df.dropna(inplace=True)

    feature_list = [f for f in FEATURES if f in df.columns]
    X = df[feature_list].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_ratio, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    results = []
    best_score = -1
    best_model = None
    best_meta = {}

    print("\n🔍 Starting grid search...")

    for layers_config in LAYER_CONFIGS:
        for dr in DROPOUT_RATES:
            for epochs in EPOCHS:
                for batch_size in BATCH_SIZES:
                    model = models.Sequential()
                    model.add(layers.Input(shape=(X_train.shape[1],)))
                    for units in layers_config:
                        model.add(layers.Dense(units, activation="relu"))
                        model.add(layers.Dropout(dr))
                    model.add(layers.Dense(1, activation="sigmoid"))

                    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
                    h = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                                  validation_split=0.1, verbose=1)
                    loss, acc = model.evaluate(X_test, y_test, verbose=1)

                    meta = {
                        "accuracy": round(float(acc), 4),
                        "epochs": epochs,
                        "batch_size": batch_size,
                        "dropout": dr,
                        "layer_config": layers_config,
                        "test_ratio": test_ratio,
                        "trained_on": datetime.now().isoformat(),
                        "features_used": feature_list,
                    }

                    results.append(meta)

                    if acc > best_score:
                        best_score = acc
                        best_model = model
                        best_meta = meta.copy()

    print(f"\n🏆 Best accuracy: {best_score:.4f}")

    # Save best model
    best_model.save(os.path.join(output_dir, "best_model.h5"))
    joblib.dump(scaler, os.path.join(output_dir, "best_scaler.pkl"))
    with open(os.path.join(output_dir, "best_metadata.json"), "w") as f:
        json.dump(best_meta, f, indent=2)
    with open(os.path.join(output_dir, "grid_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Saved best model and full grid results.")

# ──────────────────────────────── Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", required=True, help="Path to processed CSV file")
    parser.add_argument("--output_dir", required=True, help="Directory to save models and metadata")
    args = parser.parse_args()

    run_grid_search(args.input_csv, args.output_dir)
