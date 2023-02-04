import yfinance as yf
import investpy as inv
import pandas as pd
import json
import warnings
from fredapi import Fred
from typing import Tuple, List
from multiprocessing.dummy import Pool

from firestore_helpers import CREDENTIALS

warnings.simplefilter(action='ignore', category=FutureWarning)
DATASET = 'uga-hacks-2023-mv.market_volatility_project'
TABLE = 'company_info'

query = f"Select count(*) from {DATASET}.{TABLE} where zip is not null"

api_key = json.load(open('fred_creds.json', 'r'))
fred = Fred(api_key=api_key['key'])


def get_historical_and_company_data(ticker:str, **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Given a company stock ticker, return two dataframes:
    one with historical price data, and one with company information
    """
    yf_ticker = yf.Ticker(ticker)
    try:
        historical_data = yf_ticker.history(**kwargs)
        historical_data.reset_index(inplace=True)
        historical_data['ticker'] = ticker
        historical_data['market_cap'] = historical_data['Close'] * historical_data['Volume']
        
        company_data = pd.Series(yf_ticker.info)
        company_data['ticker'] = ticker
        print(f'Done with {ticker}')
        return historical_data, company_data
    except:
        return pd.DataFrame(), pd.Series()


def list_us_stocks(n=1000):
    """
    Return a list of US stock tickers
    """
    us_stocks = inv.get_stocks().query('country == "united states"')
    if isinstance(n, int):
        ticker_list = us_stocks.head(n)['symbol']
    else:
        ticker_list = us_stocks['symbol']
    return ticker_list


def calculate_moving_average(
    data: pd.DataFrame,
    days: int,
    partition_by: str='ticker',
    over='Close_Diff') -> pd.Series:
    """
    Calculate a moving average over a given column, partitioned by another column.
    """
    return data.groupby(partition_by)[over].transform(lambda x: x.rolling(days).mean())


def collect_data_from_yahoo(ticker_list: List[str], n_threads=20, start: str = '2020-01-01', end: str = '2022-12-31'):
    """
    Collect historical price data and company data for each company in a list of tickers.
    """
    with Pool(20) as p:
        data = p.map(
            lambda x: get_historical_and_company_data(x, start=start, end=end), 
            ticker_list
            )

    historical_data = pd.concat([i[0] for i in data])
    company_data = pd.DataFrame([i[1] for i in data])

    historical_data['Close_Diff'] = historical_data['Close'].diff()
    historical_data['long_term_ma'] = calculate_moving_average(historical_data, days=30)
    return historical_data, company_data


def get_possible_tickers(dataset: str = 'uga-hacks-2023-mv.market_volatility_project', table: str = 'company_info'):
    legit_tickers = pd.read_gbq(
        f"""
        select distinct(ticker) 
        from {DATASET}.{TABLE}
        where sector is not null
        """,
        credentials=CREDENTIALS)
    return legit_tickers['tickers'].to_list()


if __name__ == "__main__":
    most_recent_query = f"""
        SELECT Date, Close, Volume, market_cap, Ticker 
        FROM (
            SELECT Date, Close, Volume,market_cap, Ticker,
                RANK() OVER(PARTITION BY Ticker ORDER BY Date DESC) rank
            FROM {DATASET}.prices
        )
        WHERE rank=1
    """
    prices = pd.read_csv('prices.csv')
