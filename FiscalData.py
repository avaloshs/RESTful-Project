# FiscalData

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


api_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"
data = fetch_data_from_api(api_url)

if data:
    df = pd.DataFrame(data["data"])

    # Selecting only required columns
    df = df[["country", "currency", "exchange_rate"]]

    print(df)
else:
    print("Failed to fetch data from API.")
