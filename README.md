# crypto-paprika

A daily ETL pipeline that extracts cryptocurrency data from the CoinPaprika API, transforms and cleans the data, and loads it into a PostgreSQL database.

## Overview

This project implements a data engineering pipeline using Apache Airflow to orchestrate the Extract-Transform-Load (ETL) process for cryptocurrency market data. The pipeline runs daily and fetches the latest cryptocurrency information including pricing, market capitalization, and historical data.

## Architecture

The pipeline consists of three main components:

```
CoinPaprika API → Extract → Transform → Load → PostgreSQL
```

### Pipeline Flow

1. **Extract** (`extract.py`): Fetches cryptocurrency data from the CoinPaprika API
2. **Transform** (`transform.py`): Normalizes JSON, cleans data, and applies transformations
3. **Load** (`load.py`): Stores processed data in PostgreSQL database

### Orchestration

The DAG (`dag/crypto_paprika_etl.py`) is scheduled to run daily using Apache Airflow with:
- 3 automatic retries on failure
- 3-minute retry delay
- Max 1 concurrent run
- Tags: `etl`, `crypto`, `postgres`, `api`

## Project Structure

```
├── extract.py                   # Data extraction from API
├── transform.py                 # Data transformation and cleaning
├── load.py                       # Database loading logic
├── dag/
│   └── crypto_paprika_etl.py   # Airflow DAG definition
├── crypto_data.json             # Raw API response (for auditing)
└── README.md                    # This file
```

## Components

### Extract (`extract.py`)

- **Function**: `fetch_crypto_data()`
- **Source**: CoinPaprika API (`https://api.coinpaprika.com/v1/tickers`)
- **Output**: List of cryptocurrency records
- **Features**:
  - 30-second timeout
  - Saves raw JSON for auditing
  - Error handling for API failures

### Transform (`transform.py`)

- **Function**: `normalize_json()` - Flattens nested JSON structure
- **Function**: `transform_crypto()` - Applies business logic transformations
- **Transformations**:
  - Removes `quotes.USD.` prefix from column names
  - Converts datetime columns to UTC
  - Rounds numeric values for consistency:
    - Price fields: 4 decimal places
    - Percentage changes: 2 decimal places
  - Datetime columns handled: `first_data_at`, `last_updated`, `ath_date`

### Load (`load.py`)

- **Function**: `load_to_db()`
- **Database**: PostgreSQL
- **Method**: SQLAlchemy via Airflow PostgresHook
- **Target Table**: `crypto_paprika`
- **Features**:
  - Batch processing with 1000-row chunks
  - Replace mode (overwrites existing data)
  - Null/empty DataFrame validation

## Requirements

### Dependencies

- `requests` - API communication
- `pandas` - Data manipulation
- `sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment configuration
- `apache-airflow` - Workflow orchestration
- `apache-airflow-providers-postgres` - PostgreSQL provider

### Python Version

- Python 3.10+

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv cryptoenv
source cryptoenv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file with your PostgreSQL credentials:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
```

### 4. Configure Airflow

Set up your Airflow PostgreSQL connection in the Airflow UI or via environment variables:

```bash
export AIRFLOW_CONN_POSTGRESQL+PSYCOPG2__HOST=your_host
export AIRFLOW_CONN_POSTGRESQL+PSYCOPG2__LOGIN=your_username
export AIRFLOW_CONN_POSTGRESQL+PSYCOPG2__PASSWORD=your_password
export AIRFLOW_CONN_POSTGRESQL+PSYCOPG2__SCHEMA=your_database
export AIRFLOW_CONN_POSTGRESQL+PSYCOPG2__PORT=5432
```

## Usage

### Running the ETL Manually

```bash
# Extract data
python -c "from extract import fetch_crypto_data; fetch_crypto_data()"

# Transform
python -c "from transform import normalize_json, transform_crypto; import json; data = json.load(open('crypto_data.json')); df = transform_crypto(normalize_json(data)); print(df.head())"

# Load
python -c "from load import load_to_db; from transform import normalize_json, transform_crypto; import json; data = json.load(open('crypto_data.json')); df = transform_crypto(normalize_json(data)); load_to_db(df)"
```

### Running via Airflow

```bash
# Start Airflow webserver
airflow webserver --port 8080

# In another terminal, start the scheduler
airflow scheduler
```

Access the Airflow UI at `http://localhost:8080` and trigger the `crypto_etl_pipeline` DAG.

## Database Schema

The `crypto_paprika` table contains the following columns (sample):
- `id`: Cryptocurrency identifier
- `name`: Cryptocurrency name
- `symbol`: Trading symbol
- `rank`: Market rank
- `price`: Current price in USD
- `volume_24h`: 24-hour trading volume
- `market_cap`: Market capitalization
- `percent_change_1h`, `percent_change_24h`, `percent_change_7d`: Price changes
- `ath_price`: All-time high price
- `ath_date`: Date of all-time high
- `first_data_at`, `last_updated`: Timestamps

## Error Handling

- **Extract**: API errors trigger task failure with retry
- **Transform**: Coerces invalid datetime values to NaT
- **Load**: Validates non-empty DataFrame before loading; empty DataFrames are skipped with warning

## Output

- Raw API data: `crypto_data.json`
- Console logs: Task execution progress
- Database: Final transformed data in PostgreSQL

## Notes

- The pipeline uses **replace mode** for the database load, meaning existing data is overwritten on each run
- Runs once daily at midnight UTC
- Maximum 1 concurrent run to avoid conflicts
- 3 automatic retries with 3-minute delays on failure
