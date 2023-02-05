import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
import datetime as dt
from data import get_possible_tickers, get_company_data, get_price_data
from visuals import create_treemap
from firestore_helpers import User, Transaction

#Assume a certain logged-in user
USER_ID = 'bbbf58ba-823f-4a8c-8007-f22960e83448'
user = User(USER_ID)

def on_button_click(ticker, volume, date) -> None:
    new_transaction = [Transaction(ticker, volume, is_purchase=True, datetime=date)]
    user.update_transactions(new_transaction)


def ord(n):
    # Used for date formatting
    # source: https://stackoverflow.com/a/16671271/17774866
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

today = dt.date.today().strftime('%A, %b. ') + ord(int(dt.date.today().strftime('%-d')))


tab1, tab2 = st.tabs(["Individual Performance", "Market Volatility"])

with tab1:
    with st.container():
        st.header(f'Portfolio Performance for {today} ' + '📈')
        st.write('created by Marc Muszik and John Black')

        portfolio = user.portfolio_value()
        portfolio_plot = px.line(portfolio, x='Date', y='value')
        st.subheader('Portfolio Performance Over Time')
        st.plotly_chart(portfolio_plot, theme=None, use_container_width=True)
    
    # from data import collect_data, list_us_stocks
    # from visuals import create_treemap

    df = user.get_transactions_df()

    st.subheader('Portfolio Makeup')
    st.dataframe(df, height=350, width=1000)

    def make_or_break(value=0):
        if value < 0:
            print("😭")
        elif value > 0:
            print("🤑")

    with st.container():
        st.subheader('Add a new transaction 👇')
        col1, col2 , col3, col4= st.columns(4)

    with st.container():
            with col1:
                ticker = st.selectbox(
                'Stock Ticker',
                tuple(get_possible_tickers()))

            with col2:
                volume = st.number_input('Volume', max_value=100000, min_value=0, step=1)

            with col3:
                date = st.date_input(label="Date")

            with col4:
                st.text('')
                st.text('')
                st.button(label="save transaction", on_click=on_button_click)

    with tab2:
        
        st.header("Market Volatility Chart")
        st.write("This is where the market volatility chart is")

        fig = create_treemap()

        st.plotly_chart(fig, theme=None, use_container_width=True)

    st.caption('This plot charts the current volatility of individual shares from 500 publicly traded companies compared to their historical volatility. Data is sourced from Yahoo Finance.')

    make_or_break(value=-5)
    make_or_break(value=5)
