import format_data as fm
import requests as rq
import pandas as pd
import numpy as np
import json

'''
For now: Request data from Polygon API.
Implement later: Make continual requests to Polygon API. 

Format the data using format_data.py. Remove nan values, split into training and testing data.

'''

TICKERS = ['SPY', 'QQQ', 'TSLA', 'AAPL']
TRAIN_SPLIT = 0.8 # 80% training, 20% testing
TIMESPAN = 'hour'
MULTIPLIER = '3'
START_DATE = '2021-07-24'
END_DATE = '2023-07-24'

def get_data():

    # Store list of dataframes for each ticker
    price_dfs = []

    for ticker in TICKERS:
        # First, make API call to Polygon for each ticker
        api_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{MULTIPLIER}/{TIMESPAN}/{START_DATE}/{END_DATE}?adjusted=true&sort=desc&limit=50000&apiKey=4Eqgqi3RkK6JwXTftEwg_bbp_hMkamaN"
        
        call = rq.get(api_url)
        # print(call.json())
        if(call.status_code != 200):
            print(f"API Call failed with status code: {call.status_code}")
        else:
            prices = call.json().get('results',[]) # returns results as default, empty dataframe if it doesn't exist
            prices = pd.DataFrame.from_dict(prices) # KeyError for results???
            # Splice to candlestick numbers, rename cols
            prices = prices.loc[:, ['o', 'c', 'h', 'l']]
            prices.rename(columns={'o':'Open', 'c':'Close', 'h': 'High', 'l': 'Low'}, inplace=True)
            print(prices)
            # Call fill + classify functions from format_data.py
            prices = fm.fill_returns(prices)
            prices = fm.classify(prices)
            # Calculating percentages may result in -inf/inf values, replace with nan and drop
            prices.replace([np.inf, -np.inf],np.nan)
            price_dfs.append(prices.dropna(axis='index'))
            print(prices)

    
    # Combine all the values together
    values = pd.concat(price_dfs).values 

    # Shuffle values to ensure NN doesn't learn order
    np.random.shuffle(values)

    # Split rows into train and test data (x: input, y: output/labels)
    split_idx = int(TRAIN_SPLIT*values.shape[0])

    # Save input training data, exclude last col (labels)
    np.save('x_train', fm.reshape_input(values[:split_idx, :-1]))

    # Save input testing data
    np.save('x_test', fm.reshape_input(values[split_idx:, :-1]))

    # Save output training data
    np.save('y_train', values[:split_idx, -1])

    # Save output testing data
    np.save('y_test', values[:split_idx, -1])

if __name__ == '__main__':
    
    get_data()
