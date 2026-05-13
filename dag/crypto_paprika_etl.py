from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
from extract import fetch_crypto_data
from transform import normalize_json, transform_crypto
from load import load_to_db


default_args = {
    "owner": "clinton",
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
    "email_on_failure": False,  
}


@dag(
    dag_id="crypto_etl_pipeline",
    default_args=default_args,
    description="Daily Crypto ETL Pipeline using CoinPaprika API",
    start_date=days_ago(1),
    schedule="@daily",     
    catchup=False,
    max_active_runs=1,
    tags=["etl", "crypto", "postgres", "api"],
    doc_md=__doc__
)
def crypto_etl_pipeline():

    @task
    def extract():
        """Extract raw data from API"""
        return fetch_crypto_data()

    @task
    def transform(raw_data):
        """Transform and clean the data"""
        df = normalize_json(raw_data)
        transformed_df = transform_crypto(df)
        return transformed_df

    @task
    def load(transformed_df: pd.DataFrame):
        """Load data into PostgreSQL"""
        load_to_db(transformed_df, table_name="crypto_paprika")
        return "Load completed successfully"

    # Define pipeline flow
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)


# Instantiate the DAG
crypto_etl_pipeline()