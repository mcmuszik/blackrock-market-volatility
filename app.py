import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as date
import streamlit.components.v1 as components


tab1, tab2 = st.tabs(["Personal", "Performance"])

with tab1:
    today = date.date.today().strftime('%m/%d/%Y')

    with st.container():
        st.header(f'Market Volatility {today} ' + '📈')
        st.subheader('created by Marc Muszik and John Black')

    # from data import collect_data, list_us_stocks
    # from visuals import create_treemap





        df = pd.DataFrame(
        np.random.randn(50, 5),
        columns=('col %d' % i for i in range(5)))

        st.dataframe(df, height=350, width=1000)

        def make_or_break(value=0):
            if value < 0:
                print("😭")
            elif value > 0:
                print("🤑")
        with st.container():
            st.subheader('See your transaction history 👇')
            col1, col2 , col3, col4= st.columns(4)
        with st.container():
                with col1:
                    option = st.selectbox(
                    'Stock Ticker',
                    ('DG', 'AMZN', 'APPL'))

                with col2:
                    number = st.number_input('Volume', max_value=100000, min_value=0, step=1)

                with col3:
                    st.date_input(label="Date")

                with col4:
                    st.text('')
                    st.text('')
                    st.button(label="save transaction")

                st.write('You selected:', option)

    with tab2:
        # stock_list = list_us_stocks(n=500)
        # #Use the session state to persist data between page refreshes
        # if 'historical_data' not in st.session_state:
        #     st.session_state['historical_data'], st.session_state['company_data'] = collect_data(stock_list)

        # fig = create_treemap(
        #     st.session_state['historical_data'], 
        #     st.session_state['company_data'] 
        #     )

        # st.plotly_chart(fig, theme=None, use_container_width=True)

        st.caption('This plot charts the current volatility of individual shares from 500 publicly traded companies compared to their historical volatility. Data is sourced from Yahoo Finance.')

        make_or_break(value=-5)
        make_or_break(value=5)

