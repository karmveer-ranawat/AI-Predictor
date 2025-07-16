# backend/ml/data_preprocess/merge_and_encode.py
import os
import pandas as pd

def merge_and_encode(input_dir="processed_stock_dataset", output_dir="combined_dataset", output_file="train_dataset.csv"):
    os.makedirs(output_dir, exist_ok=True)

    all_dfs = []
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(input_dir, file))
            all_dfs.append(df)

    if not all_dfs:
        raise ValueError("No CSV files found to merge.")

    full_df = pd.concat(all_dfs, ignore_index=True)
    symbols = sorted(full_df["symbol"].unique())
    symbol_map = {sym: idx for idx, sym in enumerate(symbols)}
    full_df["symbol_encoded"] = full_df["symbol"].map(symbol_map)

    final_path = os.path.join(output_dir, output_file)
    full_df.to_csv(final_path, index=False)
    print(f"✅ Merged dataset saved to {final_path} with {len(full_df)} rows.")
    return final_path, len(full_df)