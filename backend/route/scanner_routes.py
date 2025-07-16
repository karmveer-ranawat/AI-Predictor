# backend/route/scanner_routes.py
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from scanner.instrument_lookup import download_instruments
from scanner.scanners import (
    run_all_scanners_on_all,
    run_all_scanners_on_stock,
    run_single_scan_all,
    run_scan_on_all_nse,
    run_single_scan_on_stock
)

router = APIRouter()

@router.get("/get_all_instruments")
def download_all():
    try:
        download_instruments()
        return {"message": "Downloaded instrument data for all stocks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all_symbols")
def get_all_symbols():
    try:
        df = pd.read_csv("data/instruments_nse.csv")
        df_eq = df[
            (df["instrument_type"] == "EQ") &
            (df["segment"] == "NSE") &
            (df["exchange"] == "NSE")
        ]
        symbols = df_eq["tradingsymbol"].unique().tolist()
        return {"symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan_all")
def scan_all():
    try:
        run_all_scanners_on_all()
        return {"message": "Ran all scanners on all stocks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan_stock/{symbol}")
def scan_stock(symbol: str):
    try:
        result = run_all_scanners_on_stock(symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan_type_all/{scan_type}")
def scan_type_all(scan_type: str):
    try:
        df = run_single_scan_all(scan_type.lower())
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/run_scan_on_all_nse/{scan_type}")
def run_nse_scan(scan_type: str):  # Renamed to avoid conflict
    try:
        df = run_scan_on_all_nse(scan_type.lower())  # this calls the imported function
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan_type_stock/{scan_type}/{symbol}")
def scan_type_stock(scan_type: str, symbol: str):
    try:
        df = run_single_scan_on_stock(scan_type.lower(), symbol.upper())
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{symbol}")
def get_summary(symbol: str):
    symbol = symbol.upper()
    summary = {}

    try:
        df_44 = pd.read_csv("scanner/output/scan_results.csv")
        summary["44ma"] = symbol in df_44["Symbol"].values
    except:
        summary["44ma"] = False

    try:
        df_fib = pd.read_csv("scanner/output/fib_scan_results.csv")
        summary["fib"] = symbol in df_fib["Symbol"].values
    except:
        summary["fib"] = False

    try:
        df_rsi = pd.read_csv("scanner/output/rsi_scan_results.csv")
        summary["rsi"] = symbol in df_rsi["Symbol"].values
    except:
        summary["rsi"] = False

    return {"symbol": symbol, "summary": summary}
