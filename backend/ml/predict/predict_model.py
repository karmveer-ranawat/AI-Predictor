# backend/ml/predict/predict_model.py
import os
import json
import pandas as pd
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from ml.data_preprocess.prepare_ml_dataset import engineer_features, detect_sr_levels

def predict_stock(symbol=None, model_name="global", csv_file=None, top_n_rows=50):
    try:
        # Determine paths
        model_dir = os.path.join("ml", "models", model_name)
        model_path = os.path.join(model_dir, "model.h5")
        scaler_path = os.path.join(model_dir, "scaler.pkl")
        metadata_path = os.path.join(model_dir, "metadata.json")

        # Load model, scaler, metadata
        if not all([os.path.exists(p) for p in [model_path, scaler_path, metadata_path]]):
            raise FileNotFoundError(f"Missing model, scaler, or metadata in {model_dir}")

        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        features = metadata["features_used"]

        # Load and preprocess input
        if csv_file:
            df = pd.read_csv(csv_file)
        elif symbol:
            df_path = os.path.join("processed_stock_dataset", f"{symbol.upper()}.csv")
            if not os.path.exists(df_path):
                raise FileNotFoundError(f"No processed data for {symbol}")
            df = pd.read_csv(df_path)
        else:
            raise ValueError("Either symbol or csv_file must be provided")

        # Use most recent data only
        df = df.tail(top_n_rows)

        # If data is raw, process it
        if "returns_1d" not in df.columns:
            df = engineer_features(df)
            df = detect_sr_levels(df)

        df.dropna(inplace=True)
        feature_df = df[features].copy()

        # Scale and predict
        scaled = scaler.transform(feature_df.values)
        probs = model.predict(scaled).flatten()
        last_prob = float(probs[-1])

        verdict = "BUY" if last_prob > 0.5 else "AVOID"
        confidence = round(last_prob * 100, 2)

        return {
            "symbol": symbol,
            "model_used": model_name,
            "prediction": 1 if last_prob > 0.5 else 0,
            "confidence_percent": confidence,
            "verdict": verdict,
            "recent_chart_data": df.tail(top_n_rows).to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}
