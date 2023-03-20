import os
from binance.client import Client

# set up the Binance client with your API keys
api_key = '6ebefa6d3b0fadffc55339311359bb1e03495c807facee5c9de6819cccca8e34'
api_secret = 'cb5add686c01c8e66079175e444d60cf816df18d2a063a4834cabcfe9005b551'
client = Client(api_key, api_secret)

# Function to get current price of a crypto
def get_current_price(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    return float(price['price'])

# Function to get position size of both base and quote crypto
def get_position_size(hedge_ratio, base_crypto, quote_crypto, trade_amount):
    base_price = get_current_price(base_crypto)
    quote_price = get_current_price(quote_crypto)

    #Calculate the spread
    spread = base_price - hedge_ratio*quote_price
    print(trade_amount)
    base_size = trade_amount/(base_price+(hedge_ratio*quote_price))
    quote_size = base_size*hedge_ratio

    return base_price*base_size, quote_price*quote_size
