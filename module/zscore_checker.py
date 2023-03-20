from module.fetch_data import FetchData
from module.constants import INTERVAL

#Function to check current zscore of the spread from base_crypto, quote_crypto, hedge_ratio and window using current live prices from binance
def z_score_current(base_crypto, quote_crypto, hedge_ratio, window):
    #Get current price of base_crypto and quote_crypto
    base_data = FetchData(base_crypto, INTERVAL)
    quote_data = FetchData(quote_crypto, INTERVAL)

    series_1 = base_data['close'].astype(float)
    series_2 = quote_data['close'].astype(float)

    #Calculate the spread
    spread = series_1 - hedge_ratio*series_2

    #Calculate the zscore
    zscore_current = (spread - spread.rolling(window).mean())/spread.rolling(window).std()

    return zscore_current[-1]

def spread_current(base_crypto, quote_crypto, hedge_ratio):
    #Get current price of base_crypto and quote_crypto
    base_data = FetchData(base_crypto, INTERVAL)
    quote_data = FetchData(quote_crypto, INTERVAL)

    series_1 = base_data['close'].astype(float)
    series_2 = quote_data['close'].astype(float)

    #Calculate the spread
    spread = series_1 - hedge_ratio*series_2

    return spread[-1]
