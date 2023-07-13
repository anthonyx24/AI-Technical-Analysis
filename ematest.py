import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ma(source, length, type):
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

    # elif type == "SMMA (RMA)":
    #     alpha = 1 / length
    #     weights = np.exp(np.linspace(-alpha*(length-1), 0, length))
    #     weights /= np.sum(weights)
    #     return np.dot(source[-length:], weights)
    # elif type == "WMA":
    #     weights = np.arange(1, length + 1)
    #     weights /= np.sum(weights)
    #     return np.dot(source[-length:], weights)
    # elif type == "VWMA":
    #     volume = np.array([v for v in source[-length:, 1]])  # Assuming volume is the second column
    #     weights = volume / np.sum(volume)
    #     return np.dot(source[-length:, 0], weights)  # Assuming prices are in the first column
    
prices = pd.read_csv("data/SPY.csv")
close = prices['Close'].to_numpy()

length = 21  # Length
src = close  # Source
offset = 0  # Offset

out = ma(src, length, "EMA")
# print(out)

# Plotting EMA
# plt.plot(out, color='blue')

typeMA = "SMA"  # Method
smoothingLength = 5  # Length

smoothingLine = ma(out, smoothingLength, typeMA)

# Plotting Smoothing Line
plt.plot(smoothingLine, color='blue')
plt.plot(src, color='green')
plt.show()