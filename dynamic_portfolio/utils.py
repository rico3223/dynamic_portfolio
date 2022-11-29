# importing relevant librairies
import numpy as np
import pandas as pd
import yfinance as yf
gold = yf.download('GC=F', start='2000-01-01', end='2022-11-23')
us_dollar = yf.download('DX-Y.NYB',start='2000-01-01', end='2022-11-23')


def load_csv(ticker: str, start: str, end: str):
    """
    Creating a function that would allow us to load a csv containing all relevant features of a given ticker
    ticker should be in capital
    Start and end should be in the be following format: %YYYY-%MM-%DD
    """

    #Loading all relevant csv files
    ticker = pd.read_csv(f'../raw_data/adj_return_{ticker}.csv')
    ticker.rename(columns={'timestamp':'date'}, inplace=True)
    ticker.sort_values('date', ascending=True, inplace=True)
    ticker.reset_index(inplace=True, drop=True)

    if '1999-12-31' in ticker['date'].values:
        ticker = ticker[ticker['date']>'1999-12-31']
        ticker.reset_index(inplace=True, drop=True)


    gold = gold
    us_dollar = us_dollar

    credit_spread = pd.read_csv('../raw_data/us_yields.csv', index_col=0)
    oil = pd.read_csv('../raw_data/oil_return.csv', index_col=0)
    orders = pd.read_csv('../raw_data/orders.csv', index_col=0)
    ffunds_rate = pd.read_csv('../raw_data/fed_funds.csv', index_col=0)
    unemployment = pd.read_csv('../raw_data/unemployment.csv', index_col=0)
    inflation_expectation = pd.read_csv('../raw_data/inflation_expectation.csv', index_col=0)
    non_farm_payroll = pd.read_csv('../raw_data/non_farm_payroll.csv', index_col=0)
    cpi = pd.read_csv('../raw_data/cpi.csv', index_col=0)
    retails = pd.read_csv('../raw_data/retail_sales.csv', index_col=0)
    gdp_capita = pd.read_csv('../raw_data/gdp_per_capita.csv', index_col=0)

    #Creating our final df and merging with relevant files
    final_df = ticker.copy()
    final_df = final_df.merge(credit_spread, how='outer')

    final_df = final_df.merge(oil, how='outer', left_on='date', right_on='Date')
    final_df.drop(columns='Date', inplace=True)
    final_df.rename(columns={'Price':'oil_price'}, inplace=True)

    final_df = final_df.merge(orders, how='outer')

    final_df = final_df.merge(ffunds_rate, how='outer')

    final_df = final_df.merge(unemployment, how='outer')

    final_df = final_df.merge(inflation_expectation, how='outer')

    final_df = final_df.merge(non_farm_payroll, how='outer')

    final_df = final_df.merge(cpi, how='outer')

    final_df = final_df.merge(retails, how='outer')

    final_df = final_df.merge(gdp_capita, how='outer')

    #Sorting by chronological order and resetting index
    final_df = final_df.sort_values('date', ascending=True)
    final_df.reset_index(drop=True, inplace=True)

    #Dropping irrelevant features
    final_df.drop(columns=['oil_return','orders_change','unemployment_change','inf_exp_change', 'payroll_change', 'CPI_change','retail_sales_change','gdp_change'], inplace=True)

    #Since not all features have daily data, we forward filled the missing values
    final_df['orders'] = final_df['orders'].fillna(method='ffill')
    final_df['retail_sales'] = final_df['retail_sales'].fillna(method='ffill')
    final_df['gdp_per_capita'] = final_df['gdp_per_capita'].fillna(method='ffill')
    final_df['CPI'] = final_df['CPI'].fillna(method='ffill')
    final_df['non_farm_payroll'] = final_df['non_farm_payroll'].fillna(method='ffill')
    final_df['inf_exp'] = final_df['inf_exp'].fillna(method='ffill')
    final_df['unemployment_rate'] = final_df['unemployment_rate'].fillna(method='ffill')

    #Finally dropping our null values since they represent weekends and holidays
    final_df.dropna(inplace=True)
    final_df.reset_index(inplace=True, drop=True)


    return final_df
