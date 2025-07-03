# --- train_dl_model.py ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import layers, models

# Load dataset
df = pd.read_csv("dataset/train_dataset.csv")

# Drop rows with missing values
df.dropna(inplace=True)

# Features and label
FEATURES = [
    'returns_1d', 'returns_5d', 'volatility_5d', 'avg_volume_10d',
    'sma_20', 'sma_50', 'above_20ma', 'candle_body_ratio',
    'rsi_14', 'atr_14',
    'support_distance', 'resistance_distance', 'sr_band_width',
    'symbol_encoded'
]
LABEL = 'label'

X = df[FEATURES].values
y = df[LABEL].values

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Deep Learning model
model = models.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\n✅ Test Accuracy: {accuracy:.4f}")

# Save model and scaler
model.save("price_action_model.h5")
import joblib
joblib.dump(scaler, "scaler.pkl")
print("✅ Model and scaler saved.")
