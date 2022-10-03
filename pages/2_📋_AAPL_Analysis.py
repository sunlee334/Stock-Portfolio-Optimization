import os

import streamlit as st
import quantstats as qs
import streamlit.components.v1 as components

st.set_page_config(page_title="Apple Analysis", page_icon="📋", layout="wide")
st.markdown("# Portfolio Analysis")
st.sidebar.header("Portfolio Analysis")

dirname = os.path.dirname(__file__)
investment_portfolio = os.path.join(dirname, r'./../reports/aapl.html')
investment_portfolio

stock = qs.utils.download_returns('AAPL')
qs.reports.html(stock, "SPY", title='AAPL vs SPY', output=investment_portfolio)
# qs.reports.html(stock, benchmark="SPY",
#                 title='AAPL vs SPY',
#                 output='aapl.html')

path_to_html = "./reports/aapl.html"

# Read file and keep in variable
html_data = open(path_to_html, 'r').read()

## Show in webpage
components.html(html_data, height=5000)
