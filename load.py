import pandas as pd
import psycopg2
from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Optional
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONN_ID = "postgresql+psycopg2://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME?sslmode=require"


def load_to_db(df: pd.DataFrame, crypto_paprika: str = "crypto_paprika") -> None:
    """
    Load transformed DataFrame into PostgreSQL using Airflow PostgresHook.
    """
    if df.empty:
        print("Warning: DataFrame is empty. Skipping load.")
        return

    try:
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        engine = hook.get_sqlalchemy_engine()

        df.to_sql(
            name=crypto_paprika,
            con=engine,
            if_exists='replace', 
            index=False,
            method='multi',
            chunksize=1000
        )

        print(f"Successfully loaded {len(df)} records into table '{crypto_paprika}'.")

    except Exception as e:
        print(f"Error loading data to database: {e}")
        raise