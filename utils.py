# importing relevant librairies
import numpy as np
import pandas as pd
import yfinance as yf


def load_csv(tickers: list, start:str, end:str):
    """
    Creating a function that would allow us to load a csv containing the Adj close, High, Low and volume of relevant tickers
    tickers should be a list
    """
    csv = yf.download(tickers=tickers, start=start, end=end)
    csv.drop(columns='Close', inplace=True)
    csv = csv[1:].copy()

    return csv


load_csv(['AAPL'], start='2000-01-01', end='2000-01-10')
