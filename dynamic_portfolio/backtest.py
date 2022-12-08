
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    def max_drawdown_absolute(length_interval, return_col):
        return_col = return_col[1:]
        max_drawdown = 0
        index_drawdown_final = []
        index_drawdown_temp = []
        counter = 0

        for k in range(0, return_col.shape[0]-length_interval):
            counter += 1
            temp_df = return_col[k: k+length_interval]
            sum_return = np.sum(temp_df)
            index_drawdown_temp = list(range(k, k+length_interval))
            if sum_return < max_drawdown:
                max_drawdown = sum_return
                index_drawdown_final = index_drawdown_temp
                counter = 0

        return max_drawdown, index_drawdown_final

    def close_out(self, bar):

        date, price = self.get_data_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f'{date} | inventory {self.units} units at {price:.2f}')
            print('=' * 55)
        tax_rate = 0.3
        net_profit = self.amount * (1-tax_rate)
        perf = ((self.amount - self.initial_amount) / self.initial_amount * 100)
        net_perf = ((net_profit - self.initial_amount) / self.initial_amount * 100)
        sharpe_ratio = ((np.sum(self.data['return']).mean()) - 0.03)/(np.sum(self.data['return'][0]).std())
        #substract 10y yield for sharpe ratio, 0.03 for instance
        ann_sharpe = sharpe_ratio * 252 ** 0.5
        print('Final Balance (gross) [$] {:.2f}'.format(self.amount))
        print('Final Balance (net) [$] {:.2f}'.format(net_profit))
        print('Gross Performance [%] {:.2f}'.format(perf))
        print('Net Performance [%] {:.2f}'.format(net_perf))
        print('Trades Executed [#] {:.2f}'.format(self.trades))
        print('=' * 55)
        print('Sharpe Ratio {:.2f}'.format(sharpe_ratio))
        print('Annualized Sharpe Ratio {:.2f}'.format(ann_sharpe))

class BacktestLongOnly(BacktestBase):

    def run_sma_strategy(self, SMA1, SMA2):

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

class RotationBestWorst(BacktestBase):

    def go_long(self, bar, units=None, amount=None):

        if self.position == -1:
            self.place_buy_order(bar, units= -self.units)
        if units:
            self.place_buy_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_buy_order(bar, amount=amount)

    def go_short(self, bar, units=None, amount=None):

        if self.position == 1:
            self.place_sell_order(bar, units= self.units)
        if units:
            self.place_sell_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_sell_order(bar, amount=amount)

    def run_rotation_strategy(self):

        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount
        # Get y_pred returns from df
        self.data['y_pred'] = self.data['y_pred']

        for y_pred_return in range(0, len(self.data['y_pred'])):
            if self.position == 0:
                if self.data['y_pred'].iloc[y_pred_return] > 0.01:
                    self.place_buy_order()
                    self.position = 1
            if self.position == 1:
                if self.data['y_pred'].iloc[y_pred_return] < -0.01:
                    self.place_sell_order()
                    self.position = 0
            if self.position == 0:
                if self.data['y_pred'].iloc[y_pred_return] < -0.01:
                    self.place_sell_order()
                    self.position = 1

        self.close_out()

class LongOnlyStock(BacktestBase):

    def run_best_performing(self):

        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount
        # Get y_pred returns from df
        self.data['y_pred'] = self.data['y_pred']

        for y_pred_return in range(0, len(self.data['y_pred'])):
            if self.position == 0:
                if self.data['y_pred'].iloc[y_pred_return] in range(self.data['y_pred'][0], self.data['y_pred'][5]):
                    self.place_buy_order
                    self.position = 1

        self.close_out()

class WorstOnlyStock(BacktestBase):

    def run_worst_performing(self):

        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount
        # Get y_pred returns from df
        self.data['y_pred'] = self.data['y_pred']

        for y_pred_return in range(0, len(self.data['y_pred'])):
            if self.position == 0:
                if self.data['y_pred'].iloc[y_pred_return] in range(self.data['y_pred'][495], self.data['y_pred'][500]):
                    self.place_sell_order
                    self.position = 1

        self.close_out()



class BacktestLongShort(BacktestBase):

    def go_long(self, bar, units=None, amount=None):

        if self.position == -1:
            self.place_buy_order(bar, units= -self.units)
        if units:
            self.place_buy_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_buy_order(bar, amount=amount)

    def go_short(self, bar, units=None, amount=None):

        if self.position == 1:
            self.place_sell_order(bar, units= self.units)
        if units:
            self.place_sell_order(bar, units=units)
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_sell_order(bar, amount=amount)

    def run_sma_strategy(self, SMA1, SMA2):

        msg = f'\n\nRunning SMA strategy | SMA1={SMA1} & SMA2={SMA2}'
        msg += f'\nFixed costs {self.ftc}'
        msg += f'\nProportional costs {self.ptc}'
        print(msg)
        print('=' *  55)
        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()

        for bar in range(SMA2, len(self.data)):
            if self.position in [0, -1]:
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    self.go_long(bar, amount = 'all')
                    self.position = 1
            if self.position in [0, 1]:
                if self.data['SMA1'].iloc[bar] < self.data['SMA2'].iloc[bar]:
                    self.go_short(bar, amount='all')
                    self.position = -1
        self.close_out(bar)



if __name__ == '__main__':

    bb = BacktestBase('SPY', '2010-01-04', '2019-12-31', 10000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()

    def run_strategy():

        lobt.run_sma_strategy(20, 100)
    # lobt = BacktestLongShort('SPY', '2010-01-04', '2019-12-31', 10000, verbose = False)

    # run_strategy()

    lobt = BacktestLongShort('SPY', '2010-01-04', '2019-12-31', 10000, 10.0, 0.01, False)

    run_strategy()
