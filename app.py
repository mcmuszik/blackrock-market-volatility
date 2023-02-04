import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as date

from data import collect_data, list_us_stocks
from visuals import create_treemap

today = date.date.today().strftime('%m/%d/%Y')

st.header(f'Market Volatility {today}')
st.subheader('created by Marc Muszik and John Black')

stock_list = list_us_stocks(n=500)
historical_data, company_data = collect_data(stock_list)
fig = create_treemap(historical_data, company_data )

st.plotly_chart(fig, theme=None, use_container_width=True)

st.caption('This plot charts the current volatility of individual shares from 500 publicly traded companies compared to their historical volatility. Data is sourced from Yahoo Finance.')