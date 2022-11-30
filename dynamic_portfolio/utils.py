# importing relevant librairies
import numpy as np
import pandas as pd
import yfinance as yf



def load_csv(ticker: str):
    """
    Creating a function that would allow us to load a csv containing all relevant features of a given ticker
    ticker should be in capital
    Start and end should be in the be following format: %YYYY-%MM-%DD
    """

    #Loading all relevant csv files

    #Loading stock return
    ticker_df = pd.read_csv(f'../raw_data/stocks_return/adj_return_{ticker}.csv')
    ticker_df.rename(columns={'timestamp':'date'}, inplace=True)
    ticker_df.sort_values('date', ascending=True, inplace=True)
    ticker_df.reset_index(inplace=True, drop=True)

    if '1999-12-31' in ticker_df['date'].values:
        ticker_df = ticker_df[ticker_df['date']>'1999-12-31']
        ticker_df.reset_index(inplace=True, drop=True)

    #Loading stocks eps
    ticker_eps = pd.read_csv(f'../raw_data/eps/data_{ticker}.csv', index_col=0)
    ticker_eps['date'] = ticker_eps['reportedDate'].copy()
    ticker_eps.sort_values('date', inplace=True)
    ticker_eps['reportedDate']= pd.to_datetime(ticker_eps['reportedDate'])
    ticker_eps['year'] = pd.DatetimeIndex(ticker_eps['reportedDate']).year

    if 2000 in ticker_eps['year'].values:
        ticker_eps = ticker_eps[ticker_eps['year']>=2000]
        ticker_eps.reset_index(inplace=True, drop=True)

    ticker_eps.drop(columns=['year','fiscalDateEnding', 'estimatedEPS', 'surprise', 'reportedDate'], inplace=True)

    #Loading all macros and commodities
    gold = pd.read_csv('../raw_data/macro/gold.csv', index_col=0, decimal=',')
    us_dollar = pd.read_csv('../raw_data/macro/usd.csv', index_col=0)

    credit_spread = pd.read_csv('../raw_data/macro/us_yields.csv', index_col=0)
    oil = pd.read_csv('../raw_data/macro/oil.csv', index_col=0)
    orders = pd.read_csv('../raw_data/macro/orders.csv', index_col=0)
    ffunds_rate = pd.read_csv('../raw_data/macro/fed_funds.csv', index_col=0)
    unemployment = pd.read_csv('../raw_data/macro/unemployment.csv', index_col=0)
    inflation_expectation = pd.read_csv('../raw_data/macro/inflation_expectation.csv', index_col=0)
    non_farm_payroll = pd.read_csv('../raw_data/macro/non_farm_payroll.csv', index_col=0)
    cpi = pd.read_csv('../raw_data/macro/cpi.csv', index_col=0)
    retails = pd.read_csv('../raw_data/macro/retail_sales.csv', index_col=0)
    gdp_capita = pd.read_csv('../raw_data/macro/gdp_per_capita.csv', index_col=0)


    #Creating our final df and merging with relevant files
    final_df = ticker_df.copy()
    final_df = final_df.merge(ticker_eps, how='outer', on='date')
    final_df = final_df.merge(credit_spread, how='outer')
    final_df = final_df.merge(oil, how='outer', on='date')
    final_df = final_df.merge(orders, how='outer')
    final_df = final_df.merge(ffunds_rate, how='outer')
    final_df = final_df.merge(unemployment, how='outer')
    final_df = final_df.merge(inflation_expectation, how='outer')
    final_df = final_df.merge(non_farm_payroll, how='outer')
    final_df = final_df.merge(cpi, how='outer')
    final_df = final_df.merge(retails, how='outer')
    final_df = final_df.merge(gdp_capita, how='outer')
    final_df = final_df.merge(gold, how='outer', on='date')
    final_df = final_df.merge(us_dollar, how='outer', on='date')

    #Sorting by chronological order and resetting index
    final_df = final_df.sort_values('date', ascending=True)
    final_df.reset_index(drop=True, inplace=True)

    #Since not all features have daily data, we forward filled the missing values
    final_df['orders'] = final_df['orders'].fillna(method='ffill')
    final_df['retail_sales'] = final_df['retail_sales'].fillna(method='ffill')
    final_df['gdp_per_capita'] = final_df['gdp_per_capita'].fillna(method='ffill')
    final_df['CPI'] = final_df['CPI'].fillna(method='ffill')
    final_df['non_farm_payroll'] = final_df['non_farm_payroll'].fillna(method='ffill')
    final_df['inf_exp'] = final_df['inf_exp'].fillna(method='ffill')
    final_df['unemployment_rate'] = final_df['unemployment_rate'].fillna(method='ffill')
    final_df['reportedEPS'] = final_df['reportedEPS'].fillna(method='ffill')
    final_df['surprisePercentage'] = final_df['surprisePercentage'].replace(['None'], '0')
    final_df['surprisePercentage'] = final_df['surprisePercentage'].replace([np.nan], '0')

    #Changing the dtypes of relevant features such as surprisePercentage and gold_price
    final_df["surprisePercentage"] = pd.to_numeric(final_df["surprisePercentage"])

    # Chaging the unemployement rate to decimal
    final_df['unemployment_rate'] = final_df['unemployment_rate']/100
    final_df['surprisePercentage'] = final_df['surprisePercentage']/100

    #Dropping null values
    final_df.dropna(inplace=True)
    final_df.reset_index(drop=True, inplace=True)

    # calculating the return
    final_df['return'] = final_df['adjusted_close'].pct_change()
    final_df['return'][0]=0


    return final_df

def features_creation(ticker: str, high_low_ratio: bool = True, volatility: bool = True, momentum: bool = True, distance: bool = True, volume: bool = True, price_eps_ratio: bool = True,
                      momentum_eps_ratio: bool = True, gold_return: bool = True, oil_return: bool = True, usd_return: bool = True, cpi_return: bool = True, period:int = 250,
                      gdp_return: bool = True, days:list = [5, 10, 20] ):
    """
    Function that adds features to a dataframe
    days should be a list containing the number of days to consider for calculating the volatitliy, momentum, distance and and custom volume
    in order to calculate the momentum/eps ratio, momentum should be True
    """

    final_df = load_csv(ticker=ticker)

    if high_low_ratio==True:
        final_df['high/low'] = final_df['high']/final_df['low'] - 1 # max variation in %

    if volatility==True:
        for day in days:
            final_df[f'volatility_{day}days'] = final_df['return'].rolling(day).std().shift(1)

    if momentum==True:
        for day in days:
            final_df[f'momentum_{day}days'] = final_df['return'].rolling(day).mean().shift(1)

    if distance==True:
        for day in days:
            final_df[f'distance_{day}days'] = (final_df['return'] - final_df['return'].rolling(day).mean().shift(1))

    if volume==True:
        for day in days:
            final_df[f'volume_{day}days'] = final_df['volume'].rolling(day).mean().shift(1)

    if price_eps_ratio==True:
        final_df['price/eps'] = final_df['adjusted_close']/final_df['reportedEPS']

    if momentum_eps_ratio==True:
        final_df['momentum/eps'] = final_df['momentum']/final_df['reportedEPS']

    if gold_return==True:
        final_df['gold_return'] = final_df['gold_price'].pct_change()

    if oil_return==True:
        final_df['oil_return'] = final_df['oil_price'].pct_change()

    if usd_return==True:
        final_df['usd_return'] = final_df['usd_price'].pct_change()

    if cpi_return==True:
        final_df['cpi_return'] = final_df['CPI'].pct_change(periods=30)

    if gdp_return==True:
        final_df['gdp_return'] = final_df['gdp_per_capita'].pct_change(periods=period)

    final_df.dropna(inplace=True)
    final_df.reset_index(drop=True, inplace=True)

    return final_df

def return_tickers():
    """
    Function to return in list of all S&P500 tickers
    """

    tickers =  ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'BRK.B', 'TSLA', 'UNH', 'XOM', 'JNJ', 'WMT', 'NVDA', 'JPM', 'V', 'CVX', 'PG', 'LLY', 'MA', 'HD', 'META', 'BAC', 'ABBV', 'PFE', 'KO', 'MRK', 'PEP', 'COST', 'ORCL', 'AVGO', 'TMO', 'MCD', 'CSCO', 'ACN', 'DHR', 'TMUS', 'ABT', 'WFC', 'DIS', 'LIN', 'NEE', 'BMY', 'NKE', 'VZ', 'TXN', 'UPS', 'COP', 'ADBE', 'CMCSA', 'CRM', 'PM', 'MS', 'AMGN', 'SCHW', 'HON', 'RTX', 'QCOM', 'T', 'IBM',
 'DE', 'CVS', 'LOW', 'GS', 'UNP', 'NFLX', 'LMT', 'CAT', 'AMD', 'INTC', 'ELV', 'SPGI', 'AXP', 'SBUX', 'INTU', 'BLK', 'ADP', 'GILD', 'PLD', 'MDT', 'BA', 'AMT', 'CI', 'GE', 'TJX', 'ISRG', 'C', 'AMAT', 'PYPL', 'MDLZ', 'CB', 'SYK', 'ADI', 'MMC', 'EOG', 'NOW', 'VRTX', 'MO', 'NOC', 'EL', 'REGN', 'PGR', 'BKNG', 'DUK', 'TGT', 'SLB', 'SO', 'MMM', 'ITW', 'ZTS', 'GD', 'APD', 'HUM', 'MRNA', 'BDX', 'CSX', 'WM', 'PNC', 'HCA', 'ETN', 'USB', 'FISV', 'SHW', 'OXY', 'CL', 'MU', 'CME', 'AON', 'LRCX', 'BSX', 'EQIX', 'TFC', 'PXD', 'CHTR', 'CCI', 'MET', 'ATVI', 'ICE', 'MPC', 'NSC', 'DG', 'GM', 'EMR', 'F', 'KLAC', 'MCO', 'FCX', 'KDP', 'MNST', 'MCK', 'VLO', 'ORLY', 'ADM', 'PSX',
 'PSA', 'SRE', 'SNPS', 'MAR', 'D', 'GIS', 'AEP', 'AZO', 'KHC', 'APH', 'HSY', 'CNC', 'CTVA', 'EW', 'CTAS', 'A', 'ROP', 'JCI', 'CDNS', 'FDX', 'NXPI', 'AIG', 'KMB', 'AFL', 'HES', 'MSI', 'PAYX', 'DVN', 'TRV', 'BIIB', 'DXCM', 'SYY', 'LHX', 'RSG', 'ENPH', 'ECL', 'ADSK', 'MCHP', 'ANET', 'KMI', 'CMG', 'FTNT', 'AJG', 'STZ', 'TT', 'WMB', 'MSCI', 'O', 'IQV', 'TEL', 'ROST', 'PRU', 'EXC', 'PH', 'FIS', 'SPG', 'COF', 'NUE', 'XEL', 'HLT', 'CARR', 'PCAR', 'BK', 'NEM', 'DOW', 'EA', 'WBA', 'DD', 'ALL', 'YUM', 'AMP', 'CMI', 'ILMN', 'BF.B', 'TDG', 'IDXX', 'ED', 'KR', 'ABC', 'DLTR', 'RMD', 'ALB', 'HAL', 'NDAQ', 'LVS', 'ODFL', 'WELL', 'AME', 'CSGP', 'OTIS', 'MTD', 'SBAC', 'ON', 'VICI', 'DLR', 'CEG', 'KEYS', 'PPG', 'WEC', 'CTSH', 'ROK', 'GWW', 'PCG', 'HPQ', 'FAST', 'DFS', 'MTB', 'PEG', 'OKE', 'DHI', 'APTV', 'BKR', 'GLW', 'LYB', 'ES', 'BAX', 'STT', 'VRSK', 'TROW', 'WBD', 'AWK', 'IT', 'GPN', 'HRL', 'FANG', 'WTW', 'RJF', 'GPC', 'IFF', 'CDW', 'TSCO', 'FITB', 'ARE', 'URI', 'ZBH', 'K', 'LEN', 'EBAY', 'EIX', 'CBRE', 'EFX', 'VMC', 'TSN',
 'HIG', 'FTV', 'WY', 'EQR', 'AVB', 'MKC', 'ETR', 'LUV', 'ULTA', 'AEE', 'MLM', 'FE', 'PFG', 'FRC', 'DTE', 'DAL', 'HBAN', 'IR', 'CTRA', 'ANSS', 'ACGL', 'PPL', 'RF', 'VRSN', 'LH', 'EXR', 'PWR', 'CF', 'CAH', 'CFG', 'XYL', 'HPE', 'EPAM', 'DOV', 'WAT', 'WRB', 'TDY', 'PAYC', 'ROL', 'NTRS', 'MRO', 'CNP', 'INVH', 'CHD', 'AES', 'MOH', 'JBHT', 'MAA', 'BBY', 'CLX', 'HOLX', 'WAB', 'DRI', 'EXPD', 'STE', 'AMCR', 'VTR', 'IEX', 'CAG', 'CMS', 'KEY', 'MPWR', 'BALL', 'J', 'BR', 'GRMN', 'PKI', 'TTWO', 'INCY', 'FDS', 'MOS', 'SEDG', 'CINF', 'ABMD', 'DGX', 'WST', 'ATO', 'TRGP', 'BRO', 'SYF', 'FOX', 'FOXA', 'NTAP', 'FMC', 'EQT', 'OMC', 'SJM', 'LYV', 'CPB', 'HWM', 'CPRT', 'AVY', 'IRM', 'COO', 'ALGN', 'SWKS', 'EXPE', 'RCL', 'ETSY', 'APA', 'GEN', 'TXT', 'LDOS', 'LKQ', 'TER', 'PTC', 'TRMB', 'AKAM', 'NVR', 'UAL', 'LNT', 'FLT', 'KIM', 'ZBRA', 'TYL', 'DPZ', 'JKHY', 'MGM', 'ESS', 'L', 'PEAK', 'MTCH', 'NDSN', 'EVRG', 'VTRS', 'IPG', 'BEN', 'CBOE', 'TECH', 'SIVB', 'VFC', 'IP', 'HST', 'UDR', 'POOL', 'RE', 'PARA', 'SNA', 'CPT', 'LW', 'PKG', 'CRL', 'SWK', 'BIO', 'WDC', 'CHRW', 'STX', 'MAS', 'GL', 'CE', 'REG', 'NI', 'BXP', 'HSIC', 'CCL', 'TFX', 'CZR', 'NWS', 'NWSA', 'KMX', 'EMN', 'JNPR', 'PHM', 'CDAY', 'ALLE', 'QRVO', 'BWA', 'NRG', 'MKTX', 'WRK', 'UHS', 'FFIV', 'AOS', 'CMA', 'AAL', 'BBWI', 'HII', 'AAP', 'TPR', 'FRT', 'IVZ', 'PNW',
 'HAS', 'WYNN', 'FBHS', 'SBNY', 'DISH', 'RHI', 'WHR', 'ZION', 'CTLT', 'PNR', 'SEE', 'RL', 'NCLH', 'DXC', 'GNRC', 'AIZ', 'XRAY', 'LNC', 'DVA', 'MHK', 'OGN', 'LUMN', 'ALK', 'NWL', 'VNO', 'TAP']

    return tickers
