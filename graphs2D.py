import matplotlib.pyplot as plt
import numpy as np
import math
import sympy as smp
from returnModeling import x
from returnModeling import buy_write_irr, cash_secured_put_profit, buy_write_risk
from priceModeling import laplace_dist, scale_parameter, expected_mean_price, laplace_dist_abs, norm_dist
from getVolatility import get_daily_stock_volatility, scale_daily_volatility


# stock_price = 51.75
# option_price = .7
# strike_price = 53
# days_to_exp = 15
# daily_growth_rate = 0.0001
# growth_rate = daily_growth_rate * days_to_exp
# volatility_daily, changes = get_daily_stock_volatility('PFE')
# volatility = scale_daily_volatility(volatility_daily, days_to_exp)
# scale_param = scale_parameter(volatility)
# scaled_changes = []
# for change in changes:
#     scaled_changes.append(scale_daily_volatility(change + daily_growth_rate, days_to_exp))
#
#
# perc_move = -0.02
#
#
#
#
#
# print('Daily Volatility:')
# print(volatility_daily)
# print('Volatility:')
# print(volatility)
# print('Scale Parameter:')
# print(scale_param)
# print('Growth Rate:')
# print(growth_rate)

# print('Exp Price:')
# print(stock_price * perc_move + stock_price)
# print('Profit:')
# print(buy_write_profit_perc(perc_move, stock_price, option_price, strike_price) * stock_price * 100)
# print('Exp Price:')
# print(stock_price * perc_move + stock_price)
# print('Profit:')
# print(cash_secured_put_profit_perc(perc_move, stock_price, option_price, strike_price) * stock_price * 100)

# print('Expected Profit in $')
# print(smp.integrate(cash_secured_put_profit(x, stock_price, option_price, strike_price) * laplace_dist(x, growth_rate, scale_param), (x, -math.inf, math.inf)))
#
# print(smp.integrate(laplace_dist(x, growth_rate, scale_param), (x, -math.inf, math.inf)))





import pandas as pd

# volatility = get_daily_stock_volatility('^VIX')[0]

vix_changes = pd.read_csv('^VIX.csv')['Change']
xs = np.linspace(-.5, .5, 250)
# xys = np.linspace(0, 8, 504)
# xxs = []
# xxxs = []
ys = []
yys = []
# yyys = []
# yyyys = []
# yyyyys = []
# yyyyyys = []
# yyyyyyys = []
# for num in xs:
#     print(num)
#     # ys.append(float(buy_write_irr(num, stock_price, option_price, strike_price, buy_write_risk(stock_price, option_price), days_to_exp)))
#     ys.append(float(norm_dist(num, 0, .0926009)))
#     yys.append(float(laplace_dist(num, 0, scale_parameter(.0926009))))
#     # yyys.append(float(laplace_dist(num, growth_rate, scale_param) * buy_write_irr(num, stock_price, option_price, strike_price, buy_write_risk(stock_price, option_price), days_to_exp)))
#     # yyyys.append(0)
#     # m = expected_mean_price(num, 3.71, .05, .035, 21, 8)
#     # s = scale_daily_volatility(volatility, num)
#     # ys.append(m)
#     # yys.append(m + m * s)
#     # yyys.append(m - m * s)
#     # yyyys.append(m + m * s * 2)
#     # yyyyys.append(m - m * s * 2)
#     # yyyyyys.append(5)
#     # xxs.append(150)
#     # xxxs.append(300)
#
#
#
# plt.plot(xs, ys, c='b')
# plt.plot(xs, yys, c='g')
# # plt.plot(xs, yyys, c='g')
# # plt.plot(xs, yyyys, c='r')
# # plt.plot(xs, yyyyys, c='r')
# # plt.plot(xs, yyyyys, c='r')
# # plt.plot(xs, yyyyyys, c='r')
# # plt.plot(xxs, xys, c='r')
# # plt.plot(xxxs, xys, c='r')
# plt.hist(vix_changes, density=True, bins=200)
#
# plt.show()




# xs = np.linspace(-10, 10, 200)
# ys = []
# for num in xs:
#     print(num)
#     ys.append(laplace_dist(num, 0, scale_parameter(1)))
#
# plt.plot(xs, ys)

# for num in range(1, 10):
#     yys = []
#     for numm in xs:
#         yys.append(laplace_dist(num, 0, scale_parameter(1)) * laplace_dist(numm, num, scale_parameter(1)))
#     plt.plot(xs, yys)











# =====================================================================================================================

k = 1
m = 0
s = scale_parameter(1)

def distribution(x, nn, spac):
    equations = []
    scale_factors = []
    for n in np.linspace(0, nn * spac, nn):
        scale_factor = laplace_dist(k + n, m, s)
        equations.append(scale_factor * laplace_dist(x, k + n, s))
        scale_factors.append(scale_factor)

    return sum(equations) / sum(scale_factors)

y = smp.Symbol('y')

def dist(x, y): return distribution(x, y, .01)

print(smp.limit(dist, y, smp.oo))

from sympy.abc import n
# import scipy
#
# # def f(x): return smp.Sum((laplace_dist(n, m, s) * laplace_dist(x, n, s)), (n, k, smp.oo)) / smp.Sum(laplace_dist(n, m, s), (n, k, smp.oo))
# # def g(x): return smp.Sum(laplace_dist(x, n, s), (n, k, smp.oo))
#
#
# xs = np.linspace(-5, 10, 300)
# # ys = []
# # for num in xs:
# #     ys.append(distribution(num, 1, .1))
# # yys = []
# # for num in xs:
# #     yys.append(distribution(num, 10, .1))
# # yyys = []
# # for num in xs:
# #     yyys.append(distribution(num, 10, .01))
# yyyys = []
# for num in xs:
#     print(round(num, 2))
#     yyyys.append(distribution(num, 500, .01))
# # yyyyys = []
# # for num in xs:
# #     print(round(num, 2))
# #     yyyyys.append(distribution(num, 1000, .01))
# # yyyyyys = []
# # yyyyyyys = []
# # for num in xs:
# #     print(num)
# #     yyyyyys.append(float(f(float(num))))
# #     yyyyyyys.append(float(f(float(num))))
# #
# #
# # # plt.plot(xs, ys)
# # #plt.plot(xs, yys)
# # plt.plot(xs, yyys)
# plt.plot(xs, yyyys)
# # plt.plot(xs, yyyyys)
# # plt.plot(xs, yyyyyys)
# # plt.plot(xs, yyyyyyys)
#
# data = []
# for i in range(0, len(xs)):
#     for occurrence in range(1, int(yyyys[i] * 1000)):
#         data.append(xs[i])
#
# [a_fit, loc_fit, scale_fit] = scipy.stats.gamma.fit(data)
# print(a_fit, loc_fit, scale_fit)
#
# plt.plot(xs, scipy.stats.gamma.pdf(xs, a_fit, loc=loc_fit, scale=scale_fit))
#
# plt.hist(data, density=True, bins=200)
#
# plt.show()






# print(float(distribution(1, 10, .01)))
# print(float(distribution(1, 100, .01)))
# print(float(distribution(1, 1000, .01)))
# print(float(distribution(1, 10000, .01)))


# print(float(f(1)))
