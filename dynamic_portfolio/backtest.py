
import numpy as np
import pandas as pd

class BacktestBase(object):

    def __init__ (self, symbol, start, end, amount, ftc=0.0, ptc=0.0, verbose=True):

        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.get_data()

    def get_data(self):

        raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv', index_col = 0, parse_dates = True).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start:self.end]
        raw.rename(columns={self.symbol: 'price'}, inplace = True)
        raw['return'] = np.log(raw / raw.shift(1))
        self.data = raw.dropna()

    def plot_data(self, cols=None):

        if cols is None:
            cols = ['price']
        self.data['price'].plot(figsize=(10,6), title=self.symbol)

    def get_data_price(self, bar):

        date = str(self.data.index[bar])[:10]
        price = self.data.price.iloc[bar]
        return date, price

    def print_balance(self, bar):

        date, price = self.get_date_price(bar)
        print(f'{date} | current balance {self.amount:2f}')

    def print_net_wealth(self, bar):

        date, price = self.get_date_price(bar)
        net_wealth = self.units * price + self.amount
        print(f'{date} | current net wealth {net_wealth:2f}')

    def place_buy_order(self, bar, units = None, amount = None):

        date, price = self.get_data_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount -= (units * price) * (1 + self.ptc) + self.ftc
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def place_sell_order(self, bar, units = None, amount = None):

        date, price = self.get_data_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount += (units * price) * (1 - self.ptc) - self.ftc
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def close_out(self, bar):

        date, price = self.get_data_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f'{date} | inventory {self.units} units at {price:.2f}')
            print('=' * 55)
        print('Final balance [$] {:.2f}'.format(self.amount))
        perf = ((self.amount - self.initial_amount) / self.initial_amount * 100)
        print('Net Performance [%] {:.2f}'.format(perf))
        print('Trades Executed [#] {:.2f}'.format(self.trades))
        print('=' * 55)


class BacktestLongOnly(BacktestBase):

    def sma_strategy(self, SMA1, SMA2):

        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()

        for bar in range(SMA2, len(self.data)):
            if self.position == 0:
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    self.place_buy_order(bar, amount = self.amount)
                    self.position = 1
            elif self.position ==1:
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0
        self.close_out(bar)


        def run_strategy():

            lobt.run_sma_strategy(42, 252)
        lobt = BacktestLongOnly('SPY', '2010-01-04', '2019-12-31', 10000, verbose = False)

        run_strategy()

        lobt = BacktestLongOnly('SPY', '2010-01-04', '2019-12-31', 10000, 10.0, 0.01, False)

        run_strategy()


if __name__ == '__main__':

    bb = BacktestBase('SPY', '2010-01-04', '2019-12-31', 10000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()

    BacktestLongOnly.run_strategy()
