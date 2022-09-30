import streamlit as st
import pandas as pd
import os

dirname = os.path.dirname(__file__)

investment_portfolio = os.path.join(dirname, r'./../rawdata/investment_portfolio.xlsx')


st.set_page_config(page_title="Portfolio", page_icon="📋")

st.markdown("# Portfolio")
st.sidebar.header("Portfolio")

st.write("모든 투자자는 그들만의 포트폴리오 전략이 있을 수 있습니다. 상황에 따라 다른 전략과 투자 시나리오가 반영됩니다.")
st.write("각자의 성향이 반영되었을 뿐 옳고 그름을 구별할 수는 없습니다.")

df = pd.read_excel(investment_portfolio)
df
