# importing relevant librairies
import numpy as np
import pandas as pd
import yfinance as yf


def load_csv(tickers: list, start:str, end:str):
    """
    Creating a function that would allow us to load a csv containing all relevant features of a given ticker
    Start and end should in the be following format: %YYYY-%MM-%DD
    """
    ticker = yf.download(tickers=tickers, start=start, end=end)
    wti = yf.download('WTI', start=start, end=end)
    gold = yf.download('GC=F', start=start, end=end)
    us_dollar = yf.download('DX-Y.NYB', start=start, end=end)

    credit_spread = #load from project directory
    ffunds_rate = #load from project directory
    treasury_yield = #load from project directory
    unemployment = #load from project directory
    inflation_expectation = #load from project directory
    non_farm_payroll = #load from project directory
    inflation = #load from project directory
    cpi = #load from project directory
    wmt = #load from project directory
    retails = #load from project directory
    gdp_capita = #load from project directory
    gdp = #load from project directory

    return ...
