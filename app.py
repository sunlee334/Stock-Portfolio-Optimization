# -*- coding: utf-8 -*-

# https://medium.datadriveninvestor.com/build-your-own-stock-portfolio-optimizer-web-app-with-streamlit-be8654ef8c65
# streamlit run app.py

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

from plotly.subplots import make_subplots
from datetime import datetime
from stqdm import stqdm
from backdata import investment
from backdata import start_year, start_month, start_day
from backdata import tickers as init_tickers
from backdata import sectors as init_sectors
from backdata import etfs as init_etfs
from backdata import fred_api_key
from collections import OrderedDict
from fredapi import Fred

fred = Fred(api_key=fred_api_key)

st.set_page_config(page_title="Sun's Stock Portfolio Optimizer", layout="wide")
st.title("Sun's Stock Portfolio Optimizer")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(start_year, start_month, start_day))
with col2:
    end_date = st.date_input("End Date")  # it defaults to current date

# 겅제 지표
continued_claims = pd.DataFrame(fred.get_series('CCSA', observation_start=start_date))
continued_claims.index = continued_claims.index.strftime('%Y-%m-%d')
continued_claims.rename(columns={0: 'Continued Claims'}, inplace=True)

average_hourly_earnings = pd.DataFrame(fred.get_series('CES0500000003', observation_start=start_date))
average_hourly_earnings.index = average_hourly_earnings.index.strftime('%Y-%m-%d')
average_hourly_earnings.rename(columns={0: 'Average Hourly Earnings'}, inplace=True)

rate_10y = pd.DataFrame(fred.get_series('DGS10', observation_start=start_date))
rate_10y.index = rate_10y.index.strftime('%Y-%m-%d')
rate_10y.rename(columns={0: 'Rate 10Y'}, inplace=True)

funds = pd.DataFrame(fred.get_series('FEDFUNDS', observation_start=start_date))
funds.index = funds.index.strftime('%Y-%m-%d')
funds.rename(columns={0: 'Funds'}, inplace=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("실업 청구: " +
                 str("{:,.0f}".format(continued_claims.iloc[-1].values[0] // 1000)) + 'K' + ' (3,500K 이상시 매수)')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=continued_claims.index,
                             y=continued_claims['Continued Claims'],
                             name='실업 청구'))
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("평균 임금: " +
                 '$' + str("{:.2f}".format(average_hourly_earnings.iloc[-1].values[0])))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=average_hourly_earnings.index,
                             y=average_hourly_earnings['Average Hourly Earnings'],
                             name='평균 임금'))
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("10년물 금리: " +
                 str("{:.2f}".format(rate_10y.iloc[-1].values[0])) + '%' + ' (4% 이상시 매수)')
with col2:
    st.subheader("기준 금리: " +
                 str("{:.2f}".format(funds.iloc[-1].values[0])) + '%')
fig = go.Figure()
fig.add_trace(go.Scatter(x=rate_10y.index,
                         y=rate_10y['Rate 10Y'],
                         name='10년물 금리'))
fig.add_trace(go.Scatter(x=funds.index,
                         y=funds['Funds'],
                         name='기준 금리'))
st.plotly_chart(fig, use_container_width=True)

# NASDAQ vs. S&P500 vs. BTC
st.header('BTC vs. S&P500 vs. NASDAQ')

col1, col2, col3 = st.columns(3)
with col1:
    df = yf.Ticker('BTC-USD').history(start=start_date, end=end_date)
    df.rename(columns={'Close': 'BTC-USD'}, inplace=True)
    df = df.dropna(how="all")
    df.index = df.index.strftime('%Y-%m-%d')
    st.subheader('BTC-USD: $' + str("{:,.2f}".format(df['BTC-USD'].iloc[-1])))
    fig = px.line(df, x=df.index, y=df['BTC-USD'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df = yf.Ticker('^GSPC').history(start=start_date, end=end_date)
    df.rename(columns={'Close': 'S&P500'}, inplace=True)
    df = df.dropna(how="all")
    df.index = df.index.strftime('%Y-%m-%d')
    st.subheader('S&P500: $' + str("{:,.2f}".format(df['S&P500'].iloc[-1])) + ' (3,500 이하시 매수)')
    fig = px.line(df, x=df.index, y=df['S&P500'])
    st.plotly_chart(fig, use_container_width=True)

with col3:
    df = yf.Ticker('^IXIC').history(start=start_date, end=end_date)
    df.rename(columns={'Close': 'NASDAQ'}, inplace=True)
    df = df.dropna(how="all")
    df.index = df.index.strftime('%Y-%m-%d')
    st.subheader('NASDAQ: $' + str("{:,.2f}".format(df['NASDAQ'].iloc[-1])))
    fig = px.line(df, x=df.index, y=df['NASDAQ'])
    st.plotly_chart(fig, use_container_width=True)

st.subheader('Fair Comparison')
df = yf.download(['BTC-USD', '^GSPC', '^IXIC'], start=start_date, end=end_date)['Adj Close'].dropna(how="all")
df.index = df.index.strftime('%Y-%m-%d')
df.rename(columns={'^GSPC': 'S&P500'}, inplace=True)
df.rename(columns={'^IXIC': 'NASDAQ'}, inplace=True)
df = 1 + df.dropna().pct_change()
df = df.cumprod()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['BTC-USD'], name='BTC-USD'))
fig.add_trace(go.Scatter(x=df.index, y=df['S&P500'], name='S&P500'))
fig.add_trace(go.Scatter(x=df.index, y=df['NASDAQ'], name='NASDAQ'))

st.plotly_chart(fig, use_container_width=True)

# Tickers
init_tickers_string = ', '.join(init_tickers)
init_sectors_string = ', '.join(init_sectors)
init_etfs_string = ', '.join(init_etfs)

sectors_string = st.text_input(
    'Enter all stock tickers to be included in portfolio separated by commas, e.g. "AAPL, AMZN"',
    init_sectors_string).upper().replace(" ", "")
sectors = sectors_string.split(',')

investment = int(st.text_input('Enter your investment($)', investment))

if sectors[0] == '':
    df = yf.download(init_sectors, start=start_date, end=end_date)['Adj Close'].dropna(how="all")
else:
    df = yf.download(sectors, start=start_date, end=end_date)['Adj Close'].dropna(how="all")

df.index = df.index.strftime('%Y-%m-%d')
st.dataframe(df.style.format("{:.2f}"))

# Display everything on Streamlit
if sectors[0] == '':
    st.subheader("Your Portfolio Consists of \n{}".format(init_sectors_string))
else:
    st.subheader("Your Portfolio Consists of \n{}".format(sectors_string))

daily_ret = df.pct_change()  # 종목 수정 종가데이터의 일별주가상승률
annual_ret = daily_ret.mean() * 252  # 연평균 주가상승률
daily_cov = daily_ret.cov()  # 일별주가상승률의 공분산행렬
annual_cov = daily_cov * 252  # 공분산행렬과 영업일 수의 곱

port_ret = []  # 포트폴리오의 일별주가상승률
port_risk = []  # 리스크
port_weights = []  # 비중
sharpe_ratio = []

for _ in stqdm(range(10000)):  # 임의로 만들 포트폴리오
    weights = np.random.random(len(sectors))
    weights /= np.sum(weights)  # 임의의 가중치를 랜덤으로 부여

    returns = np.dot(weights, annual_ret)  # 가중치와 연 수익률 행렬과 내적을 실시
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))  # 포트폴리오의 변동성의 기댓값을 산출

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns / risk)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
for i, s in enumerate(stqdm(sectors)):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in sectors]]
df

min_risk = df.loc[df['Risk'] == df['Risk'].min()]  # Low Risk
max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]  # Max Sharpe

fig = go.Figure()

fig.add_trace(go.Scattergl(
    x=df['Risk'],
    y=df['Returns'],
    name='Sharpe',
    mode='markers',
    marker=dict(
        color=np.random.randn(),
        colorscale='Viridis',
        line_width=1
    )
))

fig.add_trace(go.Scattergl(
    x=min_risk['Risk'],
    y=min_risk['Returns'],
    name='Min Risk',
    mode='markers',
    marker=dict(
        size=20,
        color=np.random.randn(),
        colorscale='Viridis',
        line_width=1
    )
))

fig.add_trace(go.Scattergl(
    x=max_sharpe['Risk'],
    y=max_sharpe['Returns'],
    name='Max Sharpe',
    mode='markers',
    marker=dict(
        size=20,
        color=np.random.randn(),
        colorscale='Viridis',
        line_width=1
    )
))

# Plot!
st.plotly_chart(fig, use_container_width=True)
st.header('Min Risk')
st.subheader('Returns: ' + str(round(float(min_risk['Returns'].values[0]), 2)))
st.subheader('Risk: ' + str(round(float(min_risk['Risk'].values[0]), 2)))
min_risk

st.header('Max Sharpe')
st.subheader('Returns: ' + str(round(float(max_sharpe['Returns'].values[0]), 2)))
st.subheader('Risk: ' + str(round(float(max_sharpe['Risk'].values[0]), 2)))
max_sharpe

stock_weight_dict = dict(zip(list(max_sharpe[sectors].columns),
                             max_sharpe[sectors].values.flatten().tolist()))
weights = OrderedDict(stock_weight_dict)

df = pd.Series(weights)
df = pd.DataFrame(df).transpose()
df
