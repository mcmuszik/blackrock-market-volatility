import yfinance as yf
import investpy as inv
import pandas as pd
import warnings
from fredapi import Fred
from typing import Tuple, List
from multiprocessing.dummy import Pool

warnings.simplefilter(action='ignore', category=FutureWarning)

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



def collect_data(ticker_list: List[str], n_threads=20, start: str = '2020-01-01', end: str = '2022-12-31'):
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
    historical_data['90_day_ma'] = calculate_moving_average(historical_data, days=30)
    historical_data['5_day_ma'] = calculate_moving_average(historical_data, days=5)
    return historical_data, company_data

if __name__ == "__main__":
    us_stock_list = list_us_stocks()[:10]
    historical_data, company_data = collect_data(us_stock_list)
