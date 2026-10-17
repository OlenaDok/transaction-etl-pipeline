import pandas as pd
from pathlib import Path


def extract_csv(filepath: str) -> pd.DataFrame:
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {filepath}. Please, check filepath.")
    return pd.read_csv(path)


def extract_all(data_dir: str) -> dict:
    base_path = Path(data_dir)

    return {
        "transactions": extract_csv(base_path / "transactions.csv"),
        "status_ref": extract_csv(base_path / "status_ref.csv"),
        "currency_ref": extract_csv(base_path / "currency_ref.csv"),
    }


if __name__ == "__main__":
    # df = extract("data/raw/transact_01022026.csv")

    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE_PATH = BASE_DIR / "data" / "raw"

    dict_df = extract_all(FILE_PATH)

    print(len(dict_df))
