import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "SPY"

def ema(source, length):
    result = np.empty(source.size - length)
    # weights for EMA
    alpha = 2 / (length + 1)
    weights = np.exp(np.linspace(-alpha*(length-1), 0, length))
    weights /= np.sum(weights)
    for i in range(length, source.size):
        temp = source[i-length:i]
        if type == "SMA":
            result[i-length] = np.mean(temp)
        elif type == "EMA":
            result[i-length] = np.dot(temp, weights)
    return result

# smoothing using SMA
# def smooth(source, length):
#     result = np.empty(source.size - length)
#     for i in range(length, source.size):
#         temp = source[i-length:i]
#         result[i-length] = np.mean(temp)
#     return result

    
# prices = pd.read_csv(f"data/{TICKER}.csv") # SPY for now
# close = prices['Close'].to_numpy()

# length = 21  # Length
# src = close  # Source
# offset = 0  # Offset

# out = ema(src, length)
# # print(out)

# # Plotting EMA
# # plt.plot(out, color='blue')

# typeMA = "SMA"  # Method
# smoothingLength = 5  # Length

# smoothingLine = smooth(out, smoothingLength)

# np.savetxt(f"data/{TICKER}_EMA.csv", smoothingLine, delimiter = ',')

# Plotting Smoothing Line
# plt.plot(smoothingLine, color='blue')
# plt.plot(src, color='green')
# plt.show()

# when price goes from under to over --> buy
# price goes over to under --> sell