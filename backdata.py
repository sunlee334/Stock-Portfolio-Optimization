investment = 100
start_year = 2018
start_month = 1
start_day = 1
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
