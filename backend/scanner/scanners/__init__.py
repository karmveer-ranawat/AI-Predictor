# backend/scanner/scanners/__init__.py
from .ma44 import run_ma44_scanner
from .fib import run_fib_scanner
from .rsi import run_rsi_scanner
import pandas as pd

# Full list of symbols
SYMBOLS = [
    "RELIANCE", "TCS", "INFY", "SBIN", "TATAMOTORS", "TATASTEEL", "IRFC", "IRCTC",
    "ITC", "IOC", "BATAINDIA", "RAYMOND", "TITAN", "TRIDENT", "PNB", "BHARATWIRE",
    "HIGHENE", "HINDUNILVR", "PAYTM", "TATATECH", "IREDA", "ONGC", "HDFCBANK", "LT",
    "NHPC", "UCOBANK", "SUZLON", "YESBANK", "TATAPOWER", "INDHOTEL", "RVNL", "HAL",
    "BEL", "ETERNAL", "GAIL", "ADANIPOWER", "ADANIENT", "BAJAJHFL", "AXISBANK",
    "SWIGGY", "AETHER"
]

def run_all_scanners_on_all():
    results = {}

    df_ma = run_ma44_scanner(SYMBOLS)
    df_fib = run_fib_scanner(SYMBOLS)
    df_rsi = run_rsi_scanner(SYMBOLS)

    for sym in SYMBOLS:
        results[sym] = {
            "44ma": not df_ma.empty and sym in df_ma["Symbol"].values,
            "fib": not df_fib.empty and sym in df_fib["Symbol"].values,
            "rsi": not df_rsi.empty and sym in df_rsi["Symbol"].values
        }

    return results


def run_all_scanners_on_stock(symbol):
    result = {}
    df1 = run_ma44_scanner([symbol])
    df2 = run_fib_scanner([symbol])
    df3 = run_rsi_scanner([symbol])

    result[symbol] = {
        "44ma": not df1.empty and symbol in df1["Symbol"].values,
        "fib": not df2.empty and symbol in df2["Symbol"].values,
        "rsi": not df3.empty and symbol in df3["Symbol"].values
    }
    return result


def run_single_scan_all(scan_type):
    if scan_type == "44ma":
        df = run_ma44_scanner(SYMBOLS)
        return {row["Symbol"]: {"44ma": True} for _, row in df.iterrows()}
    elif scan_type == "fib":
        df = run_fib_scanner(SYMBOLS)
        return {row["Symbol"]: {"fib": True} for _, row in df.iterrows()}
    elif scan_type == "rsi":
        df = run_rsi_scanner(SYMBOLS)
        return {row["Symbol"]: {"rsi": True} for _, row in df.iterrows()}
    else:
        raise ValueError(f"Invalid scan type: {scan_type}")


def run_single_scan_on_stock(scan_type, symbol):
    symbol = symbol.upper()
    if scan_type == "44ma":
        df = run_ma44_scanner([symbol])
        matched = not df.empty and symbol in df["Symbol"].values
        return {symbol: {"44ma": matched}}

    elif scan_type == "fib":
        df = run_fib_scanner([symbol])
        matched = not df.empty and symbol in df["Symbol"].values
        return {symbol: {"fib": matched}}

    elif scan_type == "rsi":
        df = run_rsi_scanner([symbol])
        matched = not df.empty and symbol in df["Symbol"].values
        return {symbol: {"rsi": matched}}

    else:
        raise ValueError(f"Invalid scan type: {scan_type}")

def run_scan_on_all_nse(scan_type):
    df = pd.read_csv("data/instruments_nse.csv")
    df = df[(df["instrument_type"] == "EQ") & (df["exchange"] == "NSE")]
    all_symbols = df["tradingsymbol"].unique().tolist()

    if scan_type == "44ma":
        df = run_ma44_scanner(all_symbols)
        return {row["Symbol"]: {"44ma": True} for _, row in df.iterrows()}
    elif scan_type == "fib":
        df = run_fib_scanner(all_symbols)
        return {row["Symbol"]: {"fib": True} for _, row in df.iterrows()}
    elif scan_type == "rsi":
        df = run_rsi_scanner(all_symbols)
        return {row["Symbol"]: {"rsi": True} for _, row in df.iterrows()}
    else:
        raise ValueError(f"Invalid scan type: {scan_type}")