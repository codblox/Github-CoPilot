# Program to check each pair of symbols from cointegrated_pairs.csv for current zscore indefinitely and alert if zscore is greater than 4 or less than -4

#Import libraries
import pandas as pd
import time
from module.zscore_checker import z_score_current
import warnings
from module.send_message import send_message
import os

warnings.filterwarnings('ignore')

#Load cointegrated pairs
cointegrated_pairs = pd.read_csv('cointegrated_pairs.csv')

#Function to check each pair of symbols from cointegrated_pairs.csv for current zscore indefinitely and alert if zscore is greater than 4 or less than -4
def zscore_checker():
    while True:
        try:
            for i in range(len(cointegrated_pairs)):
                base_crypto = cointegrated_pairs['base_symbol'][i]
                quote_crypto = cointegrated_pairs['quote_symbol'][i]
                hedge_ratio = cointegrated_pairs['hedge_ratio'][i]
                window = cointegrated_pairs['window'][i]
                zscore_current = round(z_score_current(base_crypto, quote_crypto, hedge_ratio, window),2)
                #print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')
                #Read 'zscore.csv' file and store its data in a dataframe
                if os.path.isfile('zscore.csv'):
                    zscore_temp = pd.read_csv('zscore.csv')
                else:
                    zscore_temp = pd.DataFrame(columns=['base_symbol', 'quote_symbol', 'zscore', 'hedge_ratio', 'window', 'time_stored'])

                # Create a csv file to store the zscore of each pair with zscore greater than 3 or less than -3 with the current time
                if zscore_current > 3 or zscore_current < -3:
                    # Check the csv if the pair already exists. If not, store the pair, zscore and current time. If yes, check if current time is more than 1 hour of the time_stored. If yes, check the zscore again. If zscore is still greater than 3 or less than -3, store the pair, zscore and current time. If no, continue.
                    if os.path.isfile('zscore.csv'):
                        zscore = pd.read_csv('zscore.csv')
                        if base_crypto in zscore['base_symbol'].values and quote_crypto in zscore['quote_symbol'].values:
                            if zscore['time_stored'][zscore['base_symbol'] == base_crypto].values[0] + 3600 < time.time():
                                if zscore_current > 3 or zscore_current < -3:
                                    #Delete pair details from csv
                                    zscore = zscore.drop(zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)].index)
                                    zscore = zscore.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio':hedge_ratio, "window" : window , 'time_stored': time.time()}, ignore_index=True)
                                    # Sort by zscore before storing
                                    zscore = zscore.sort_values(by=['zscore'], ascending=False)
                                    zscore.to_csv('zscore.csv', index=False)
                                    send_message(f'{base_crypto} and {quote_crypto} added to csv [>1 hr]. Zscore: {zscore_current}')
                                else :
                                    # If zscore is less than 3 or greater than -3 and time is more than 1 hour, delete the pair from the csv
                                    # send message to telegram that the pair is deleted
                                    send_message(f'{base_crypto} and {quote_crypto} removed from csv')
                                    zscore = zscore.drop(zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)].index)
                            else :
                                # If time is less than 1 hour, check if current z score is more than stored z score. If yes, update the zscore and time_stored. If no, continue.
                                if abs(zscore_current) > abs(zscore['zscore'][zscore['base_symbol'] == base_crypto].values[0]):
                                    #Remove previous entry of the pair
                                    zscore = zscore.drop(zscore[(zscore['base_symbol'] == base_crypto) & (zscore['quote_symbol'] == quote_crypto)].index)

                                    #Add new entry of the pair
                                    zscore = zscore.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio':hedge_ratio, "window" : window, 'time_stored': time.time()}, ignore_index=True)
                                    # Sort by zscore before storing
                                    zscore = zscore.sort_values(by=['zscore'], ascending=False)
                                    zscore.to_csv('zscore.csv', index=False)
                                    send_message(f'{base_crypto} and {quote_crypto} updated. Zscore: {zscore_current}')
                        else:
                            zscore = zscore.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio':hedge_ratio, "window" : window, 'time_stored': time.time()}, ignore_index=True)
                            # Sort by zscore before storing
                            zscore = zscore.sort_values(by=['zscore'], ascending=False)
                            zscore.to_csv('zscore.csv', index=False)
                            send_message(f'[NEW PAIR]{base_crypto} and {quote_crypto} added to csv [NEW PAIR]. Zscore: {zscore_current}')
                    else:
                        zscore = pd.DataFrame(columns=['base_symbol', 'quote_symbol', 'zscore', 'time_stored'])
                        zscore = zscore.append({'base_symbol': base_crypto, 'quote_symbol': quote_crypto, 'zscore': zscore_current, 'hedge_ratio':hedge_ratio, "window" : window, 'time_stored': time.time()}, ignore_index=True)
                        # Sort by zscore before storing
                        zscore = zscore.sort_values(by=['zscore'], ascending=False)
                        zscore.to_csv('zscore.csv', index=False)
                        send_message(f'[NEW PAIR]{base_crypto} and {quote_crypto} added to csv [NEW PAIR]. Zscore: {zscore_current}')

                

                    
                #print(f"Checking Z Score for {base_crypto} and {quote_crypto} with hedge_ratio {hedge_ratio} and window : {window} ")
                if zscore_current > 2.5 or zscore_current < -2.5:
                    print("FOUND AN OPPORTUNITY : ")
                    print(f'{base_crypto} - {hedge_ratio}*{quote_crypto} Zscore: {zscore_current} Window : {window} ')

                    # if zscore_current >= 4 or zscore_current <= -4:
                    #     send_message(f'ALERT : {base_crypto} and {quote_crypto} are cointegrated. Current zscore: {zscore_current} with hedge_ratio {hedge_ratio} and window : {window} ')

                    # Check zscore_temp dataframe if the pair already exists. If yes, check if current zscore > 4 or <-4 and is more than the stored value of zscore. If yes, send message. If no, continue. If no, check if current zscore > 4 or <-4. If yes, store the pair, zscore and current time. If no, continue.
                    if base_crypto in zscore_temp['base_symbol'].values and quote_crypto in zscore_temp['quote_symbol'].values:
                        if zscore_current > 3 or zscore_current < -3:
                            if abs(zscore_current) >= abs(zscore_temp['zscore'][zscore_temp['base_symbol'] == base_crypto].values[0]):
                                send_message(f'ALERT : {base_crypto} and {quote_crypto} are cointegrated. Current zscore: {zscore_current} with hedge_ratio {hedge_ratio} and window : {window} ')
                            else:
                                continue
                        else:
                            continue

            print("<-------------------------------------> \n\n\n\n\n")
            print("<------------------------------------->")
            time.sleep(60)
        except:
            print("Error in zscore_checker")
            time.sleep(15)
            continue

zscore_checker()
