import requests
import pandas as pd
import time

# Function to fetch data from the Binance API
def FetchData(symbol, interval):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=365'
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df.iloc[:, 0:6]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    return df

# create a function which takes timeperiod (in days) as input and gives start time (which is timeperiod amount of days back from current timestamp) and end time (current time) as output using datetime library
from datetime import datetime, timedelta

def get_time_period(time_period):
    end_time = int(datetime.now().timestamp())
    start_time = int((datetime.now() - timedelta(days=time_period)).timestamp())
    return start_time, end_time




