import requests as rq
import pandas as pd
import numpy as np
import json

'''
For now: Request data from Polygon API.
Implement later: Make continual requests to Polygon API. 

Format the data using format_data.py. Remove nan values, split into training and testing data.

'''

TICKERS = ['SPY']
TIMESPAN = 'day'
MULTIPLIER = '1'
START_DATE = '2021-09-01'
END_DATE = '2023-08-01'

def get_data():

    # Store list of dataframes for each ticker
    price_dfs = []

    for ticker in TICKERS:
        # First, make API call to Polygon for each ticker
        api_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{MULTIPLIER}/{TIMESPAN}/{START_DATE}/{END_DATE}?adjusted=true&sort=desc&limit=50000&apiKey=4Eqgqi3RkK6JwXTftEwg_bbp_hMkamaN"
        
        call = rq.get(api_url)
        if(call.status_code != 200):
            print(f"API Call failed with status code: {call.status_code}")
        else:
            prices = call.json().get('results',[]) # returns results as default, empty dataframe if it doesn't exist
            if not prices: break
            prices = pd.DataFrame.from_dict(prices)
            # Splice to candlestick numbers, rename cols
            prices = prices.loc[:, ['o', 'c', 'h', 'l']]
            prices.rename(columns={'o':'Open', 'c':'Close', 'h': 'High', 'l': 'Low'}, inplace=True)
            # print(prices)
            price_dfs.append(prices)
    
    return price_dfs
