investment = 100
start_year = 2022
start_month = 1
start_day = 1
start_date = str(start_year) + '-' + str(start_month) + '-' + str(start_day)
# start_date = '2021-01-01'
end_year = 2022
end_month = 1
end_day = 1
fred_api_key = 'b196e1fce34e1b65061828a431424b6d'

industry_list = [
    'Basic Materials',
    'Communication Services',
    'Consumer Cyclical',
    'Consumer Defensive',
    'Energy',
    'Financial Services',
    'Healthcare',
    'Industrials',
    'Real Estate',
    'Technology',
    'Utilities'
]

basic_materials = [
]
communication_services = [
    'IRDM',  # Iridium Communications Inc.
    'GOOGL'  # Alphabet Inc.
]
consumer_cyclical = [
    'AMZN',  # Amazon.com, Inc.
    'TSLA'  # Tesla, Inc.
]
consumer_defensive = [
    # 'WMT',  # Walmart Inc.
    'MCD',  # McDonald's Corporation
    # 'KO'  # The Coca-Cola Company
]
energy = [
]
financial_services = [
]
healthcare = [
    'UNH',  # UnitedHealth Group Incorporated
    # 'JNJ'  # Johnson & Johnson
]
industrials = [
    'LMT'  # Lockheed Martin Corporation
]
real_estate = [
    'AMT',  # American Tower Corporation
    'PLD',  # Prologis, Inc.
    'EQIX'  # Equinix, Inc.
]
technology = [
    'AAPL',  # Apple Inc.
    'AMD',  # Advanced Micro Devices, Inc.
    'TXN',  # Texas Instruments Incorporated
    'MSFT',  # Microsoft Corporation
    'NVDA'  # NVIDIA Corporation
]
utilities = [
    'NEE',  # NextEra Energy, Inc.
]

sector_list = basic_materials + \
              communication_services + \
              consumer_cyclical + \
              consumer_defensive + \
              energy + \
              financial_services + \
              healthcare + \
              industrials + \
              real_estate + \
              technology + \
              utilities
etf_list = [
    'SCHD',  # SCHWAB US DIVIDEND EQUITY ETF
    'VOO'  # Vanguard 500 Index Fund
]

leverage_list = [
    'TQQQ',  # ProShares UltraPro QQQ
    'SOXL'  # Direxion Daily Semiconductor Bull 3X Shares
]

ticker_list = etf_list + sector_list + leverage_list

fred_tickers = {
    'CPI': 'MEDCPIM158SFRBCLE',  # Median Consumer Price Index
    'CC': 'CCSA',  # Continued Claims
    'AHE': 'CES0500000003',  # Average Hourly Earnings of All Employees, Total Private
    'TS10': 'DGS10',
    # Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis
    'FUNDS': 'DFF',  # Federal Funds Effective Rate
    'USD-KRW': 'DEXKOUS'  # South Korean Won to U.S. Dollar Spot Exchange Rate
}
