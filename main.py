from module.constants import INTERVAL, TIME_PERIOD
from module.cointegration_check import CointegrationCheck
from module.fetch_data import FetchData, get_time_period
import pandas as pd

#main function
if __name__ == '__main__':
    base_crypto = input("Enter the base crypto: ")
    quote_crypto = input("Enter the quote crypto: ")

    time_period = TIME_PERIOD
    interval = INTERVAL
    
    base_data = FetchData(base_crypto, interval)
    quote_data = FetchData(quote_crypto, interval)

    CointegrationCheck(base_data, quote_data,base_crypto,quote_crypto)