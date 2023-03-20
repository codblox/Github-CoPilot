import pandas as pd
from module.get_current_data import get_current_price
from module.constants import TRADE_AMOUNT

# Program to calculate order amount for each ticker
def get_order_amount(ticker1, ticker2, hedge_ratio, trade_amount = TRADE_AMOUNT):
    # Get the current price of the pair
    price_ticker_1 = get_current_price(ticker1)
    price_ticker_2 = get_current_price(ticker2)
    
    # Calculate the spread
    spread = price_ticker_1 - hedge_ratio*price_ticker_2
    
    # Calculate the order amount for each ticker
    order_amount_ticker_1 = trade_amount/(price_ticker_1+(hedge_ratio*price_ticker_2))
    order_amount_ticker_2 = order_amount_ticker_1*hedge_ratio
    
    return order_amount_ticker_1*price_ticker_1, order_amount_ticker_2*price_ticker_2

# Program to create logs of open trades
def open_trade(ticker1, ticker2, trade_amount = TRADE_AMOUNT):
    # Open cointegrated_pairs.csv and get the hedge ratio and window for the pair
    cointegrated_pairs = pd.read_csv('cointegrated_pairs.csv')
    
    # Get the hedge ratio and window for the pair
    hedge_ratio = cointegrated_pairs.loc[(cointegrated_pairs['base_symbol'] == ticker1) & (cointegrated_pairs['quote_symbol'] == ticker2), 'hedge_ratio'].values[0]
    window = cointegrated_pairs.loc[(cointegrated_pairs['base_symbol'] == ticker1) & (cointegrated_pairs['quote_symbol'] == ticker2), 'window'].values[0]

    # Get the current price of the pair
    price_ticker_1 = get_current_price(ticker1)
    price_ticker_2 = get_current_price(ticker2)

    # Calculate order amount and order quantity for each ticker
    order_amount_ticker_1, order_amount_ticker_2 = get_order_amount(ticker1, ticker2, hedge_ratio)
    print(f"Order amount for {ticker1}: {order_amount_ticker_1}, Order amount for {ticker2}: {order_amount_ticker_2}")
    order_quantity_ticker_1 = order_amount_ticker_1/price_ticker_1
    order_quantity_ticker_2 = order_amount_ticker_2/price_ticker_2

    #Store the data in a dataframe
    opened_trade = pd.DataFrame({'base_symbol': [ticker1], 'quote_symbol': [ticker2], 'hedge_ratio': [hedge_ratio], 'window': [window], 'base_price': [price_ticker_1], 'quote_price': [price_ticker_2], 'base_quantity': [order_quantity_ticker_1], 'quote_quantity': [order_quantity_ticker_2], 'trade_amount': [trade_amount], 'base_amount': [order_amount_ticker_1], 'quote_amount': [order_amount_ticker_2]})
    
    #Check if opened_trades.csv exists. If not, create it. If yes, append the data to it. Sort the data by base_symbol and quote_symbol before saving
    try:
        open_trades = pd.read_csv('opened_trades.csv')
        open_trades = open_trades.append(opened_trade)
        open_trades = open_trades.sort_values(by=['base_symbol', 'quote_symbol'])
        open_trades.to_csv('opened_trades.csv', index=False)
    except:
        opened_trade.to_csv('opened_trades.csv', index=False)
