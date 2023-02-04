import numpy as np
import plotly
import plotly.express as px


def show_moving_average_comparison(ticker, historical_data) -> plotly.graph_objs._figure.Figure:
    fig = px.line(
        historical_data.query(f'ticker == "{ticker}"'), 
        x=historical_data.query(f'ticker == "{ticker}"').index, 
        y=['long_term_ma', 'short_term_ma']
        )
    return fig


def create_treemap(historical_data, company_data) -> plotly.graph_objs._figure.Figure:

    historical_data_with_industry = historical_data.merge(
        company_data[['ticker', 'sector', 'industry']], 
        on='ticker')
    #Industry is a subset of sector

    most_recent = historical_data_with_industry.groupby('ticker').last().reset_index()
    most_recent['volatility'] = (most_recent['5_day_ma'] - most_recent['90_day_ma'])

    missing_market_caps = list(np.where(most_recent['market_cap'] == 0)[0])
    missing_sector = list(np.where(most_recent[['sector', 'industry']].isna().any(axis=1))[0])
    complete_data = most_recent.drop(index=missing_market_caps + missing_sector)

    volatility_treemap = px.treemap(
        data_frame=complete_data,
        path=['sector', 'industry', 'ticker'],
        values='market_cap',
        color='volatility',
        color_continuous_scale='RdYlGn_r').show()
    return volatility_treemap

