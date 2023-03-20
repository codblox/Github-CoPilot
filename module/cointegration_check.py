#import coint from statsmodels
from statsmodels.tsa.stattools import coint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import requests
import os
import sys
import json
import math
import random
import warnings
import requests
from datetime import datetime
from statsmodels.tsa.vector_ar.var_model import VAR
import statsmodels.api as sm
from sklearn.decomposition import PCA

#Calculate half_life of a time series using OLS
def half_life_ols(spread):
    df_spread = pd.DataFrame(spread)
    spread_lag = df_spread.close.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = df_spread.close - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    
    # Define the dependent and independent variables
    endog = spread_ret
    exog = sm.add_constant(spread_lag)  # add a constant to the independent variable

    # Fit the OLS model
    model = sm.OLS(endog=endog, exog=exog)
    results = model.fit()

    # Calculate the half-life of mean reversion
    half_life = round(-1 * np.log(2) / results.params[1], 0)
    return half_life
    

#Calculate window size for rolling z_score calculation using the method described in the paper "The Half-Life of Cointegration" by Hamilton (1994)
def window_size(half_life):
    window = int(2*half_life)
    return window

#Calculate z_score of the spread using the method described in the paper "The Half-Life of Cointegration" by Hamilton (1994) taking spread and rolling window size (window) as input
def zscore(spread, window):
    spread_mean = spread.rolling(window).mean()
    spread_std = spread.rolling(window).std()
    spread_zscore = (spread - spread_mean) / spread_std
    return spread_zscore

def hedge_ratio_pca(series_1, series_2):
    #calculate the hedge ratio using PCA
    series_1 = series_1 - series_1.mean()
    series_2 = series_2 - series_2.mean()
    x0 = np.column_stack((series_1,series_2))
    
    pca = PCA(n_components=2)
    pca.fit(x0)
    hedge_ratio = pca.components_[0][0] / pca.components_[0][1]
    print(pca.mean_[1]-hedge_ratio*pca.mean_[0])
    return hedge_ratio
    


def CointegrationCheck(base_data, quote_data, base_symbol, quote_symbol):
    #get the close column of both dataframes
    series_1 = base_data['close'].astype(float)
    series_2 = quote_data['close'].astype(float)
    
    coint_flag = 0
    
    #check for cointegration using Augmented Dickey Fuller test
    try :
        result = coint(series_1, series_2)
        test_stat = result[0]
        pvalue = result[1]
        crit_val_1 = result[2][0]
        crit_val_5 = result[2][1]
        crit_val_10 = result[2][2]
    except Exception as e:
        print(f'Error in cointegration check for {base_symbol} and {quote_symbol} : {e}')
        return

    if pvalue < 0.05 and test_stat < crit_val_5:
        coint_flag = 1

    if coint_flag == 1:
        try :
            #calculate hedge ratio
            hedge_ratio = round(hedge_ratio_pca(series_1, series_2),3)
            #calculate spread
            spread = base_data['close'].astype(float) - hedge_ratio*quote_data['close'].astype(float)
            #calculate half life
            half_life_res = half_life_ols(spread)
    #         half_life_2 = half_life(spread)

            #calculate window size
            window = window_size(half_life_res)

            #calculate 10th percentile of spread
            spread_10th_percentile = spread.quantile(0.1)

            #calculate 90th percentile of spread
            spread_90th_percentile = spread.quantile(0.9)

            if half_life_res > 3 and half_life_res < 25:
                #store and save the spread details in a csv file with name 'cointegrated_pairs.csv'. If the file does not exist, create it.
                if os.path.isfile('cointegrated_pairs.csv'):
                    df = pd.read_csv('cointegrated_pairs.csv')
                    df = df.append({'base_symbol': base_symbol, 'quote_symbol': quote_symbol, 'hedge_ratio': hedge_ratio, 'half_life': half_life_res, 'window': window, '10th percentile' : spread_10th_percentile, '90th percentile' : spread_90th_percentile}, ignore_index=True)
                    df.to_csv('cointegrated_pairs.csv', index=False)
                else:
                    df = pd.DataFrame({'base_symbol': base_symbol, 'quote_symbol': quote_symbol, 'hedge_ratio': hedge_ratio, 'half_life': half_life_res, 'window': window, '10th percentile' : spread_10th_percentile, '90th percentile' : spread_90th_percentile}, index=[0])
                    df.to_csv('cointegrated_pairs.csv', index=False)
        except Exception as e:
            print(e)
            print('Error in calculating hedge ratio, half life or window size for pair {} and {}'.format(base_symbol, quote_symbol))

def calculate_mean(spread):
    spread_mean = spread.mean()
    return spread_mean