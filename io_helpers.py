# -*- coding: utf-8 -*-
import pandas as pd

def read_any(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".parquet"):
        try:
            return pd.read_parquet(path)
        except Exception:
            return pd.read_csv(path.replace(".parquet",".csv"))
    else:
        return pd.read_csv(path)

def save_any(df, path):
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    elif path.endswith(".parquet"):
        try:
            df.to_parquet(path, index=False)
        except Exception:
            df.to_csv(path.replace(".parquet",".csv"), index=False)
    else:
        df.to_csv(path+".csv", index=False)
