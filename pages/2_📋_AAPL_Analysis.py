import os
from os.path import isfile, join
from os import listdir
import pathlib
import streamlit as st
import quantstats as qs
import streamlit.components.v1 as components

st.set_page_config(page_title="Apple Analysis", page_icon="📋", layout="wide")
st.markdown("# Portfolio Analysis")
st.sidebar.header("Portfolio Analysis")

# get current directory
# path = os.getcwd()
# path
# # parent directory
# parent = os.path.dirname(path)
# parent
#
# dirname = os.path.dirname(__file__)
# dirname

parent_path = pathlib.Path(__file__).parent.parent.resolve()
parent_path
data_path = os.path.join(parent_path, "aapl")
data_path


stock = qs.utils.download_returns('SPY')
os.getcwd()
qs.reports.html(stock, "SPY", title='AAPL vs SPY', output=data_path)
# qs.reports.html(stock, benchmark="SPY",
#                 title='AAPL vs SPY',
#                 output='aapl.html')

path_to_html = "./reports/aapl.html"

# Read file and keep in variable
html_data = open(path_to_html, 'r').read()

## Show in webpage
components.html(html_data, height=5000)
