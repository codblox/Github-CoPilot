# Program to get all tradable tickers on USDT Perpetual Futures from Binance

# Import libraries
import requests
import pandas as pd

# Function to get all tradable tickers on USDT Perpetual Futures from Binance
def get_all_tickers_binance():
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url).json()
    df = pd.DataFrame(data['symbols'])
    df = df[df['status'] == 'TRADING']
    df = df[df['contractType'] == 'PERPETUAL']
    df = df[df['quoteAsset'] == 'USDT']
    df = df[['symbol']]
    return df


# Function to get top_n tickers from the list of all tickers on Coinmarketcap in order of marketcap
def get_top_n_tickers_coinmarketcap(top_n):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        "start": "1",
        "limit": "1000",
        "convert": "USD",
        "sort": "market_cap",
        "sort_dir": "desc",
        "cryptocurrency_type": "coins",
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "627a97f0-4f7b-4a91-888e-d004152fe265"
    }

    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()
    df = pd.DataFrame(data["data"])
    df_top = df.head(top_n)

    return df_top[['symbol', 'name', 'quote']]


# Compare symbols from Binance and Coinmarketcap and create a dataframe containing symbol, name and quote of those symbols which are present in both Binance and Coinmarketcap
def compare_symbols(top_n):
    df_binance = get_all_tickers_binance()
    #Slice last 4 characters of symbol to remove USDT
    df_binance['symbol'] = df_binance['symbol'].str[:-4]
    df_coinmarketcap = get_top_n_tickers_coinmarketcap(top_n)
    
    # Create a new dataframe containing symbol, name and quote of those symbols which are present in both Binance and Coinmarketcap
    df = pd.merge(df_binance, df_coinmarketcap, on='symbol', how='inner')
    df = df[['symbol', 'name', 'quote']]
    
    return df

