# backend/route/ml_routes.py
from fastapi import APIRouter, Query, HTTPException, UploadFile, File
from ml.data_collection import collect_single_stock, fetch_batch
from ml.data_preprocess.prepare_ml_dataset import process_stock, process_all
from ml.data_preprocess.merge_and_encode import merge_and_encode
from ml.predict.predict_model import predict_stock
from ml.train.train_model import train_model
import os
import json

router = APIRouter()

@router.get("/fetch_single")
def fetch_single(symbol: str, years: int = 4, interval: str = "day", output_dir: str = "raw_stock_data"):
    try:
        success = collect_single_stock(symbol, years, interval, output_dir)
        if success:
            return {"message": f"Fetched and saved data for {symbol}"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch {symbol}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch_batch")
def fetch_batch_route(years: int = 4, interval: str = "day", output_dir: str = "raw_stock_data"):
    try:
        result = fetch_batch(years=years, interval=interval, output_dir=output_dir)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocess_stock")
def preprocess_stock(symbol: str, data_dir: str = "raw_stock_data", output_dir: str = "processed_stock_dataset"):
    try:
        file_path = f"{data_dir}/{symbol}.csv"
        df = process_stock(file_path, output_dir)
        return {"message": f"Processed {symbol} with {len(df)} rows."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocess_all")
def preprocess_all_route(input_dir: str = "raw_stock_data", output_dir: str = "processed_stock_dataset"):
    try:
        process_all(input_dir, output_dir)
        return {"message": f"Processed all files in {input_dir} to {output_dir}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/merge_encode")
def merge_encode_route(input_dir: str = "processed_stock_dataset", output_dir: str = "combined_dataset", output_file: str = "train_dataset.csv"):
    try:
        path, count = merge_and_encode(input_dir, output_dir, output_file)
        return {"message": f"Merged dataset with {count} rows.", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/train_multi")
def train_multi_route(
    input_csv: str = "combined_dataset/train_dataset.csv",
    test_ratio: float = 0.2,
    epochs: int = 30,
    batch_size: int = 32,
    save_dir: str = "ml/models/global"
):
    try:
        result = train_model(
            input_csv=input_csv,
            test_ratio=test_ratio,
            epochs=epochs,
            batch_size=batch_size,
            save_dir=save_dir
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/train_single")
def train_single_route(
    symbol: str,
    test_ratio: float = 0.2,
    epochs: int = 30,
    batch_size: int = 32,
    data_dir: str = "processed_stock_dataset"
):
    try:
        input_csv = os.path.join(data_dir, f"{symbol}.csv")
        save_dir = os.path.join("ml", "models", symbol.upper())
        result = train_model(
            input_csv=input_csv,
            test_ratio=test_ratio,
            epochs=epochs,
            batch_size=batch_size,
            save_dir=save_dir
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
def list_models(base_dir: str = "ml/models"):
    try:
        models = []
        for model_name in os.listdir(base_dir):
            model_path = os.path.join(base_dir, model_name)
            metadata_file = os.path.join(model_path, "metadata.json")
            if os.path.isdir(model_path) and os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    metadata["name"] = model_name
                    models.append(metadata)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ml/predict")
def predict_route(
    symbol: str = Query(default=None),
    model_name: str = Query(default="global"),
    file: UploadFile = File(default=None),
    top_n_rows: int = Query(default=30)
):
    try:
        result = predict_stock(symbol=symbol, model_name=model_name, csv_file=file, top_n_rows=top_n_rows)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))