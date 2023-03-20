from module.get_current_data import *
from module.send_message import send_message
import pandas as pd
from module.open_trades import *
from module.close_trades import *

if __name__ == "__main__":
    ticker1 = input("Enter the base crypto: ")
    ticker2 = input("Enter the quote crypto: ")
    
    ticker1.upper()
    ticker2.upper()

    trade_type = input("Enter 'open' or 'close': ")
    trade_type.lower()
    if trade_type == 'open':
        flag = 1
    elif trade_type == 'close':
        flag = 0
    else:
        print("Enter either 'open' or 'close'")

    if flag == 1:
        amount = int(input("Enter the trade amount: "))
        print("Opening trade for {} and {}".format(ticker1, ticker2))
        open_trade(ticker1, ticker2, trade_amount=amount)
        send_message("Trade opened for {} and {}".format(ticker1, ticker2))
    elif flag == 0:
        print("Closing trade for {} and {}".format(ticker1, ticker2))
        closing_trade(ticker1, ticker2)
        send_message("Trade closed for {} and {}".format(ticker1, ticker2))
