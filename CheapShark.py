# CheapShark

import pandas as pd
import requests

BASE = "http://127.0.0.1:5000/"
APP_VERSION = "v1/"


def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


api_url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15"
data = fetch_data_from_api(api_url)
if data:
    df = pd.DataFrame(data)

    # Selecting only required columns
    df = df[["gameID", "salePrice"]]

    print(df)
else:
    print("Failed to fetch data from API.")
