from fredapi import Fred

investment = 100
start_year = 2018
start_month = 1
start_day = 1
start_date = str(start_year) + '-' + str(start_month) + '-' + str(start_day)
end_year = 2022
end_month = 1
end_day = 1

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
    'BHP',  # BHP Group Limited
    'LIN'  # Linde plc
]
communication_services = [
    'GOOGL'  # Alphabet Inc.
]
consumer_cyclical = [
    'AMZN',  # Amazon.com, Inc.
    'TSLA'  # Tesla, Inc.
]
consumer_defensive = [
    'WMT',  # Walmart Inc.
    'PG',  # The Procter & Gamble Company
    'CMG'  # Chipotle Mexican Grill, Inc.
]
energy = [
    'XOM',  # Exxon Mobil Corporation
    'CVX'  # Chevron Corporation
]
financial_services = [
    'BRK-B'  # Berkshire Hathaway Inc.
]
healthcare = [
    'UNH',  # UnitedHealth Group Incorporated
    'JNJ'  # Johnson & Johnson
]
industrials = [
    'UPS',  # United Parcel Service, Inc.
    'RTX'  # Raytheon Technologies Corporation
]
real_estate = [
    'AMT',  # American Tower Corporation
    'PLD',  # Prologis, Inc.
    'EQIX'  # Equinix, Inc.
]
technology = [
    'AAPL',  # Apple Inc.
    'MSFT'  # Microsoft Corporation
]
utilities = [
    'NEE',  # NextEra Energy, Inc.
    'SO'  # The Southern Company
]

sectors = basic_materials + \
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
etfs = [
    'BOTZ',  # Global X Robotics & Artificial Intelligence ETF
    'SCHD',  # SCHWAB US DIVIDEND EQUITY ETF
    'VOO',  # VANGUARD S&P 500 ETF
    'VTI'  # VANGUARD TOTAL STOCK MARKET ETF
]

tickers = etfs + sectors

# FRED API
fred = Fred(api_key='b196e1fce34e1b65061828a431424b6d')

sp500 = fred.get_series('SP500', observation_start=start_date)
rate_10y = fred.get_series('DGS10', observation_start=start_date)
rate_2y = fred.get_series('DGS2', observation_start=start_date)
rate_3m = fred.get_series('DGS3MO', observation_start=start_date)
continued_claims = fred.get_series('CCSA', observation_start=start_date)
funds = fred.get_series('FEDFUNDS', observation_start=start_date)