import pandas as pd
from sqlalchemy import create_engine
from transform import transform_crypto, normalize_json
import os
from dotenv import load_dotenv

av_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"
engine = create_engine(av_url)

def load_to_db(df, crypto_paprika):
    df.to_sql(crypto_paprika, 
              engine, 
              if_exists='replace', 
              index=False)
    
    print(f"Data loaded to {crypto_paprika} table in the database.")

