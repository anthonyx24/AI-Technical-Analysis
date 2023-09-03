from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import general_pkg.indicators as ind
import general_pkg.get_data as gd

class EmaCross(Strategy):

    def init(self):
        self.close = self.data.Close # sets close data? idk
        self.ema = ind.ema(self.close, 21)

    def next(self): # figure out if this is right
        if crossover(self.ema, self.close): 
            self.buy()
        elif crossover(self.close, self.ema): 
            self.sell()

class SmaCross(Strategy):

    n1 = 20 # period of the first SMA
    n2 = 50 # period of the second SMA

    def init(self):
        close = self.data.Close # close price data
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
      if crossover(self.sma1, self.sma2):
          self.buy()
      elif crossover(self.sma2, self.sma1):
          self.sell()


if __name__ == '__main__':
    prices = gd.get_data()[0]
    bt = Backtest(prices, EmaCross, commission=0.002, exclusive_orders=True)
    stats = bt.run()
    print(stats)
    print(stats['_trades'])
    bt.plot()
