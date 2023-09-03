import numpy as np
import pandas as pd

TICKER = "SPY"

'''
Calculates simple moving average, given price data and period length.
'''
def sma(source, length):
    result = np.empty(source.size - length)
    for i in range(length, source.size):
        temp = source[i-length:i]
        result[i-length] = np.mean(temp)
    return result

'''
Calculates exponential moving average, given price data and period length.
'''
def ema(source, length):
    result = np.empty(source.size - length)
    # weights for EMA
    alpha = 2 / (length + 1)
    weights = np.exp(np.linspace(-alpha*(length-1), 0, length))
    weights /= np.sum(weights)
    for i in range(length, source.size):
        temp = source[i-length:i]
        result[i-length] = np.dot(temp, weights)
    return result

