import requests
import pandas as pd
import numpy as np
from marketHolidays import market_holidays
from getFundamentalData import get_dividend


# Gets raw list of contracts and adds dividend date, drop, and amount if desired
def get_raw_contracts(symbol):
    options_endpoint = 'https://api.tdameritrade.com/v1/marketdata/chains'
    options_payload = {'symbol': symbol,
                       'strikeCount': '12',
                       'includeQuotes': 'TRUE',
                       'strategy': 'SINGLE',
                       'apikey': 'WIEVXFCS1MAYRE7JDG5PHF0JB5GPYT8Y'}

    raw = pd.json_normalize(requests.get(url=options_endpoint, params=options_payload).json())  # get raw option data

    price = raw['underlyingPrice'][0]  # gets underlying stock price

    # Remove all columns related to the underlying stock, leaving only cells containing tables of each contract
    del raw['symbol']
    del raw['status']
    del raw['strategy']
    del raw['interval']
    del raw['isDelayed']
    del raw['isIndex']
    del raw['interestRate']
    del raw['underlyingPrice']
    del raw['volatility']
    del raw['daysToExpiration']
    del raw['numberOfContracts']
    del raw['underlying.symbol']
    del raw['underlying.description']
    del raw['underlying.change']
    del raw['underlying.percentChange']
    del raw['underlying.close']
    del raw['underlying.quoteTime']
    del raw['underlying.tradeTime']
    del raw['underlying.bid']
    del raw['underlying.ask']
    del raw['underlying.last']
    del raw['underlying.mark']
    del raw['underlying.markChange']
    del raw['underlying.markPercentChange']
    del raw['underlying.bidSize']
    del raw['underlying.askSize']
    del raw['underlying.highPrice']
    del raw['underlying.lowPrice']
    del raw['underlying.openPrice']
    del raw['underlying.totalVolume']
    del raw['underlying.exchangeName']
    del raw['underlying.fiftyTwoWeekHigh']
    del raw['underlying.fiftyTwoWeekLow']
    del raw['underlying.delayed']

    option_list = pd.json_normalize(list(raw.loc[0]))  # gets first (and only) row and converts to dataframe
    num_of_contracts = len(option_list.index) - 1  # gets total number of contracts
    option_chain = pd.json_normalize(option_list[0][0])  # converts first contract to dataframe
    for contract in range(1, num_of_contracts):  # Combines all contracts into one option chain
        option_chain = option_chain.append(pd.json_normalize(option_list[0][contract]))
        option_chain['underlyingSymbol'] = symbol  # adds column for symbol
        option_chain['underlyingPrice'] = price  # adds column for underlying price

    option_chain['expirationDate'] = pd.to_datetime(option_chain['expirationDate'] * 1000000).dt.date  # expiration epoch to datetime
    option_chain['today'] = pd.to_datetime(str(pd.datetime.now())[:10]) # today's date without hours minutes seconds

    # re-number index
    option_chain = option_chain.reset_index()
    del option_chain['index']
    index_length = len(option_list.index) - 1
    # calculate market days to expiration; includes today and expiration date
    for index in range(0, index_length):
        option_chain.at[index, 'marketDaysToExpiration'] = np.busday_count(np.datetime64('today', 'D'),
                                                                           option_chain['expirationDate'][index],
                                                                           weekmask='1111100',
                                                                           holidays=market_holidays).astype(int)

    option_chain = option_chain[option_chain['bid'] != 0]
    # option_chain = option_chain[option_chain['inTheMoney'] == False]
    option_chain['bidAskSpread'] = (option_chain['ask'] - option_chain['bid']) / option_chain['ask']
    # option_chain = option_chain[option_chain['bidAskSpread'] <= .5].reset_index()
    option_chain['mid'] = option_chain['mark']
    # option_chain['assumedFill'] = option_chain['mid'] - (option_chain['mid'] - option_chain['bid']) * option_chain['bidAskSpread']  # adjust mark to reflect liquidity
    # option_chain['assumedFill'] = np.where(option_chain['inTheMoney'] == True, option_chain['bid'], option_chain['assumedFill'])  # for ITM options, mark = bid
    option_chain['assumedFill'] = option_chain['bid']

    option_chain['dividend_yield'], option_chain['dividend_amount'], option_chain['dividend_pay_amount'], option_chain['dividend_count'], option_chain['dividend_spacing'], option_chain['dividend_date'] = get_dividend(symbol)

    option_chain = option_chain.reset_index()
    del option_chain['index']

    return option_chain, price
