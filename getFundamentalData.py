import quandl
import pandas as pd
import numpy as np
import requests


def update_financials(): pd.DataFrame(quandl.get_table('SHARADAR/SF1', dimension='MRY', paginate=True, api_key='zjqr19B8DiYQqkhdnsAe')).to_csv('financials.csv')
def update_quarterly_financials(): pd.DataFrame(quandl.get_table('SHARADAR/SF1', dimension='MRQ', paginate=True, api_key='zjqr19B8DiYQqkhdnsAe')).to_csv('financials_quarterly.csv')
def update_earnings_estimates(): pd.DataFrame(quandl.get_table('ZACKS/EE', per_type='A', paginate=True, api_key='zjqr19B8DiYQqkhdnsAe')).to_csv('estimates.csv')
def update_company_info(): pd.DataFrame(quandl.get_table('SHARADAR/TICKERS', table='SF1', paginate=True, api_key='zjqr19B8DiYQqkhdnsAe')).to_csv('info.csv')


def get_financials(): return pd.read_csv('financials.csv')
def get_quarterly_financials(): return pd.read_csv('financials_quarterly.csv')
def get_earnings_estimates(): return pd.read_csv('estimates.csv')
def get_company_info(): return pd.read_csv('info.csv')


def get_dividend(symbol):
    div_endpoint = 'https://api.tdameritrade.com/v1/instruments'
    div_payload = {'symbol': symbol,
                   'projection': 'fundamental',
                   'apikey': 'WIEVXFCS1MAYRE7JDG5PHF0JB5GPYT8Y'}

    div_raw = pd.json_normalize(requests.get(url=div_endpoint, params=div_payload).json())

    div_yield = div_raw[symbol + '.fundamental.dividendYield'][0] / 100
    div_amount = div_raw[symbol + '.fundamental.dividendAmount'][0]
    div_pay_amount = div_raw[symbol + '.fundamental.dividendPayAmount'][0]
    div_count = int(div_amount / div_pay_amount)
    div_spacing = int(252 / div_count)
    div_date = np.datetime64(div_raw[symbol + '.fundamental.dividendDate'][0][:10])

    return div_yield, div_amount, div_pay_amount, div_count, div_spacing, div_date
