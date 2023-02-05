import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt

from data import collect_data, list_us_stocks, get_possible_tickers
from visuals import create_treemap
from firestore_helpers import User, Transaction, CREDENTIALS

USER_ID = '1b57fe1d-5fd5-4a13-b8e3-82bfbb1e8c42'

def ord(n):
    # Used for date formatting
    # source: https://stackoverflow.com/a/16671271/17774866
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

today = dt.date.today().strftime('%A, %b. ') + ord(int(dt.date.today().strftime('%-d')))

user = User(USER_ID)


st.header(f'Market Volatility for {today}.')
st.subheader('created by Marc Muszik and John Black')

stock_list = get_possible_tickers()


#Use the session state to persist data between page refreshes
if 'historical_data' not in st.session_state:
    st.session_state['historical_data'], st.session_state['company_data'] = collect_data(stock_list)

fig = create_treemap(
    st.session_state['historical_data'], 
    st.session_state['company_data'] 
    )

st.plotly_chart(fig, theme=None, use_container_width=True)

st.caption('This plot charts the current volatility of individual shares from 500 publicly traded companies compared to their historical volatility. Data is sourced from Yahoo Finance.')