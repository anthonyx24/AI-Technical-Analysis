import numpy as np
import pandas as pd
import indicators as ind


WINDOW_LENGTH = 30
FEAT_COLS = ['Open', 'Close', 'High', 'Low'] # need to rename cols from polygon


def lagged_cols(prices: pd.DataFrame, col: str, name: str) -> pd.DataFrame:
    '''
    Adds in new "lagged" columns for each time period 
    (so if window is 30, adds 29 new columns to get last 30 periods)
    '''
    return prices.assign(**{
        f'{name}_t-{lag}': col.shift(lag)
        for lag in range(0, WINDOW_LENGTH)
    })

def fill_returns(prices: pd.DataFrame) -> pd.DataFrame:
    '''
    For each of the feature cols, get percentage returns, add to cols created by
    lagged_cols function.
    '''
    for col in FEAT_COLS:
        return_col = prices[col]/prices[col].shift(1)-1
        # calculates percentage returns from prev period
        prices = lagged_cols(prices, return_col, f'{col}_Percent_Return')
    
    return prices


def classify(prices: pd.DataFrame) -> pd.DataFrame:
    '''
    Adds in a classification column to label data
    Classifications:
    - 0: Closing price below EMA
    - 1: Closing price above or equal to EMA
    '''
    close = prices['Close']
    averages = ind.ema(close, 21) # 21 EMA
    close = close[21:]
    # averages = ind.smooth(averages, 5) # 5 is smoothing length
    
    conditions = [
        close < averages,
        close >= averages,
    ]

    result = np.select(
        condlist = conditions,
        choicelist = [0,1]
    )

    # prices['averages'] = averages
    prices = prices[21:]
    prices['Class'] = result
    
    return prices


def reshape_input(input: np.array) -> np.array:
    '''
    For Recurrent Neural Nets (RNNs), the inputs need to be a 3D array
    with shape (#examples, time window length, #features)
    '''
    # number of features, assume all features are same length (should be 4)
    num_features = input.shape[1]//WINDOW_LENGTH # shape[1] = #cols

    # create empty array with correct size, shape[0] = rows
    reshaped = np.zeros((input.shape[0], WINDOW_LENGTH, num_features))

    # fill reshaped array
    for n in range(num_features):
        # separate 2D input array into 3D array by separating by feature (open, close, low, high)
        reshaped[:,:,n] = input[:, n*WINDOW_LENGTH:(n+1)*WINDOW_LENGTH]

    return reshaped

    

