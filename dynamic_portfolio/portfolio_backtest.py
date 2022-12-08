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
        self.shorts = []
        self.longs = []
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
            self.value = self.returns.loc[self.row].sort_values(ascending=True)
            self.close_position()
            print('Closed positions')
            for stock in self.value.index[:self.n_shorts]:
                if stock in self.shorts and stock not in self.value.index[:self.n_shorts]:
                    self.place_buy_order(stock = stock)
                if stock not in self.shorts and stock in self.value.index[:self.n_shorts]:
                    self.place_sell_order(stock = stock)
                if stock in self.shorts and stock in self.value.index[:self.n_shorts]:
                    continue
            for stock in self.value.index[-self.n_longs:]:
                if stock in self.longs and stock not in self.value.index[-self.n_longs:]:
                    self.place_sell_order(stock = stock)
                if stock not in self.longs and stock in self.value.index[-self.n_longs:]:
                    self.place_buy_order(stock = stock)
                if stock in self.longs and stock in self.value.index[-self.n_longs:]:
                    continue
            print('Opened poistions')

        # Close out all positions
        for stock in self.longs:
            self.place_sell_order(stock=stock)
            self.longs.remove(stock)
        for stock in self.shorts:
            self.place_buy_order(stock=stock)
            self.shorts.remove(stock)
        print(self.longs, self.shorts)


    def close_position(self):
        for stock in self.returns.columns:
            if stock in self.shorts and stock in self.value.index[self.n_shorts:-self.n_longs+1]:
                self.place_buy_order(stock=stock)
                self.shorts.remove(stock)
            if stock in self.longs and stock in self.value.index[self.n_shorts:-self.n_longs+1]:
                self.place_sell_order(stock=stock)
                self.longs.remove(stock)


    def place_buy_order(self, stock):
        price = self.prices.at[self.row+1, stock]
        units = int((self.percentage*self.capital)/price)
        self.capital -= (units * price) * (1 + self.fee)

        for i in range(units):
            self.longs.append(stock)

        self.trades += 1
        print(f'buy {units} {stock} at price={price} capital={self.capital}, trades={self.trades}')

    def place_sell_order(self, stock, units = 1):
        price = self.prices.at[self.row+1, stock]
        units = int((self.percentage*self.capital)/price)
        self.capital += (units * price) * (1 - self.fee)

        for i in range(units):
            self.shorts.append(stock)

        self.trades += 1
        print(f'sell {units} {stock} at price={price}: capital={self.capital}, trades={self.trades}')

if __name__== "__main__":
    toto = Portfolio(100000, 0, 0, percentage=0.05)
    toto.rotation_strategy(n_longs=5, n_shorts=5, y_pred=False)
