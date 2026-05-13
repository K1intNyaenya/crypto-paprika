import requests
import json

url = "https://api.coinpaprika.com/v1/tickers"
response = requests.get(url)

raw_data = response.json()

# function to extract the data and save it in a json file in the same folder
def extract_crypto(raw_data):
    with open("crypto_data.json", "w") as f:
        json.dump(raw_data, f, indent=4)
extract_crypto(raw_data)

    