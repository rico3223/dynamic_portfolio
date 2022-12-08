import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt



class Portfolio():

    def __init__(self, capital, tax_rate, fee):
        self.capital = capital
        self.tax_rate = tax_rate
        self.fee = fee
        self.trades = 0
        self.daily_return = 0
        self.overall_return = 0
        self.prices = pd.read_csv('raw_data/backtest_data/open_price_454_stocks.csv', index_col=0)
        self.prices.reset_index(inplace=True, drop=True)
        self.preds = pd.read_csv('raw_data/backtest_data/gradientboosting_pred_454_stocks.csv', index_col=0)
        self.preds.reset_index(inplace=True, drop=True)

    def rotation_strategy(self):
        self.shorts = []
        self.longs = []
        for self.row in self.preds.index[:len(self.preds)-1]:
            self.value = self.preds.loc[self.row].sort_values(ascending=True)
            self.close_position()
            for stock in self.value.index[:5]:
                #print(stock)
                if stock in self.shorts and stock not in self.value.index[:5]:
                    self.place_buy_order(stock = stock)
                    #self.shorts.remove(stock)
                    #print(self.shorts)
                if stock not in self.shorts and stock in self.value.index[:5]:
                    self.place_sell_order(stock = stock)
                    self.shorts.append(stock)
                    #print(self.shorts)
                if stock in self.shorts and stock in self.value.index[:5]:
                    continue

            for stock in self.value.index[-5:]:
                if stock in self.longs and stock not in self.value.index[-5:]:
                    self.place_sell_order(stock = stock)
                    #self.longs.remove(stock)
                    #print(self.longs)
                if stock not in self.longs and stock in self.value.index[-5:]:
                    self.place_buy_order(stock = stock)
                    self.longs.append(stock)
                    #print(self.longs)
                if stock in self.longs and stock in self.value.index[-5:]:
                    continue
        print(self.longs)
        print(self.shorts)

    def close_position(self):
        for stock in self.preds.columns:
            if stock in self.shorts and stock in self.value.index[5:-6]:
                self.place_buy_order(stock=stock)
                self.shorts.remove(stock)
            if stock in self.longs and stock in self.value.index[5:-6]:
                self.place_sell_order(stock=stock)
                self.longs.remove(stock)


    def place_buy_order(self, stock, units = 1):
        price = self.prices.at[self.row+1, stock] # aller récupérer le bon prix
        self.capital -= (units * price) * (1 + self.fee)
        self.trades += 1
        print(f'buy {stock} at price={price}: capital={self.capital}, trades={self.trades}')
        #\n portfolio buy = {self.longs}

    def place_sell_order(self, stock, units = 1):
        price = self.prices.at[self.row+1, stock] # aller récupérer le bon prix
        self.capital += (units * price) * (1 - self.fee)
        self.trades += 1
        print(f'sell {stock} at price={price}: capital={self.capital}, trades={self.trades}')

if __name__== "__main__":
    toto = Portfolio(100000, 0, 0)
    toto.rotation_strategy()
