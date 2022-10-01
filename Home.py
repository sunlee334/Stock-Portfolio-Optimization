# -*- coding: utf-8 -*-

# https://sunlee334-stock-portfolio-optimization-app-cgekqm.streamlitapp.com/
# streamlit run Home.py

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import altair as alt
import plotly.express as px

from datetime import datetime
from stqdm import stqdm
from backdata import start_year, start_month, start_day
from backdata import sector_list, etf_list, leverage_list, ticker_list, fred_tickers
from backdata import fred_api_key
from fredapi import Fred

st.set_page_config(page_title="Sun's Stock Portfolio Optimizer", page_icon="📈")
st.title("Sun's Stock Portfolio Optimizer")

st.sidebar.markdown("# Main page 🎈")


def fred_processing(ticker, start_date, column_name):
    data = pd.DataFrame(fred.get_series(fred_tickers[ticker], observation_start=start_date))
    data.index = data.index.strftime('%Y-%m-%d')
    data.rename(columns={0: column_name}, inplace=True)
    data = pd.DataFrame(data)
    return data


def yf_stock_processing(ticker, start_date, end_date, column_name):
    data = yf.Ticker(ticker).history(start=start_date, end=end_date).dropna(how="all")
    data.index = data.index.strftime('%Y-%m-%d')
    data.rename(columns={'Close': column_name}, inplace=True)
    data = pd.DataFrame(data[column_name])
    return data


def yf_stocks_processing(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close'].dropna(how="all")
    data.index = data.index.strftime('%Y-%m-%d')
    for ticker in tickers:
        data.rename(columns={ticker: ticker}, inplace=True)
    return data


def variance_last(data):
    data = float((data.iloc[-1].values - data.iloc[-2].values) / data.iloc[-2].values * 100)
    return data


def variance_init(data):
    data = float((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100)
    return data


def get_tickers(ticker_list, start_date, end_date):
    tickers = yf_stocks_processing(tickers=ticker_list, start_date=start_date, end_date=end_date)

    return tickers


def set_portfolio_fig(ticker_list, tickers_data):
    tickers_string = ', '.join(ticker_list).upper().replace(",", ", ")
    # Display everything on Streamlit
    st.caption("Your Portfolio Consists of \n{}".format(tickers_string))
    st.metric(label="Total", value="$ " + "{:,.2f}".format(tickers_data.iloc[-1].sum()))

    daily_ret = tickers_data.pct_change()  # 종목 수정 종가데이터의 일별주가상승률
    annual_ret = daily_ret.mean() * 252  # 연평균 주가상승률
    daily_cov = daily_ret.cov()  # 일별주가상승률의 공분산행렬
    annual_cov = daily_cov * 252  # 공분산행렬과 영업일 수의 곱

    port_ret = []  # 포트폴리오의 일별주가상승률
    port_risk = []  # 리스크
    port_weights = []  # 비중
    sharpe_ratio = []

    for _ in stqdm(range(10000)):  # 임의로 만들 포트폴리오
        weights = np.random.random(len(ticker_list))
        weights /= np.sum(weights)  # 임의의 가중치를 랜덤으로 부여

        returns = np.dot(weights, annual_ret)  # 가중치와 연 수익률 행렬과 내적을 실시
        risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))  # 포트폴리오의 변동성의 기댓값을 산출

        port_ret.append(returns)
        port_risk.append(risk)
        port_weights.append(weights)
        sharpe_ratio.append(returns / risk)

    portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
    for i, s in enumerate(stqdm(ticker_list)):
        portfolio[s] = [weight[i] for weight in port_weights]
    stocks = pd.DataFrame(portfolio)
    stocks = stocks[['Returns', 'Risk', 'Sharpe'] + [s for s in ticker_list]]

    # min_risk = stocks.loc[stocks['Risk'] == stocks['Risk'].min()] * 100  # Low Risk
    max_sharpe = stocks.loc[stocks['Sharpe'] == stocks['Sharpe'].max()] * 100  # Max Sharpe
    weight_dict = dict(zip(list(max_sharpe[ticker_list].columns),
                           max_sharpe[ticker_list].values.flatten().tolist()))

    ticker_value_df = tickers_data.rename(index={tickers_data.index[-1]: 'Value'})
    ticker_value_df = pd.DataFrame(ticker_value_df.iloc[-1]).reset_index()
    ticker_value_df.rename(columns={'index': 'Ticker Name'}, inplace=True)

    stock_per_df = pd.DataFrame(pd.Series(weight_dict)).reset_index()
    stock_per_df.rename(columns={'index': 'Ticker Name'}, inplace=True)
    stock_per_df.rename(columns={0: 'Ticker % in Portfolio'}, inplace=True)

    df = ticker_value_df.merge(stock_per_df, on='Ticker Name', how='outer')
    df = df.sort_values(by='Ticker % in Portfolio', ascending=False)

    st.table(df.style.format({'Value': '{:.2f}', 'Ticker % in Portfolio': "{:.1f}" + ' %'}))

    df = ((tickers_data.pct_change() + 1).cumprod())

    fig = px.line(df, x=df.index, y=ticker_list)

    return fig


fred = Fred(api_key=fred_api_key)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(start_year, start_month, start_day))
with col2:
    end_date = st.date_input("End Date")  # it defaults to current date

# FRED
CPI = fred_processing(ticker='CPI', start_date=start_date, column_name='Consumer Price Index')
CC = fred_processing(ticker='CC', start_date=start_date, column_name='Continued Claims')
AHE = fred_processing(ticker='AHE', start_date=start_date, column_name='Average Hourly Earnings')
TS10 = fred_processing(ticker='TS10', start_date=start_date, column_name='Treasury Securities at 10-Year')
FUNDS = fred_processing(ticker='FUNDS', start_date=start_date, column_name='Federal Funds')
KRW = fred_processing(ticker='USD-KRW', start_date=start_date, column_name='USD-KRW')

# Yahoo Finance
BTC = yf_stock_processing(ticker='BTC-USD', start_date=start_date, end_date=end_date, column_name='BTC')
SP500 = yf_stock_processing(ticker='^GSPC', start_date=start_date, end_date=end_date, column_name='S&P500')
NASDAQ = yf_stock_processing(ticker='^IXIC', start_date=start_date, end_date=end_date, column_name='NASDAQ')

st.header("Economic Indicator")
score_tab, data_tab, chart_tab = st.tabs(['💯 Score', '🗃 Data', '📈 Chart'])

with score_tab:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="S&P500 (3,400 이하)", value="{:,.2f}".format(SP500.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(SP500))) + '%')
        st.metric(label="NASDAQ (10,500 이하)", value="{:,.2f}".format(NASDAQ.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(NASDAQ))) + '%')
        st.metric(label="BTC", value="{:,.2f}".format(BTC.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(BTC))) + '%')
    with col2:
        st.metric(label="CPI (2% 이하)", value="{:,.2f}".format(CPI.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(CPI))) + '%')
        st.metric(label="Continued Claims (3,500K 이상)", value="{:,.0f}".format(CC.iloc[-1][0] // 1000) + 'K',
                  delta=str("{:,.2f}".format(variance_last(CC))) + '%')
        st.metric(label="Average Hourly Earnings", value="{:,.2f}".format(AHE.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(AHE))) + '%')
    with col3:
        st.metric(label="USD-KRW", value="{:,.2f}".format(KRW.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(KRW))) + '%')
        st.metric(label="Treasury Securities at 10-Year (4% 이상)", value="{:,.2f}".format(TS10.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(TS10))) + '%')
        st.metric(label="Federal Funds (4.6% 목표)", value="{:,.2f}".format(FUNDS.iloc[-1][0]),
                  delta=str("{:,.2f}".format(variance_last(FUNDS))) + '%')

with data_tab:
    col1, col2, col3 = st.columns(3)
    with col1:
        data = SP500.join(NASDAQ, how='outer').join(BTC, how='outer').join(KRW, how='outer').dropna()
        st.dataframe(data.style.format("{:.2f}"))
    with col2:
        data = CPI.join(AHE, how='outer').join(FUNDS, how='outer').dropna()
        st.dataframe(data.style.format("{:.2f}"))
    with col3:
        st.dataframe(TS10.dropna().style.format("{:.2f}"))

with chart_tab:
    # S&P500 vs. NASDAQ vs. BTC
    source = SP500.join(NASDAQ, how='outer').join(BTC, how='outer').dropna().reset_index()
    base = alt.Chart(source).encode(
        alt.X('Date:T', axis=alt.Axis(title=None))
    )
    SP500 = base.mark_line(color='red', tooltip=True).encode(
        alt.Y('S&P500:Q', title='S&P500'),
    )
    NASDAQ = base.mark_line(color='blue', tooltip=True).encode(
        alt.Y('NASDAQ:Q', title='NASDAQ')
    )
    chart = alt.layer(
        SP500 + NASDAQ,
        base.mark_line(color='green', tooltip=True).encode(alt.Y('BTC:Q', title='BTC')),
    ).resolve_scale(y='independent').interactive()
    st.altair_chart(chart, use_container_width=True)

    # USD-KRW
    st.line_chart(KRW)
    # CPI
    st.bar_chart(CPI)
    # Continued Claims
    st.bar_chart(CC)
    # Average Hourly Earnings
    st.line_chart(AHE)
    # Treasury Securities at 10-Year
    st.line_chart(TS10)
    # Federal Funds
    st.bar_chart(FUNDS)

st.warning("Don't fight the Fed", icon="⚠️")

# st.header("Portfolio")
# summary_tab, stock_tab, etf_tab, leverage_tab = st.tabs(['🚀 Summary', '📈 Stock', '🏛️ ETF', '💰 Leverage'])
#
# with summary_tab:
#     tickers_data = get_tickers(ticker_list, start_date, end_date)
#     fig = set_portfolio_fig(ticker_list, tickers_data.dropna(axis=0))
#     st.plotly_chart(fig, use_container_width=True)
#
# with stock_tab:
#     stocks_data = get_tickers(sector_list, start_date, end_date)
#     fig = set_portfolio_fig(sector_list, stocks_data.dropna(axis=0))
#     st.plotly_chart(fig, use_container_width=True)
#
# with etf_tab:
#     etfs_data = get_tickers(etf_list, start_date, end_date)
#     fig = set_portfolio_fig(etf_list, etfs_data.dropna(axis=0))
#     st.plotly_chart(fig, use_container_width=True)
#
# with leverage_tab:
#     leverages_data = get_tickers(leverage_list, start_date, end_date)
#     fig = set_portfolio_fig(leverage_list, leverages_data.dropna(axis=0))
#     st.plotly_chart(fig, use_container_width=True)
#
# st.header("수익률 확인")
# # 수익률 확인
# columns = list(tickers_data.columns.values)
#
# tickers = []
# values = []
# variance = []
#
# for i in range(len(columns)):
#     ticker_data = [tickers_data.dropna(axis=0)[columns[i]]][0]
#     tickers.append(columns[i])
#     values.append(ticker_data.iloc[-1])
#     variance.append(variance_init(ticker_data))
#
#     # st.metric(label=str(columns[i]), value="{:,.2f}".format(ticker_data.iloc[-1]),
#     #           delta=str("{:,.2f}".format(variance_init(ticker_data))) + '%')
#
# df = pd.DataFrame({'Tickers': tickers,
#                    'Values': values,
#                    'Variance': variance})
#
# st.dataframe(df.style.format({
#     'Values': "{:.2f}",
#     'Variance': "{:.2f}" + '%'
# }))
