import streamlit as st
import pandas as pd
import os
import yfinance as yf

st.set_page_config(page_title="Portfolio", page_icon="π")
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


if st.button('μλ°μ΄νΈ'):
    try:
        with st.spinner('μ λ³΄λ₯Ό κ°μ Έμ€λ μ€...'):
            update_investment_portfolio()
        investment_portfolio = get_investment_portfolio()
        st.success('μλ°μ΄νΈκ° μλ£λμμ΅λλ€!', icon="β")
        st.dataframe(investment_portfolio)

    except:
        e = RuntimeError('This is an exception of type RuntimeError')
        st.exception(e)
else:
    investment_portfolio = get_investment_portfolio()
    st.dataframe(investment_portfolio)
