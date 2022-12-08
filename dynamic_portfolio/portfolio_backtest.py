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
        self.preds = pd.read_csv('raw_data/backtest_data/gradientboosting_pred_454_stocks.csv', index_col=0)


    def rotation_strategy(self):
        shorts = []
        longs = []
        for self.row in self.preds.index[:len(self.preds)-1]:
            value = self.preds.loc[self.row].sort_values(ascending=True)
            print(value)
            for self.stock in value.index[:4]:
                print(self.stock)
                if self.stock not in shorts and self.stock in value.index[:4]:
                    self.place_sell_order(stock)
                    shorts.append(self.stock)
                if self.stock in shorts and self.stock in value.index[:4]:
                    pass
                if self.stock in shorts and self.stock not in value.index[:4]:
                    self.place_buy_order()
                    shorts.remove(self.stock)
            for self.stock in value.index[-5:]:
                if self.stock not in longs and self.stock in value.index[-5:]:
                    self.place_buy_order()
                    longs.append(self.stock)
                if self.stock in longs and self.stock in value.index[-5:]:
                    pass
                if self.stock not in longs and self.stock not in value.index[-5:]:
                    self.place_sell_order
                    shorts.remove(self.stock)


    def place_buy_order(self, units = 1):
        price = self.prices.loc[self.row+1, self.stock] # aller récupérer le bon prix
        self.capital -= (units * price) * (1 + self.fee)
        self.trades += 1


    def place_sell_order(self, stock, units = 1):
        price = self.prices.loc[self.row+1, self.stock] # aller récupérer le bon prix
        self.capital += (units * price) * (1 - self.fee)
        self.trades += 1

if __name__== "__main__":
    toto = Portfolio(100000, 0.1, 0.1)
    toto.rotation_strategy()
