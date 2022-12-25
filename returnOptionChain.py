from getOptionChain import get_raw_contracts
import getVolatility as vol
import getExpectedReturns as exp
import getFundamentalData as fun
import numpy as np
import pandas as pd
import multiprocessing as mp
from functools import partial
import warnings
warnings.filterwarnings('ignore')


def calls_return(i, option_chain_calls, volatility, daily_growth_rate, today, dividend_date, dividend_pay, dividend_spacing):
    print('call ' + str(i))
    option_chain_calls = option_chain_calls[option_chain_calls.index == i]
    option_chain_calls['risk'], option_chain_calls['irr'], option_chain_calls['annualized_volatility'], option_chain_calls['expected_trade_days'], option_chain_calls['expected_dividend'], option_chain_calls['max_dividend'], option_chain_calls['dividend_count'], option_chain_calls['div_info'], option_chain_calls['theta_rate'] = exp.buy_write(
        option_chain_calls['underlyingPrice'][i],
        option_chain_calls['assumedFill'][i],
        option_chain_calls['strikePrice'][i],
        option_chain_calls['marketDaysToExpiration'][i],
        volatility,
        daily_growth_rate,
        today,
        dividend_date,
        dividend_pay,
        dividend_spacing,
        option_chain_calls['delta'][i],
        option_chain_calls['gamma'][i],
        option_chain_calls['theta'][i],
        option_chain_calls['vega'][i])

    return option_chain_calls


# def calls_vol(i, option_chain_calls, unique_days_to_expiration):
#     print('call vol ' + str(i))
#     expiration_prices = unique_days_to_expiration[unique_days_to_expiration['market_days_to_expiration'] == option_chain_calls['marketDaysToExpiration'][i]].reset_index()['expiration_prices'][0]
#     option_chain_calls = option_chain_calls[option_chain_calls.index == i]
#     option_chain_calls['contract_volatility'], option_chain_calls['mean'] = vol.get_buy_write_volatility(
#         option_chain_calls['underlyingPrice'][i],
#         option_chain_calls['assumedFill'][i],
#         option_chain_calls['strikePrice'][i],
#         expiration_prices)
#
#     return option_chain_calls[['index', 'contract_volatility', 'mean']]


# def puts_return(i, option_chain_puts, volatility, daily_growth_rate):
#     print('put ' + str(i))
#     option_chain_puts = option_chain_puts[option_chain_puts.index == i]
#     option_chain_puts['risk'], option_chain_puts['profit'], option_chain_puts['ror'], option_chain_puts['irr'], option_chain_puts['contract_volatility'] = exp.cash_secured_put(
#         option_chain_puts['underlyingPrice'][i],
#         option_chain_puts['assumedFill'][i],
#         option_chain_puts['strikePrice'][i],
#         option_chain_puts['marketDaysToExpiration'][i],
#         volatility,
#         daily_growth_rate)
#
#     return option_chain_puts


# def puts_vol(i, option_chain_puts, unique_days_to_expiration):
#     print('put vol ' + str(i))
#     expiration_prices = unique_days_to_expiration[unique_days_to_expiration['market_days_to_expiration'] == option_chain_puts['marketDaysToExpiration'][i]].reset_index()['expiration_prices'][0]
#     option_chain_puts = option_chain_puts[option_chain_puts.index == i]
#     option_chain_puts['contract_volatility'], option_chain_puts['mean'] = vol.get_cash_secured_put_volatility(
#         option_chain_puts['underlyingPrice'][i],
#         option_chain_puts['assumedFill'][i],
#         option_chain_puts['strikePrice'][i],
#         expiration_prices)
#
#     return option_chain_puts[['index', 'contract_volatility',  'mean']]


def main(symbol, yearly_growth_rate, risk_free_rate):
    daily_growth_rate = yearly_growth_rate / 252
    option_chain, stock_price = get_raw_contracts(symbol)  # get option chain and stock price
    volatility = vol.load_daily_volatility()
    volatility = volatility[volatility['symbol'] == symbol].reset_index()['daily_volatility_%'][0]  # get underlying daily volatility
    today = np.datetime64('today', 'D')
    dividend_yield, dividend_amount, dividend_pay, dividend_count, dividend_spacing, dividend_date = fun.get_dividend(symbol)

    # changes = vol.get_daily_stock_volatility(symbol)[1]  # get underlying percent moves
    # changes = [change * -1 for change in changes] + changes  # eliminates directional bias
    # unique_days_to_expiration = pd.DataFrame({'market_days_to_expiration': option_chain['marketDaysToExpiration'].unique()})
    # list_of_lists = []
    # for i in range(
    #         len(unique_days_to_expiration.index)):  # sets empty list for expiration prices at each expiration date
    #     list_of_lists.append([])
    # unique_days_to_expiration['expiration_prices'] = list_of_lists
    #
    # for index in range(0, len(unique_days_to_expiration)):  # gets expiration percentages for each expiration date
    #     expiration_prices = []
    #     for change in changes:
    #         scaled_change = (change + daily_growth_rate) * np.sqrt(unique_days_to_expiration['market_days_to_expiration'][index])
    #         expiration_prices.append(scaled_change)
    #
    #     unique_days_to_expiration.at[index, 'expiration_prices'] = expiration_prices
    option_chain = option_chain[option_chain['marketDaysToExpiration'] > 1]
    option_chain_calls = option_chain[option_chain['putCall'] == 'CALL'].reset_index()
    # option_chain_puts = option_chain[option_chain['putCall'] == 'PUT'].reset_index()

    # option_chain_calls_vol = option_chain_calls[['index', 'marketDaysToExpiration', 'underlyingPrice', 'assumedFill', 'strikePrice']]
    # option_chain_puts_vol = option_chain_puts[['index', 'marketDaysToExpiration', 'underlyingPrice', 'assumedFill', 'strikePrice']]

    calls_index = len(option_chain_calls.index)
    # puts_index = len(option_chain_puts.index)

    option_chain_calls = pd.concat(mp.Pool().map(partial(calls_return, option_chain_calls=option_chain_calls, volatility=volatility, daily_growth_rate=daily_growth_rate, today=today, dividend_date=dividend_date, dividend_pay=dividend_pay, dividend_spacing=dividend_spacing), range(0, calls_index)))
    # option_chain_puts = pd.concat(mp.Pool().map(partial(puts_return, option_chain_puts=option_chain_puts, volatility=volatility, daily_growth_rate=daily_growth_rate), range(0, puts_index)))

    # option_chain_calls_vol = pd.concat(mp.Pool().map(partial(calls_vol, option_chain_calls=option_chain_calls_vol,
    #                                                          unique_days_to_expiration=unique_days_to_expiration),
    #                                                  range(0, calls_index)))
    # option_chain_puts_vol = pd.concat(mp.Pool().map(
    #     partial(puts_vol, option_chain_puts=option_chain_puts_vol, unique_days_to_expiration=unique_days_to_expiration),
    #     range(0, puts_index)))

    # option_chain_calls = option_chain_calls.merge(option_chain_calls_vol)
    # option_chain_puts = option_chain_puts.merge(option_chain_puts_vol)]

    # option_chain = option_chain_calls.append(option_chain_puts)
    option_chain = option_chain_calls

    option_chain['daily_growth_rate'] = daily_growth_rate
    # option_chain['contract_volatility'] = np.where(option_chain['contract_volatility'] == 0, 0.000000000001, option_chain['contract_volatility'])
    # option_chain['contract_sharpe_ratio'] = (option_chain['ror'] - (risk_free_rate * option_chain['marketDaysToExpiration'] / 252)) / option_chain['contract_volatility']
    # option_chain['dividend_yield'] = np.where((option_chain['putCall'] == 'CALL') & (option_chain['inTheMoney'] == False), option_chain['dividend_yield'], 0)
    # option_chain['dividend_amount'] = np.where((option_chain['putCall'] == 'CALL') & (option_chain['inTheMoney'] == False), option_chain['dividend_amount'], 0)
    # option_chain['irr'] = option_chain['irr'] + option_chain['dividend_yield']
    # option_chain['annualized_volatility'] = option_chain['contract_volatility'] * (252 / option_chain['marketDaysToExpiration']) ** 2
    option_chain['annualized_sharpe_ratio'] = (option_chain['irr'] - risk_free_rate) / option_chain['annualized_volatility']
    option_chain['underlying_irr'] = yearly_growth_rate + option_chain['dividend_yield']
    option_chain['underlying_annualized_volatility'] = volatility * np.sqrt(252)
    option_chain['underlying_annualized_sharpe_ratio'] = (option_chain['underlying_irr'] - risk_free_rate) / option_chain['underlying_annualized_volatility']

# ADD COST BASIS
    option_chain.to_csv(symbol + 'returns.csv')

    print('---DONE---')


if __name__ == '__main__':
    # main('symbol', yearly_growth_rate, risk_free_rate)
    main('EPD', .05, 0.041008)

