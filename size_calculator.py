#Program to calculate the dollar size of each position to hedge the spread given the hedge_ratio of the spread

#Import libraries
from module.constants import TRADE_AMOUNT
from module.get_current_data import get_position_size

base_crypto = 'GALAUSDT'
quote_crypto = 'GRTUSDT'



#Function to calculate the dollar size of each position to hedge the spread given the hedge_ratio of the spread
hedge_ratio = 0.612

base_size, quote_size = get_position_size(hedge_ratio, base_crypto, quote_crypto, TRADE_AMOUNT)
print(f'Base size: {base_size} {base_crypto}')
print(f'Quote size: {quote_size} {quote_crypto}')
