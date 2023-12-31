import numpy as np
import pandas as pd
import general_pkg.indicators as ind
import general_pkg.get_data as gd

pd.options.mode.chained_assignment = None  # default='warn'

'''
For now: Request data from Polygon API.
Implement later: Make continual requests to Polygon API. 

Format the data. Remove nan values, split into training and testing data.

'''

TRAIN_SPLIT = 0.8 # 80% training, 20% testing
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
    Current Classifications:
    - 0: Closing price below EMA
    - 1: Closing price above or equal to EMA

    Future, will replace this with triangle labeling.

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


def format_data():

    # Store list of dataframes for each ticker
    price_dfs = gd.get_data()

    for prices in price_dfs:
        # Call fill + classify functions from format_data.py
        prices = fill_returns(prices)
        prices = classify(prices)
        # Calculating percentages may result in -inf/inf values, replace with nan and drop
        prices.replace([np.inf, -np.inf],np.nan)
        prices.dropna(axis='index')
        print(prices)
    
    # Combine all the values together
    values = pd.concat(price_dfs).values 

    # Shuffle values to ensure NN doesn't learn order
    np.random.shuffle(values)

    # Split rows into train and test data (x: input, y: output/labels)
    split_idx = int(TRAIN_SPLIT*values.shape[0])

    # Save input training data, exclude last col (labels)
    np.save('x_train', reshape_input(values[:split_idx, :-1]))

    # Save input testing data
    np.save('x_test', reshape_input(values[split_idx:, :-1]))

    # Save output training data
    np.save('y_train', values[:split_idx, -1])

    # Save output testing data
    np.save('y_test', values[:split_idx, -1])


if __name__ == '__main__':
    
    format_data()

    

