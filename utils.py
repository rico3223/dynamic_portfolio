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


def macro_cleaning(url):
    """Methodology used to clean macro features extracted from Alphavantage"""
    url = 'path'

    temp = pd.read_csv(url) #reads csv as dataframe

    temp['timestamp'] = pd.to_datetime(temp['timestamp']) #converts column to date format

    temp = temp.rename(columns = {'timestamp':'date', 'value': 'indicator'}) #renames columns as date and the relevant indicator

    temp_mask = temp['date'] >= '2000-01-01' #filter for relevant timeframe
    temp = temp[temp_mask] #apply filter

    temp = temp.sort_values('date', ascending=True) #sort to start from 2000

    temp['indicator_change'] = temp['indicator'].pct_change() #calculate % changes

    temp.to_csv('new_path')

    return
