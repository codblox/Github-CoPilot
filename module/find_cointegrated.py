from get_all_tickers import compare_symbols
from fetch_data import FetchData, get_time_period
from constants import INTERVAL, TIME_PERIOD
from cointegration_check import CointegrationCheck
import os

tradable_symbols = compare_symbols(100)

# Get data for all tradable symbols using FetchData and store it in a dictionary
def get_data(tradable_symbols):
    data = {}
    for i in range(len(tradable_symbols)):
        try:
            symbol = tradable_symbols['symbol'][i]
            symbol += 'USDT'
            data[symbol] = FetchData(symbol, INTERVAL)
            print(f'Fetched data for {symbol}')
        except Exception as e:
            print(f'Error in fetching data for {symbol} : {e}')
            continue
    return data

# For each pair of symbols, check if they are cointegrated
def check_cointegration(data):
    for i in range(len(tradable_symbols)):
        for j in range(i+1, len(tradable_symbols)):
            base_crypto = tradable_symbols['symbol'][i]
            quote_crypto = tradable_symbols['symbol'][j]
            base_crypto += 'USDT'
            quote_crypto += 'USDT'
            CointegrationCheck(data[base_crypto], data[quote_crypto], base_crypto, quote_crypto)

#Check if cointegrated_pairs.csv exists. If it does, delete it.
if os.path.isfile('cointegrated_pairs.csv'):
    os.remove('cointegrated_pairs.csv')

check_cointegration(get_data(tradable_symbols))