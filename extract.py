import requests
import json
from typing import List, Dict, Any


def fetch_crypto_data() -> List[Dict[str, Any]]:
    """
    Extract cryptocurrency data from CoinPaprika API.
    """
    url = "https://api.coinpaprika.com/v1/tickers"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() 
        
        raw_data = response.json()
        
        # Save raw data for auditing/debugging
        with open("crypto_data.json", "w") as f:
            json.dump(raw_data, f, indent=4)
        
        print(f"Successfully extracted {len(raw_data)} records from CoinPaprika API.")
        return raw_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise