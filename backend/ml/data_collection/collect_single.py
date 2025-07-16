# backend/ml/data_collection/collect_single.py

from .collect_multiple import fetch_and_save

def collect_single_stock(symbol: str, years: int = 4, interval: str = "day", output_dir: str = "data"):
    return fetch_and_save(symbol, years, interval, output_dir)
