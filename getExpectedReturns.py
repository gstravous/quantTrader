import math
import numpy as np
import sympy as smp
import priceModeling as pm
import returnModeling as rm
from returnModeling import x
import getVolatility as vol
from marketHolidays import add_market_days, market_holidays


# def buy_write(stock_price, option_price, strike_price, days_to_expiration, volatility, daily_growth_rate):
def buy_write(stock_price, option_price, strike_price, days_to_expiration, volatility, daily_growth_rate, today, dividend_date, dividend_pay, dividend_spacing):
    scale_param = pm.scale_parameter(vol.scale_daily_volatility(volatility, days_to_expiration))
    mean = daily_growth_rate * days_to_expiration
    risk = rm.buy_write_risk(stock_price, option_price)
    # expected_profit = smp.integrate(rm.buy_write_profit(x, stock_price, option_price, strike_price) * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, math.inf))
    # expected_ror = expected_profit / risk
    # expected_irr = (expected_ror / days_to_expiration) * 252
    # std_dev = math.sqrt(smp.integrate((rm.buy_write_profit(x, stock_price, option_price, strike_price) / risk - expected_ror) ** 2 * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, math.inf)))

    if dividend_date <= today:
        dividend_date = add_market_days(dividend_date, dividend_spacing)

    days_to_dividend = np.busday_count(today, dividend_date, weekmask='1111100', holidays=market_holidays).astype('timedelta64[D]').astype(np.int32)
    if days_to_expiration > days_to_dividend:
        dividend_count = int(1 + (days_to_expiration - days_to_dividend) // dividend_spacing)
    else:
        dividend_count = 0

    total_dividend = dividend_count * dividend_pay

    right_limit = math.inf
    p_list = []
    r_list = []
    p_times_r_list = []
    p_times_trade_days = []
    for div in range(0, dividend_count):
        days_to_div = days_to_dividend + div * dividend_spacing
        left_limit = ((strike_price - stock_price) / stock_price - mean) * np.sqrt(days_to_expiration - days_to_div)
        extrinsic_value = (option_price + theta * days_to_div) - (stock_price - strike_price)
        prob_called = smp.integrate(pm.laplace_dist(x, mean, scale_param), (x, left_limit, right_limit))
        p_list.append(prob_called)
        p_times_trade_days.append(prob_called * days_to_div)

        div_received = div * dividend_pay
        irr_called = ((((strike_price - stock_price + option_price + div_received) * 100) / risk) / days_to_div) * 252
        r_list.append(irr_called)

        p_times_r_list.append(prob_called * irr_called)
        right_limit = left_limit
    not_called_sum_of_p_times_r = smp.integrate(rm.buy_write_irr(x, stock_price, option_price, strike_price, risk, days_to_expiration, total_dividend) * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, right_limit))
    expected_irr = sum(p_times_r_list) + not_called_sum_of_p_times_r

    # print('Sum of probabilities:' + str(smp.integrate(pm.laplace_dist(x, mean, scale_param), (x, -math.inf, right_limit)) + sum(p_list)))

    squares_list = []
    for div in range(0, dividend_count):
        r = r_list[div]
        p = p_list[div]
        squares_list.append((r - expected_irr) ** 2 * p)
    not_called_sum_of_squares = smp.integrate((rm.buy_write_irr(x, stock_price, option_price, strike_price, risk, days_to_expiration, total_dividend) - expected_irr) ** 2 * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, right_limit))
    std_dev = np.sqrt(float(sum(squares_list) + not_called_sum_of_squares))

    expected_trade_days = sum(p_times_trade_days) + smp.integrate(pm.laplace_dist(x, mean, scale_param), (x, -math.inf, right_limit)) * days_to_expiration
    annualized_volatility = std_dev * (expected_trade_days / 252) * np.sqrt(float(252 / expected_trade_days))  # scales vol down linearly and then back up with square root

    return risk, expected_irr, annualized_volatility, expected_trade_days, total_dividend, dividend_count


def cash_secured_put(stock_price, option_price, strike_price, days_to_expiration, volatility, daily_growth_rate):
    scale_param = pm.scale_parameter(vol.scale_daily_volatility(volatility, days_to_expiration))
    mean = daily_growth_rate * days_to_expiration
    risk = rm.cash_secured_put_risk(strike_price, option_price)
    expected_profit = smp.integrate(
        rm.cash_secured_put_profit(x, stock_price, option_price, strike_price) * pm.laplace_dist(x, mean, scale_param),
        (x, -math.inf, math.inf))
    expected_ror = expected_profit / risk
    expected_irr = (expected_ror / days_to_expiration) * 252
    std_dev = math.sqrt(smp.integrate((rm.cash_secured_put_profit(x, stock_price, option_price,
                                                                  strike_price) / risk - expected_ror) ** 2 * pm.laplace_dist(
        x, mean, scale_param), (x, -math.inf, math.inf)))

    return risk, expected_profit, expected_ror, expected_irr, std_dev
