import pandas as pd
from typing import List, Dict, Any


def normalize_json(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Normalize nested JSON into a flat DataFrame.
    """
    df = pd.json_normalize(data)
    return df


def transform_crypto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations to the cryptocurrency DataFrame.
    """
    df = df.copy()  # Avoid modifying original data

    # Clean column names (remove quotes.USD. prefix that comes after normalization)
    df.columns = df.columns.str.replace("quotes.USD.", "", regex=False)

    # Clean datetime columns
    datetime_cols = ["first_data_at", "last_updated", "ath_date"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], utc=True, errors='coerce')

    # Round numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if col in ["price", "ath_price", "beta_value", "volume_24h", "market_cap"]:
            df[col] = df[col].round(4)
        elif col in ["percent_change_1h", "percent_change_24h", "percent_change_7d"]:
            df[col] = df[col].round(2)
  

    print(f"Transformed DataFrame shape: {df.shape}")
    return df