# --- merge_and_encode.py ---
import os
import pandas as pd

INPUT_DIR = "ml_data"

OUTPUT_DIR = "dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = "train_dataset.csv"

all_dfs = []

for file in os.listdir(INPUT_DIR):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(INPUT_DIR, file))
        all_dfs.append(df)

# Merge all into one
full_df = pd.concat(all_dfs, ignore_index=True)

# Encode symbol column categorically
symbols = sorted(full_df["symbol"].unique())
symbol_map = {sym: idx for idx, sym in enumerate(symbols)}
full_df["symbol_encoded"] = full_df["symbol"].map(symbol_map)

# Save merged dataset
full_df.to_csv(f"{OUTPUT_DIR}/{OUTPUT_FILE}", index=False)

print(f"✅ Merged dataset saved as {OUTPUT_DIR}/{OUTPUT_FILE} with {len(full_df)} rows.")