# importing relevant librairies
import numpy as np
import pandas as pd
import yfinance as yf


tickers = ['AAPL',
 'MSFT',
 'GOOG',
 'AMZN',
 'BRK.B',
 'TSLA',
 'UNH',
 'XOM',
 'JNJ',
 'WMT',
 'NVDA',
 'JPM',
 'V',
 'CVX',
 'PG',
 'LLY',
 'MA',
 'HD',
 'META',
 'BAC',
 'ABBV',
 'PFE',
 'KO',
 'MRK',
 'PEP',
 'COST',
 'ORCL',
 'AVGO',
 'TMO',
 'MCD',
 'CSCO',
 'ACN',
 'DHR',
 'TMUS',
 'ABT',
 'WFC',
 'DIS',
 'LIN',
 'NEE',
 'BMY',
 'NKE',
 'VZ',
 'TXN',
 'UPS',
 'COP',
 'ADBE',
 'CMCSA',
 'CRM',
 'PM',
 'MS',
 'AMGN',
 'SCHW',
 'HON',
 'RTX',
 'QCOM',
 'T',
 'IBM',
 'DE',
 'CVS',
 'LOW',
 'GS',
 'UNP',
 'NFLX',
 'LMT',
 'CAT',
 'AMD',
 'INTC',
 'ELV',
 'SPGI',
 'AXP',
 'SBUX',
 'INTU',
 'BLK',
 'ADP',
 'GILD',
 'PLD',
 'MDT',
 'BA',
 'AMT',
 'CI',
 'GE',
 'TJX',
 'ISRG',
 'C',
 'AMAT',
 'PYPL',
 'MDLZ',
 'CB',
 'SYK',
 'ADI',
 'MMC',
 'EOG',
 'NOW',
 'VRTX',
 'MO',
 'NOC',
 'EL',
 'REGN',
 'PGR',
 'BKNG',
 'DUK',
 'TGT',
 'SLB',
 'SO',
 'MMM',
 'ITW',
 'ZTS',
 'GD',
 'APD',
 'HUM',
 'MRNA',
 'BDX',
 'CSX',
 'WM',
 'PNC',
 'HCA',
 'ETN',
 'USB',
 'FISV',
 'SHW',
 'OXY',
 'CL',
 'MU',
 'CME',
 'AON',
 'LRCX',
 'BSX',
 'EQIX',
 'TFC',
 'PXD',
 'CHTR',
 'CCI',
 'MET',
 'ATVI',
 'ICE',
 'MPC',
 'NSC',
 'DG',
 'GM',
 'EMR',
 'F',
 'KLAC',
 'MCO',
 'FCX',
 'KDP',
 'MNST',
 'MCK',
 'VLO',
 'ORLY',
 'ADM',
 'PSX',
 'PSA',
 'SRE',
 'SNPS',
 'MAR',
 'D',
 'GIS',
 'AEP',
 'AZO',
 'KHC',
 'APH',
 'HSY',
 'CNC',
 'CTVA',
 'EW',
 'CTAS',
 'A',
 'ROP',
 'JCI',
 'CDNS',
 'FDX',
 'NXPI',
 'AIG',
 'KMB',
 'AFL',
 'HES',
 'MSI',
 'PAYX',
 'DVN',
 'TRV',
 'BIIB',
 'DXCM',
 'SYY',
 'LHX',
 'RSG',
 'ENPH',
 'ECL',
 'ADSK',
 'MCHP',
 'ANET',
 'KMI',
 'CMG',
 'FTNT',
 'AJG',
 'STZ',
 'TT',
 'WMB',
 'MSCI',
 'O',
 'IQV',
 'TEL',
 'ROST',
 'PRU',
 'EXC',
 'PH',
 'FIS',
 'SPG',
 'COF',
 'NUE',
 'XEL',
 'HLT',
 'CARR',
 'PCAR',
 'BK',
 'NEM',
 'DOW',
 'EA',
 'WBA',
 'DD',
 'ALL',
 'YUM',
 'AMP',
 'CMI',
 'ILMN',
 'BF.B',
 'TDG',
 'IDXX',
 'ED',
 'KR',
 'ABC',
 'DLTR',
 'RMD',
 'ALB',
 'HAL',
 'NDAQ',
 'LVS',
 'ODFL',
 'WELL',
 'AME',
 'CSGP',
 'OTIS',
 'MTD',
 'SBAC',
 'ON',
 'VICI',
 'DLR',
 'CEG',
 'KEYS',
 'PPG',
 'WEC',
 'CTSH',
 'ROK',
 'GWW',
 'PCG',
 'HPQ',
 'FAST',
 'DFS',
 'MTB',
 'PEG',
 'OKE',
 'DHI',
 'APTV',
 'BKR',
 'GLW',
 'LYB',
 'ES',
 'BAX',
 'STT',
 'VRSK',
 'TROW',
 'WBD',
 'AWK',
 'IT',
 'GPN',
 'HRL',
 'FANG',
 'WTW',
 'RJF',
 'GPC',
 'IFF',
 'CDW',
 'TSCO',
 'FITB',
 'ARE',
 'URI',
 'ZBH',
 'K',
 'LEN',
 'EBAY',
 'EIX',
 'CBRE',
 'EFX',
 'VMC',
 'TSN',
 'HIG',
 'FTV',
 'WY',
 'EQR',
 'AVB',
 'MKC',
 'ETR',
 'LUV',
 'ULTA',
 'AEE',
 'MLM',
 'FE',
 'PFG',
 'FRC',
 'DTE',
 'DAL',
 'HBAN',
 'IR',
 'CTRA',
 'ANSS',
 'ACGL',
 'PPL',
 'RF',
 'VRSN',
 'LH',
 'EXR',
 'PWR',
 'CF',
 'CAH',
 'CFG',
 'XYL',
 'HPE',
 'EPAM',
 'DOV',
 'WAT',
 'WRB',
 'TDY',
 'PAYC',
 'ROL',
 'NTRS',
 'MRO',
 'CNP',
 'INVH',
 'CHD',
 'AES',
 'MOH',
 'JBHT',
 'MAA',
 'BBY',
 'CLX',
 'HOLX',
 'WAB',
 'DRI',
 'EXPD',
 'STE',
 'AMCR',
 'VTR',
 'IEX',
 'CAG',
 'CMS',
 'KEY',
 'MPWR',
 'BALL',
 'J',
 'BR',
 'GRMN',
 'PKI',
 'TTWO',
 'INCY',
 'FDS',
 'MOS',
 'SEDG',
 'CINF',
 'ABMD',
 'DGX',
 'WST',
 'ATO',
 'TRGP',
 'BRO',
 'SYF',
 'FOX',
 'FOXA',
 'NTAP',
 'FMC',
 'EQT',
 'OMC',
 'SJM',
 'LYV',
 'CPB',
 'HWM',
 'CPRT',
 'AVY',
 'IRM',
 'COO',
 'ALGN',
 'SWKS',
 'EXPE',
 'RCL',
 'ETSY',
 'APA',
 'GEN',
 'TXT',
 'LDOS',
 'LKQ',
 'TER',
 'PTC',
 'TRMB',
 'AKAM',
 'NVR',
 'UAL',
 'LNT',
 'FLT',
 'KIM',
 'ZBRA',
 'TYL',
 'DPZ',
 'JKHY',
 'MGM',
 'ESS',
 'L',
 'PEAK',
 'MTCH',
 'NDSN',
 'EVRG',
 'VTRS',
 'IPG',
 'BEN',
 'CBOE',
 'TECH',
 'SIVB',
 'VFC',
 'IP',
 'HST',
 'UDR',
 'POOL',
 'RE',
 'PARA',
 'SNA',
 'CPT',
 'LW',
 'PKG',
 'CRL',
 'SWK',
 'BIO',
 'WDC',
 'CHRW',
 'STX',
 'MAS',
 'GL',
 'CE',
 'REG',
 'NI',
 'BXP',
 'HSIC',
 'CCL',
 'TFX',
 'CZR',
 'NWS',
 'NWSA',
 'KMX',
 'EMN',
 'JNPR',
 'PHM',
 'CDAY',
 'ALLE',
 'QRVO',
 'BWA',
 'NRG',
 'MKTX',
 'WRK',
 'UHS',
 'FFIV',
 'AOS',
 'CMA',
 'AAL',
 'BBWI',
 'HII',
 'AAP',
 'TPR',
 'FRT',
 'IVZ',
 'PNW',
 'HAS',
 'WYNN',
 'FBHS',
 'SBNY',
 'DISH',
 'RHI',
 'WHR',
 'ZION',
 'CTLT',
 'PNR',
 'SEE',
 'RL',
 'NCLH',
 'DXC',
 'GNRC',
 'AIZ',
 'XRAY',
 'LNC',
 'DVA',
 'MHK',
 'OGN',
 'LUMN',
 'ALK',
 'NWL',
 'VNO',
 'TAP']


def load_csv(tickers: list, start:str, end:str):
    """
    Creating a function that would allow us to load a csv containing the Adj close, High, Low and volume of relevant tickers
    tickers should be a list
    date format :'YYYY-MM-DD'
    """
    csv = yf.download(tickers=tickers, start=start, end=end)
    csv.drop(columns='Close', inplace=True)
    csv = csv[1:].copy()

    return csv

def get_tickers():
    return tickers
