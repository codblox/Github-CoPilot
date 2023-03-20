from module.get_current_data import *
import pandas as pd

def closing_trade(ticker1, ticker2):

    side = input("Enter the side of the trade to be closed (long/short): ")

    multiple_trades = 0 # Variable to check if multiple trades are open for the pair or not
    #Check if multiple trades are open for the pair or not
    try:
        open_trades = pd.read_csv('opened_trades.csv')
        multiple_trades = open_trades[(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].shape[0]
    except:
        pass
    print("Number of trades open for the pair: ", multiple_trades)
    # If one trade is open for the pair, close it
    if multiple_trades == 1:
        # Get the current price of the pair
        price_ticker_1 = get_current_price(ticker1)
        price_ticker_2 = get_current_price(ticker2)

        # Get prices at which trade was opened for each ticker (multiple trades can be there for base_symbol and quote_symbol. So, we need to get the price at which the trade was opened for the pair)
        open_price_ticker_1 = open_trades['base_price'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].values[0]
        open_price_ticker_2 = open_trades['quote_price'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].values[0]

        # Get the order quantity for each ticker(multiple trades can be there for base_symbol and quote_symbol. So, we need to get the price at which the trade was opened for the pair)
        order_quantity_ticker_1 = open_trades['base_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].values[0]
        order_quantity_ticker_2 = open_trades['quote_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].values[0]

        if side == 'long':
            profit_ticker_1 = (price_ticker_1 - open_price_ticker_1)*order_quantity_ticker_1
            profit_ticker_2 = (open_price_ticker_2 - price_ticker_2)*order_quantity_ticker_2*-1
        elif side == 'short':
            profit_ticker_1 = (open_price_ticker_1 - price_ticker_1)*order_quantity_ticker_1*-1
            profit_ticker_2 = (price_ticker_2 - open_price_ticker_2)*order_quantity_ticker_2

        # Calculate the total profit/loss
        total_profit = profit_ticker_1 + profit_ticker_2

        # Store the data in a dataframe (store the profit/loss in percentage as well as absolute value. also store opening and closing prices)
        closed_trade = pd.DataFrame({'base_symbol': [ticker1], 'quote_symbol': [ticker2], 'base_price': [(price_ticker_1)], 'quote_price': [(price_ticker_2)], 'base_quantity': [round(order_quantity_ticker_1,3)], 'quote_quantity': [round(order_quantity_ticker_2,3)], 'base_profit': [round(profit_ticker_1,2)], 'quote_profit': [round(profit_ticker_2,2)], 'total_profit': [round(total_profit,2)], 'base_profit_percent': [round(profit_ticker_1*100/(order_quantity_ticker_1*open_price_ticker_1),2)], 'quote_profit_percent': [round(profit_ticker_2*100/(order_quantity_ticker_2*open_price_ticker_2))], 'total_profit_percent': [round(total_profit*100/((order_quantity_ticker_1*open_price_ticker_1)+(order_quantity_ticker_2*open_price_ticker_2)),2)], 'base_open_price': [(open_price_ticker_1)], 'quote_open_price': [(open_price_ticker_2)]})
        
        # Append the data to the closed_trades.csv file
        try:
            closed_trades = pd.read_csv('closed_trades.csv')
            closed_trades = closed_trades.append(closed_trade)
            closed_trades.to_csv('closed_trades.csv', index = False)
        except:
            closed_trade.to_csv('closed_trades.csv', index = False)

        # Delete the trade from the opened_trades.csv file
        open_trades = open_trades[(open_trades['base_symbol'] != ticker1) & (open_trades['quote_symbol'] != ticker2)]
        open_trades.to_csv('opened_trades.csv', index = False)

    elif multiple_trades > 1:
        # Calculate total quantity of the pair (each ticker individually)(multiple trades can be there for base_symbol and quote_symbol. So, we need to get the price at which the trade was opened for the pair)
        total_quantity_ticker_1 = open_trades['base_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].sum()
        total_quantity_ticker_2 = open_trades['quote_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].sum()

        #Calculate average opening price for each ticker using the quantity for each ticker (multiple trades can be there for base_symbol and quote_symbol. So, we need to get the price at which the trade was opened for the pair)
        open_price_ticker_1 = (open_trades['base_price'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)]*open_trades['base_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)]).sum()/total_quantity_ticker_1
        open_price_ticker_2 = (open_trades['quote_price'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)]*open_trades['quote_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)]).sum()/total_quantity_ticker_2

        # Get the current price of the pair
        price_ticker_1 = get_current_price(ticker1)
        price_ticker_2 = get_current_price(ticker2)

        # Ask the user how much % of the trade he wants to close
        percent_trade = float(input('Enter the % of the trade you want to close: '))
        percent_trade = percent_trade/100

        # Calculate the quantity to be sold for each ticker
        total_quantity_ticker_1 = total_quantity_ticker_1*percent_trade
        total_quantity_ticker_2 = total_quantity_ticker_2*percent_trade

        # Calculate the profit/loss for each ticker
        profit_ticker_1 = (price_ticker_1 - open_price_ticker_1)*total_quantity_ticker_1
        profit_ticker_2 = (price_ticker_2 - open_price_ticker_2)*total_quantity_ticker_2

        # Calculate the total profit/loss
        total_profit = profit_ticker_1 + profit_ticker_2

        # Store the data in a dataframe (store the profit/loss in percentage as well as absolute value. also store opening and closing prices)
        closed_trade = pd.DataFrame({'base_symbol': [ticker1], 'quote_symbol': [ticker2], 'base_price': [(price_ticker_1)], 'quote_price': [(price_ticker_2)], 'base_quantity': [round(total_quantity_ticker_1,3)], 'quote_quantity': [round(total_quantity_ticker_2,3)], 'base_profit': [round(profit_ticker_1,2)], 'quote_profit': [round(profit_ticker_2,2)], 'total_profit': [round(total_profit,2)], 'base_profit_percent': [round(profit_ticker_1*100/(total_quantity_ticker_1*open_price_ticker_1),2)], 'quote_profit_percent': [round(profit_ticker_2*100/(total_quantity_ticker_2*open_price_ticker_2))], 'total_profit_percent': [round(total_profit*100/((total_quantity_ticker_1*open_price_ticker_1)+(total_quantity_ticker_2*open_price_ticker_2)),2)], 'base_open_price': [(open_price_ticker_1)], 'quote_open_price': [(open_price_ticker_2)]})

        # Append the data to the closed_trades.csv file
        try:
            closed_trades = pd.read_csv('closed_trades.csv')
            closed_trades = closed_trades.append(closed_trade)
            closed_trades.to_csv('closed_trades.csv', index = False)
        except:
            closed_trade.to_csv('closed_trades.csv', index = False)

        # Calculate remaining quantity of the pair, each ticker individually
        remaining_quantity_ticker_1 = open_trades['base_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].sum() - total_quantity_ticker_1
        remaining_quantity_ticker_2 = open_trades['quote_quantity'][(open_trades['base_symbol'] == ticker1) & (open_trades['quote_symbol'] == ticker2)].sum() - total_quantity_ticker_2

        #If the remaining quantity is 0, delete the trade from the opened_trades.csv file
        if remaining_quantity_ticker_1 == 0 and remaining_quantity_ticker_2 == 0:
            open_trades = open_trades[(open_trades['base_symbol'] != ticker1) & (open_trades['quote_symbol'] != ticker2)]
            open_trades.to_csv('opened_trades.csv', index = False)
        
        #If the remaining quantity is not 0, delete all the trades for the pair from the opened_trades.csv file and add a new trade with the remaining quantity and price
        else:
            open_trades = open_trades[(open_trades['base_symbol'] != ticker1) & (open_trades['quote_symbol'] != ticker2)]
            open_trades.to_csv('opened_trades.csv', index = False)
            open_trade = pd.DataFrame({'base_symbol': [ticker1], 'quote_symbol': [ticker2], 'base_price': [round(price_ticker_1,3)], 'quote_price': [round(price_ticker_2,3)], 'base_quantity': [round(remaining_quantity_ticker_1,3)], 'quote_quantity': [round(remaining_quantity_ticker_2,3)]})
            try:
                open_trades = pd.read_csv('opened_trades.csv')
                open_trades = open_trades.append(open_trade)
                open_trades.to_csv('opened_trades.csv', index = False)
            except:
                open_trade.to_csv('opened_trades.csv', index = False)




    