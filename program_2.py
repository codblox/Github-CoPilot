#Import libraries
import pandas as pd
import time
from module.zscore_checker import z_score_current, spread_current
import warnings
from module.send_message import send_message
import os

warnings.filterwarnings('ignore')

#Load cointegrated pairs
cointegrated_pairs = pd.read_csv('cointegrated_pairs.csv')

#Function to check each pair of symbols from cointegrated_pairs.csv for current zscore indefinitely and alert if zscore is greater than 3 or less than -3
# Create a zscore.csv file to store the zscore of each pair with zscore greater than 3 or less than -3 with the current time. If the pair already exists in the csv, check if the current time is more than 1 hour of the time_stored. If yes, check the zscore again. If zscore is still greater than 3 or less than -3, update the zscore and current time. If no, delete the pair from the csv
def zscore_checker():
    while True:
        try:
            for i in range(len(cointegrated_pairs)):
                base_crypto = cointegrated_pairs['base_symbol'][i]
                quote_crypto = cointegrated_pairs['quote_symbol'][i]
                hedge_ratio = cointegrated_pairs['hedge_ratio'][i]
                ten_percentile = cointegrated_pairs['10th percentile'][i]
                ninty_percentile = cointegrated_pairs['90th percentile'][i]
                window = cointegrated_pairs['window'][i]
                zscore_current = round(z_score_current(base_crypto, quote_crypto, hedge_ratio, window),2)
                spread = spread_current(base_crypto, quote_crypto, hedge_ratio)
                #print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                #Read 'zscore.csv' file and store its data in a dataframe
                if os.path.isfile('zscore.csv'):
                    zscore_temp = pd.read_csv('zscore.csv')
                else:
                    zscore_temp = pd.DataFrame(columns=['base_symbol', 'quote_symbol', 'zscore', 'hedge_ratio', 'window', 'time_stored'])

                # #if current spread is less than 10th percentile or greater than 90th percentile, store the pair, spread and current time in 'spread.csv'
                # if spread < ten_percentile:
                #     print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Spread: {spread} Window : {window} 10th percentile: {ten_percentile}')

                # if spread > ninty_percentile:
                #     print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Spread: {spread} Window : {window} 90th percentile: {ninty_percentile}')

                # Create a csv file to store the zscore of each pair with zscore greater than 3 or less than -3 with the current time
                if (zscore_current > 2 or zscore_current < -2) and (spread > ninty_percentile or spread < ten_percentile):
                    print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                    # Check the csv if the pair already exists. If not, store the pair, zscore and current time. If yes, check if current time is more than 1 hour of the time_stored. If yes, check the zscore again. If zscore is still greater than 3 or less than -3, store the pair, zscore and current time. If no, continue.
                    if os.path.isfile('zscore.csv'):
                        zscore = pd.read_csv('zscore.csv')
                        #Check if the pair already exists in the csv
                        if zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)].empty:
                            #Store the pair, zscore and current time
                            zscore_temp = zscore_temp.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio': hedge_ratio, 'window': window, 'time_stored': time.time()}, ignore_index=True)
                            zscore_temp.to_csv('zscore.csv', index=False)
                            #send_message(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                        else:
                            # Check if current time is more than 1 hour of the time_stored. If yes, store the pair, zscore and current time after removing current pair entry in the csv. If no, continue.
                            if time.time() - zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)]['time_stored'].values[0] > 3600:
                                zscore_temp = zscore_temp[(zscore_temp.base_symbol != base_crypto)&(zscore_temp.quote_symbol != quote_crypto)]
                                zscore_temp = zscore_temp.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio': hedge_ratio, 'window': window, 'time_stored': time.time()}, ignore_index=True)
                                zscore_temp.to_csv('zscore.csv', index=False)
                                #send_message(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                            else:
                                #Check if abs(zscore_current) is more than abs(zscore_stored). If yes, store the pair, zscore and current time after removing current pair entry in the csv. If no, continue.
                                if abs(zscore_current) > abs(zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)]['zscore'].values[0]):
                                    zscore_temp = zscore_temp[(zscore_temp.base_symbol != base_crypto)&(zscore_temp.quote_symbol != quote_crypto)]
                                    zscore_temp = zscore_temp.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio': hedge_ratio, 'window': window, 'time_stored': time.time()}, ignore_index=True)
                                    zscore_temp.to_csv('zscore.csv', index=False)
                                    #send_message(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore Updated: {zscore_current} Window : {window} ')

                    else:
                        #Store the pair, zscore and current time
                        zscore_temp = zscore_temp.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio': hedge_ratio, 'window': window, 'time_stored': time.time()}, ignore_index=True)
                        zscore_temp.to_csv('zscore.csv', index=False)
                        #send_message(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                if zscore_current > 2.5 or zscore_current < -2.5:
                    print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} [NOT CONSIDERING SPREAD]')

                else:
                    #Check if the pair already exists in the csv. If yes, remove the pair from the csv. If no, continue.
                    if os.path.isfile('zscore.csv'):
                        zscore = pd.read_csv('zscore.csv')
                        if zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)].empty:
                            continue
                        else:
                            #Find the row containing both base_symbol and quote_symbol and remove it from the csv. There can be rows containing only base_symbol or quote_symbol. Do not remove those rows.
                            zscore_temp = zscore_temp[(zscore_temp.base_symbol != base_crypto) & (zscore_temp.quote_symbol != quote_crypto)]
                            zscore_temp.to_csv('zscore.csv', index=False)
                    else:
                        continue
            print("<--------------------------------------------->")
            time.sleep(300)
            print("\n\n\n\n<--------------------------------------------->")
                
        except Exception as e:
            print('Error in zscore_checker' , e)
            continue
                                
zscore_checker()