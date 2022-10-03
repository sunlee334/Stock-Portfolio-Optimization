import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="Portfolio", page_icon="📋")
st.markdown("# Portfolio")
st.sidebar.header("Portfolio")

dirname = os.path.dirname(__file__)

investment_portfolio = os.path.join(dirname, r'./../rawdata/investment_portfolio.xlsx')
investment_portfolio = pd.read_excel(investment_portfolio)

market_value = investment_portfolio['Hold'] * investment_portfolio['Value']
market_value = market_value.sum()

st.metric(label='총 자산', value='$' + "{:,.2f}".format(market_value))

investment_portfolio
ticker = investment_portfolio['Ticker']
company = investment_portfolio['Company']
sector = investment_portfolio['Sector']
value = investment_portfolio['Value']
hold = investment_portfolio['Hold']

source = pd.DataFrame({'Ticker': ticker,
                       'Company': company,
                       'Sector': sector,
                       'Value': value,
                       'Hold': hold,
                       })

# base = alt.Chart(source).encode(
#     theta=alt.Theta("Hold:Q", stack=True),
#     color=alt.Color("Ticker:N"),
#     tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
# )
#
# pie = base.mark_arc(outerRadius=120)
# text = base.mark_text(radius=140, size=20).encode(text="Ticker:N")

chart = (
    alt.Chart(source)
    .mark_arc()
    .encode(
        theta=alt.Theta('Hold:Q'),
        color=alt.Color('Ticker:N'),
        tooltip=['Ticker', 'Company', 'Sector', 'Value', 'Hold']
    )
)

st.altair_chart(chart, use_container_width=True)
