import pandas as pd
from pathlib import Path
from extract import extract_all


def transform(transactions: pd.DataFrame, status_ref: pd.DataFrame, currency_ref: pd.DataFrame) -> pd.DataFrame:
    df = transactions.merge(status_ref, on="status_code", how="left")
    df = transactions.merge(currency_ref, on="currency_code", how="left")

    return df


if __name__ == "__main__":
    # df = extract("data/raw/transact_01022026.csv")

    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE_PATH = BASE_DIR / "data" / "raw"

    dict_df = extract_all(FILE_PATH)

    df = transform(dict_df['transactions'],
                   dict_df['status_ref'], dict_df['currency_ref'])
    print(df.head())
