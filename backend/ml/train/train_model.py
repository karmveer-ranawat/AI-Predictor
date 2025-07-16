# backend/ml/train/train_model.py
import os
import json
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import layers, models

def train_model(
    input_csv="combined_dataset/train_dataset.csv",
    features=None,
    label_col="label",
    test_ratio=0.2,
    epochs=30,
    batch_size=32,
    save_dir = os.path.join("ml", "models", "global")
):
    if features is None:
        features = [
            'returns_1d', 'returns_5d', 'volatility_5d', 'avg_volume_10d',
            'sma_20', 'sma_50', 'above_20ma', 'candle_body_ratio',
            'rsi_14', 'atr_14', 'support_distance',
            'resistance_distance', 'sr_band_width', 'symbol_encoded'
        ]

    os.makedirs(save_dir, exist_ok=True)

    df = pd.read_csv(input_csv)
    df.dropna(inplace=True)

    # Dynamically remove symbol_encoded if not present
    feature_list = [f for f in features if f in df.columns]

    X = df[feature_list].values
    y = df[label_col].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = models.Sequential([
        layers.Input(shape=(X_train.shape[1],)),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    loss, accuracy = model.evaluate(X_test, y_test)

    model_path = os.path.join(save_dir, "model.h5")
    scaler_path = os.path.join(save_dir, "scaler.pkl")
    metadata_path = os.path.join(save_dir, "metadata.json")

    model.save(model_path)
    joblib.dump(scaler, scaler_path)

    metadata = {
        "accuracy": round(float(accuracy), 4),
        "epochs": epochs,
        "batch_size": batch_size,
        "test_ratio": test_ratio,
        "trained_on": datetime.now().isoformat(),
        "model_path": model_path,
        "scaler_path": scaler_path,
        "input_csv": input_csv,
        "features_used": feature_list
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Test Accuracy: {accuracy:.4f}")
    print(f"✅ Model saved to: {model_path}")
    print(f"✅ Scaler saved to: {scaler_path}")
    print(f"✅ Metadata saved to: {metadata_path}")

    return metadata
