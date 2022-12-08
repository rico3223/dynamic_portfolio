import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt



class Portfolio():

    def __init__(self, capital, tax_rate, fee, percentage):
        self.capital = capital
        self.tax_rate = tax_rate
        self.fee = fee
        self.percentage = percentage
        self.trades = 0
        self.daily_return = 0
        self.overall_return = 0
        self.prices = pd.read_csv('raw_data/backtest_data/open_price_454_stocks.csv', index_col=0)
        self.prices.reset_index(inplace=True, drop=True)

    def rotation_strategy(self, n_longs, n_shorts, y_pred=True):
        self.n_longs = n_longs
        self.n_shorts = n_shorts
        self.shorts = {}
        self.longs = {}
        self.counter = 0

        if y_pred==True:
            self.returns = pd.read_csv('raw_data/backtest_data/gradientboosting_pred_454_stocks.csv', index_col=0)
            self.returns.reset_index(inplace=True, drop=True)
        else:
            self.returns = pd.read_csv('raw_data/backtest_data/real_returns.csv', index_col=0)
            self.returns.reset_index(inplace=True, drop=True)

        for self.row in self.returns.index[:len(self.returns)-1]:
            self.counter += 1
            print(f'Day {self.counter}\n=================')

            print(self.shorts)
            print(self.longs)

            self.value = self.returns.loc[self.row].sort_values(ascending=True)
            print('Closed positions')
            self.close_position()

            print(self.shorts)
            print(self.longs)

            self.top_5 = self.returns.loc[self.row].sort_values(ascending=False)
            print('Opened positions')
            for stock in self.top_5.index[:self.n_longs]:
                # if stock in self.longs.keys() and stock not in self.top_5.index[:self.n_longs]:
                #     self.place_sell_close_long(stock = stock)
                if stock not in self.longs.keys() and stock in self.top_5.index[:self.n_longs]:
                    self.place_buy_open_long(stock = stock)
                if stock in self.longs.keys() and stock in self.top_5.index[:self.n_longs]:
                    continue
            for stock in self.value.index[:self.n_shorts]:
                # if stock in self.shorts.keys() and stock not in self.value.index[:self.n_shorts]:
                #     self.place_buy_close_short(stock = stock)
                if stock not in self.shorts.keys() and stock in self.value.index[:self.n_shorts]:
                    self.place_sell_open_short(stock = stock)
                if stock in self.shorts.keys() and stock in self.value.index[:self.n_shorts]:
                    continue
        print(self.shorts)
        print(self.longs)


    def close_position(self):
        temp_list_long = list(self.longs.keys())
        for stock in temp_list_long:
           if stock in self.value.index[self.n_shorts:-self.n_longs+1]:
                self.place_sell_close_long(stock=stock)
                del self.longs[stock]

        temp_list_short = list(self.shorts.keys())
        for stock in temp_list_short:
            if stock in self.value.index[self.n_shorts:-self.n_longs+1]:
                self.place_buy_close_short(stock=stock)
                del self.shorts[stock]


    def place_buy_open_long(self, stock):
        # if stock in self.longs.keys():
        #     price = self.prices.at[self.row+1, stock]
        #     units = self.longs[stock]
        #     self.capital -= (units * price) * (1 + self.fee)

        price = self.prices.at[self.row+1, stock]
        units = int((self.percentage*self.capital)/price)
        self.capital -= (units * price) * (1 + self.fee)
        self.longs[stock]=units

        self.trades += 1
        print(f'buy {units} {stock} at price={price} capital={self.capital}, trades={self.trades}')


    def place_buy_close_short(self, stock):
        price = self.prices.at[self.row+1, stock]
        units = self.shorts[stock]
        self.capital -= (units * price) * (1 - self.fee)

        self.trades += 1
        print(f'buy {units} {stock} at price={price} capital={self.capital}, trades={self.trades}')

    def place_sell_close_long(self, stock):
        price = self.prices.at[self.row+1, stock]
        units = self.longs[stock]
        self.capital += (units * price) * (1 - self.fee)

        self.trades += 1
        print(f'sell {units} {stock} at price={price} capital={self.capital}, trades={self.trades}')

    def place_sell_open_short(self, stock):
        # if stock in self.shorts.keys():
        #     price = self.prices.at[self.row+1, stock]
        #     units = self.shorts[stock]
        #     self.capital += (units * price) * (1 - self.fee)
        price = self.prices.at[self.row+1, stock]
        units = int((self.percentage*self.capital)/price)
        self.capital += (units * price) * (1 - self.fee)
        self.shorts[stock]=units
        self.trades += 1

        print(f'sell {units} {stock} at price={price}: capital={self.capital}, trades={self.trades}')

if __name__== "__main__":
    toto = Portfolio(100000, 0, 0, percentage=0.1)
    toto.rotation_strategy(n_longs=5, n_shorts=5, y_pred=True)
