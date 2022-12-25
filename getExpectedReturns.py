import math
import numpy as np
import sympy as smp
import priceModeling as pm
import returnModeling as rm
from returnModeling import x
import getVolatility as vol
from marketHolidays import add_market_days, market_holidays


def theo_option_price(dollar_stock_move, days, current_option_price, delta, gamma, theta, theta_rate): return current_option_price + dollar_stock_move * delta + (.5 * dollar_stock_move ** 2 - .5 * dollar_stock_move) * gamma + days * theta + .5 * theta_rate * days ** 2

# def buy_write(stock_price, option_price, strike_price, days_to_expiration, volatility, daily_growth_rate):
def buy_write(stock_price, option_price, strike_price, days_to_expiration, volatility, daily_growth_rate, today, dividend_date, dividend_pay, dividend_spacing, delta, gamma, theta, vega):
    if vega == 0:
        vega = .005
    scale_param = pm.scale_parameter(vol.scale_daily_volatility(volatility, days_to_expiration))
    risk = rm.buy_write_risk(stock_price, option_price)
    intrinsic_value = stock_price - strike_price
    if intrinsic_value < 0:  # if OTM, 0 intrinsic value
        intrinsic_value = 0
    extrinsic_value = option_price - intrinsic_value
    try:
        theta_rate = (intrinsic_value - option_price - theta * days_to_expiration) / (.5 * days_to_expiration ** 2 - .5 * days_to_expiration)
        x_vertex = (.5 * theta_rate - theta) / theta_rate
        y_vertex = theo_option_price(strike_price - stock_price, x_vertex, option_price, delta, gamma, theta, theta_rate)
        if x_vertex > days_to_expiration:
            if y_vertex > 0:
                theta_rate = 0
                theta = -1 * (extrinsic_value / days_to_expiration)
        else:
            if y_vertex < 0:
                theta_rate = 0
                theta = -1 * (extrinsic_value / days_to_expiration)
            else:
                if x_vertex > 0:
                    theta_rate = 0
                    theta = -1 * (extrinsic_value / days_to_expiration)

    except:
        theta_rate = 0
        theta = -1 * (extrinsic_value / days_to_expiration)

    if intrinsic_value > option_price:
        theta = 0
        theta_rate = 0
    # expected_profit = smp.integrate(rm.buy_write_profit(x, stock_price, option_price, strike_price) * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, math.inf))
    # expected_ror = expected_profit / risk
    # expected_irr = (expected_ror / days_to_expiration) * 252
    # std_dev = math.sqrt(smp.integrate((rm.buy_write_profit(x, stock_price, option_price, strike_price) / risk - expected_ror) ** 2 * pm.laplace_dist(x, mean, scale_param), (x, -math.inf, math.inf)))

    if dividend_date <= today:  # if next div not announced, estimate it
        dividend_date = add_market_days(dividend_date, dividend_spacing)

    days_to_dividend = np.busday_count(today, dividend_date, weekmask='1111100', holidays=market_holidays).astype('timedelta64[D]').astype(np.int32)
    if days_to_expiration > days_to_dividend:  # count the number of dividends to be paid between now and expiration
        dividend_count = int(1 + (days_to_expiration - days_to_dividend) // dividend_spacing)
    else:
        dividend_count = 0

    total_dividend = dividend_count * dividend_pay  # total $ of dividend to be paid between now and expiration

    exp_mean = (pm.expected_mean_price(days_to_expiration, stock_price, daily_growth_rate * 252, dividend_pay, dividend_spacing, days_to_dividend) - stock_price) / stock_price

    strike_percent = (strike_price - stock_price) / stock_price  # percent move to strike
    right_limit = math.inf
    p_list = []  # for std dev calc
    r_list = []  # for std dev calc
    p_times_r_list = []  # for irr calc
    p_times_trade_days = []  # for exp trade length calc
    p_times_dividend = []  # for exp div received calc
    div_info = []
    prob_prev_not_called = 0
    for div in range(0, dividend_count):
        days_to_div = days_to_dividend + div * dividend_spacing - 1
        mean_at_div = (pm.expected_mean_price(days_to_div, stock_price, daily_growth_rate * 252, dividend_pay, dividend_spacing, days_to_dividend) - stock_price) / stock_price
        # left_limit = (strike_percent - mean_at_div) * np.sqrt(days_to_expiration - days_to_div)  # std dev @ exp that; if over, assumed already called at this dividend
        left_limit = (strike_percent - mean_at_div) * np.sqrt((days_to_expiration - days_to_div) / days_to_div) + exp_mean
        if stock_price >= strike_price:  # if currently ITM, calculate current extrinsic value, and reduce by theta
            extrinsic_value = theo_option_price(0, days_to_div, option_price, delta, gamma, theta, theta_rate) - intrinsic_value
        else:  # if currently OTM, estimate extrinsic value if stock were to be ATM at ex-dividend; no intrinsic
            extrinsic_value = theo_option_price(strike_price - stock_price, days_to_div, option_price, delta, gamma, theta, theta_rate)

        prob_itm = smp.integrate(pm.laplace_dist(x, exp_mean, scale_param), (x, left_limit, right_limit)) + prob_prev_not_called
        req_extrinsic_move = dividend_pay - extrinsic_value  # dollar move in extrinsic value to NOT be called
        prob_called_if_itm = smp.integrate(pm.laplace_dist(x, 0, pm.scale_parameter(vol.scale_daily_volatility(.0926009 * vega, days_to_div))), (x, -math.inf, req_extrinsic_move))
        prob_called = prob_itm * prob_called_if_itm
        prob_prev_not_called = prob_itm * (1 - prob_called_if_itm)
        p_list.append(prob_called)
        p_times_trade_days.append(prob_called * days_to_div)
        div_received = div * dividend_pay  # div received, if any, before being called; excludes this dividend
        p_times_dividend.append(prob_called * div_received)
        irr_called = ((((strike_price - stock_price + option_price + div_received) * 100) / risk) / days_to_div) * 252
        r_list.append(irr_called)
        p_times_r_list.append(prob_called * irr_called)
        right_limit = left_limit

        div_info.append((days_to_div, extrinsic_value, req_extrinsic_move, pm.scale_parameter(vol.scale_daily_volatility(.0926009 * vega, days_to_div)), prob_itm, prob_called_if_itm, prob_called))

        if stock_price >= strike_price:
            break

    if prob_prev_not_called > 0:
        p_list.append(prob_prev_not_called)  # prob not called at last dividend, assumed called at expiration
        r_list.append(rm.buy_write_irr(strike_price, stock_price, option_price, strike_price, risk, days_to_expiration, total_dividend))  # return if called at expiration

    not_called_sum_of_p_times_r = smp.integrate(rm.buy_write_irr(x, stock_price, option_price, strike_price, risk, days_to_expiration, total_dividend) * pm.laplace_dist(x, exp_mean, scale_param), (x, -math.inf, right_limit))
    expected_irr = sum(p_times_r_list) + not_called_sum_of_p_times_r

    print('Sum of probabilities:' + str(smp.integrate(pm.laplace_dist(x, exp_mean, scale_param), (x, -math.inf, right_limit)) + sum(p_list)))

    squares_list = []
    for i in range(len(r_list)):
        r = r_list[i]
        p = p_list[i]
        squares_list.append((r - expected_irr) ** 2 * p)
    not_called_sum_of_squares = smp.integrate((rm.buy_write_irr(x, stock_price, option_price, strike_price, risk, days_to_expiration, total_dividend) - expected_irr) ** 2 * pm.laplace_dist(x, exp_mean, scale_param), (x, -math.inf, right_limit))
    std_dev = np.sqrt(float(sum(squares_list) + not_called_sum_of_squares))

    prob_never_called_early = smp.integrate(pm.laplace_dist(x, exp_mean, scale_param), (x, -math.inf, right_limit)) + prob_prev_not_called

    expected_trade_days = sum(p_times_trade_days) + prob_never_called_early * days_to_expiration
    expected_dividend = sum(p_times_dividend) + prob_never_called_early * total_dividend
    annualized_volatility = std_dev * (expected_trade_days / 252) * np.sqrt(float(252 / expected_trade_days))  # scales vol down linearly and then back up with square root

    return risk, expected_irr, annualized_volatility, str(p_list), str(r_list), exp_mean * stock_price + stock_price, not_called_sum_of_squares, str(div_info), theta_rate
    # return risk, expected_irr, annualized_volatility, expected_trade_days, expected_dividend, total_dividend, dividend_count, str(div_info), theta_rate


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
