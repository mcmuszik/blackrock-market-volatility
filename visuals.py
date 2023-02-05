import numpy as np
import datetime as dt
import pandas as pd
import plotly
import plotly.express as px

from data import DATASET
from firestore_helpers import CREDENTIALS


def show_moving_average_comparison(ticker) -> plotly.graph_objs._figure.Figure:
    price_data = pd.read_gbq(f'select * from {DATASET}.prices')
    fig = px.line(
        price_data.query(f'ticker == "{ticker}"'), 
        x=price_data.query(f'ticker == "{ticker}"').index, 
        y=['long_term_ma', 'short_term_ma']
        )
    return fig


def create_treemap() -> plotly.graph_objs._figure.Figure:
    company_info = pd.read_gbq(f'select industry, sector, industry from {DATASET}.company_info')
    price_data = pd.read_gbq(f'select * from {DATASET}.prices')
    price_data_with_industry = price_data.merge(
        company_info, 
        on='ticker')

    most_recent = price_data_with_industry.groupby('ticker').last().reset_index()
    most_recent['volatility'] = (most_recent['short_term_ma'] - most_recent['long_term_ma'])

    missing_market_caps = list(np.where(most_recent['market_cap'] == 0)[0])
    missing_sector = list(np.where(most_recent[['sector', 'industry']].isna().any(axis=1))[0])
    complete_data = most_recent.drop(index=missing_market_caps + missing_sector)

    volatility_treemap = px.treemap(
        data_frame=complete_data,
        path=['sector', 'industry', 'ticker'],
        values='market_cap',
        color='volatility',
        color_continuous_scale='RdYlGn_r')
    return volatility_treemap

if __name__ == "__main__":
    fig = create_treemap()
    fig.show()
