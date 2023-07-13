# Credit: https://wire.insiderfinance.io/how-to-develop-a-pattern-recognition-neural-network-for-trading-d0398eeb56f5

import os
import yfinance as yf

TICKERS = ['SPY', 'QQQ']

# Obtain price data for specified tickers
def get_data(tickers: list):
    
    # saves as pandas df

    data = yf.download(
        tickers = tickers,
        interval = '1d',
        group_by = 'ticker',
        threads = True
    )

    for ticker in tickers:
        try:
            df = data.loc[:, ticker.upper()].dropna()
            df.to_csv(f'data/{ticker}.csv', index = True)
        except:
            print(f'Ticker {ticker} failed to download.')
    
    return

if __name__ == '__main__':
    
    # Check if a directory exists called 'data', if not, create it
    if not os.path.isdir('data'):
        os.mkdir('data')
    
    get_data(TICKERS)


