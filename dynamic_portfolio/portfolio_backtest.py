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
        for row in self.preds.index:
            value = self.preds.loc[row].sort_values(ascending=True)
            print(value)
            for stock in value.index[:4]:
                print(stock)
                if stock not in shorts and stock in value.index[:4]:
                    self.place_sell_order()
                    shorts.append(stock)
                if stock in shorts and stock in value.index[:4]:
                    pass
                if stock in shorts and stock not in value.index[:4]:
                    self.place_buy_order()
                    shorts.remove(stock)
            for stock in value.index[-5:]:
                if stock not in longs and stock in value.index[-5:]:
                    self.place_buy_order()
                    longs.append(stock)
                if stock in longs and stock in value.index[-5:]:
                    pass
                if stock not in longs and stock not in value.index[-5:]:
                    self.place_sell_order
                    shorts.remove(stock)


    def place_buy_order(self, units = 1):
        price = self.prices.loc[row+1, stock] # aller récupérer le bon prix
        self.capital -= (units * price) * (1 + self.fee)
        self.trades += 1


    def place_sell_order(self, bar, units = 1):
        price = self.prices.loc[row+1, stock] # aller récupérer le bon prix
        self.capital += (units * price) * (1 - self.fee)
        self.trades += 1

if __name__== "__main__":
    toto = Portfolio(100000, 0.1, 0.1)
    toto.rotation_strategy()
