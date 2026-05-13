import pandas as pd
import json


# normalize the json data
def normalize_json(data):
    df = pd.json_normalize(data)
    return df


# transform the normalized json df
def transform_crypto(df):

    # removing "quotes.USD." from column names after normalization
    df.columns = df.columns.str.replace("quotes.USD.", "", regex=False)

    # convert datetime columns
    df["first_data_at"] = pd.to_datetime(df["first_data_at"])
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["ath_date"] = pd.to_datetime(df["ath_date"])

    # round numeric columns
    df["price"] = df["price"].round(2)
    df["ath_price"] = df["ath_price"].round(2)
    df["beta_value"] = df["beta_value"].round(2)

    return df