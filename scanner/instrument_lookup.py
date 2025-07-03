import os
import pandas as pd
from scanner.kite_auth import get_kite

INSTRUMENT_FILE = "instruments_nse.csv"

def download_instruments():
    kite = get_kite()
    instruments = kite.instruments("NSE")
    df = pd.DataFrame(instruments)
    df.to_csv(INSTRUMENT_FILE, index=False)
    print(df)
    return df

def get_token(symbol):
    if not os.path.exists(INSTRUMENT_FILE):
        df = download_instruments()
    else:
        df = pd.read_csv(INSTRUMENT_FILE)

    # Ensure proper filtering for actual equity stocks only
    df_eq = df[
        (df["instrument_type"] == "EQ") &
        (df["segment"] == "NSE") &
        (df["exchange"] == "NSE")
    ]

    row = df_eq[df_eq["tradingsymbol"] == symbol.upper()]
    if not row.empty:
        return int(row.iloc[0]["instrument_token"])
    else:
        raise Exception(f"Instrument token not found for {symbol}")