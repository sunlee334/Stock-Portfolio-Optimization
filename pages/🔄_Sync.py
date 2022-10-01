import streamlit as st
import pandas as pd
import os
import yfinance as yf

st.set_page_config(page_title="Portfolio", page_icon="📋")
st.markdown("# Sync")
st.sidebar.header("Sync")

dirname = os.path.dirname(__file__)
path_investment_portfolio = os.path.join(dirname, r'./../rawdata/investment_portfolio.xlsx')


def get_investment_portfolio():
    investment_portfolio = pd.read_excel(path_investment_portfolio)

    return investment_portfolio


def update_investment_portfolio():
    investment_portfolio = get_investment_portfolio()
    investment_portfolio = investment_portfolio.drop(columns='Value')

    ticker_list = investment_portfolio['Ticker'].to_string(index=False)

    adj_close_value = yf.download(ticker_list)['Adj Close'] \
        .iloc[-1] \
        .rename('Value') \
        .reset_index() \
        .rename(columns={'index': 'Ticker'})

    df = pd.merge(left=investment_portfolio, right=adj_close_value, on="Ticker")
    df.to_excel(path_investment_portfolio, index=False)

    return


if st.button('업데이트'):
    try:
        with st.spinner('정보를 가져오는 중...'):
            update_investment_portfolio()
        investment_portfolio = get_investment_portfolio()
        st.success('업데이트가 완료되었습니다!', icon="✅")
        st.dataframe(investment_portfolio)

    except:
        e = RuntimeError('This is an exception of type RuntimeError')
        st.exception(e)
else:
    investment_portfolio = get_investment_portfolio()
    st.dataframe(investment_portfolio)
