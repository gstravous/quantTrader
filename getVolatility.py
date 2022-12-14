import pandas as pd
import numpy as np
import requests
import time
import returnModeling as rm
from getFundamentalData import get_company_info


def get_daily_stock_volatility(symbol):
    print('getting volatility')
    print(symbol)
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/' + symbol + '/pricehistory'
    payload = {'period': '20',
               'periodType': 'year',
               'frequency': '1',
               'frequencyType': 'daily',
               'apikey': 'WIEVXFCS1MAYRE7JDG5PHF0JB5GPYT8Y'}

    try:
        prices = pd.json_normalize(pd.json_normalize(requests.get(url=endpoint, params=payload).json())['candles'][0]).reset_index()

        changes = []
        for index in range(0, len(prices['index']) - 2):
            start_price = prices['close'][index]
            next_index = index + 1
            end_price = prices['close'][next_index]
            change = (end_price - start_price) / start_price
            changes.append(change)

    except:
        wait = 1
        worked = False
        for seconds in range(0, 20):
            if worked: break
            wait =+ seconds
            print(wait)
            time.sleep(wait)
            try:
                prices = pd.json_normalize(pd.json_normalize(requests.get(url=endpoint, params=payload).json())['candles'][0]).reset_index()

                changes = []
                for index in range(0, len(prices['index']) - 2):
                    start_price = prices['close'][index]
                    next_index = index + 1
                    end_price = prices['close'][next_index]
                    change = (end_price - start_price) / start_price
                    changes.append(change)

                worked = True
            except:
                changes = []

    print('done')
    return np.std(changes), changes


def update_daily_volatility():
    stock_volatility = pd.DataFrame({'symbol': [], 'daily_volatility_%': [], 'daily_volatility_$': []})
    for symbol in get_company_info()['ticker']:
        percent, changes = get_daily_stock_volatility(str(symbol))
        stock_volatility = stock_volatility.append(pd.DataFrame({'symbol': [symbol], 'daily_volatility_%': [percent], 'daily_volatility_$': [dollar]}))

    stock_volatility.to_csv('daily_volatility.csv')


def load_daily_volatility(): return pd.read_csv('daily_volatility.csv')
def scale_daily_volatility(volatility, days): return volatility * np.sqrt(days)


# def get_buy_write_volatility(stock_price, option_price, strike_price, expiration_prices):
#     risk = rm.buy_write_risk(stock_price, option_price)
#
#     returns = []
#     for expiration_price in expiration_prices:
#         returns.append(rm.buy_write_profit(expiration_price, stock_price, option_price, strike_price) / risk)
#
#     mean = np.mean(returns)
#     squares = []
#     for x in returns:
#         squares.append(np.square(np.abs(x - mean)))
#
#     std_dev = np.sqrt(float(np.sum(squares) / len(returns)))
#
#     return std_dev, mean
#
#
# def get_cash_secured_put_volatility(stock_price, option_price, strike_price, expiration_prices):
#     risk = rm.cash_secured_put_risk(strike_price, option_price)
#
#     returns = []
#     for expiration_price in expiration_prices:
#         returns.append(rm.cash_secured_put_profit(expiration_price, stock_price, option_price, strike_price) / risk)
#
#     mean = np.mean(returns)
#     squares = []
#     for x in returns:
#         squares.append(np.square(np.abs(x - mean)))
#
#     std_dev = np.sqrt(float(np.sum(squares) / len(returns)))
#
#     return std_dev, mean
