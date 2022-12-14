import matplotlib.pyplot as plt
import numpy as np
import math
import sympy as smp
from returnModeling import x
from returnModeling import buy_write_irr, cash_secured_put_profit, buy_write_risk
from priceModeling import laplace_dist, scale_parameter
from getVolatility import get_daily_stock_volatility, scale_daily_volatility


stock_price = 51.75
option_price = .7
strike_price = 53
days_to_exp = 15
daily_growth_rate = 0.0001
growth_rate = daily_growth_rate * days_to_exp
volatility_daily, changes = get_daily_stock_volatility('PFE')
volatility = scale_daily_volatility(volatility_daily, days_to_exp)
scale_param = scale_parameter(volatility)
scaled_changes = []
for change in changes:
    scaled_changes.append(scale_daily_volatility(change + daily_growth_rate, days_to_exp))


perc_move = -0.02





print('Daily Volatility:')
print(volatility_daily)
print('Volatility:')
print(volatility)
print('Scale Parameter:')
print(scale_param)
print('Growth Rate:')
print(growth_rate)

# print('Exp Price:')
# print(stock_price * perc_move + stock_price)
# print('Profit:')
# print(buy_write_profit_perc(perc_move, stock_price, option_price, strike_price) * stock_price * 100)
# print('Exp Price:')
# print(stock_price * perc_move + stock_price)
# print('Profit:')
# print(cash_secured_put_profit_perc(perc_move, stock_price, option_price, strike_price) * stock_price * 100)

print('Expected Profit in $')
print(smp.integrate(cash_secured_put_profit(x, stock_price, option_price, strike_price) * laplace_dist(x, growth_rate, scale_param), (x, -math.inf, math.inf)))

print(smp.integrate(laplace_dist(x, growth_rate, scale_param), (x, -math.inf, math.inf)))

xs = np.linspace(-.2, .2, 200)
ys = []
yys = []
yyys = []
yyyys = []
for num in xs:
    # print(num)
    ys.append(float(buy_write_irr(num, stock_price, option_price, strike_price, buy_write_risk(stock_price, option_price), days_to_exp)))
    yys.append(float(laplace_dist(num, growth_rate, scale_param)))
    yyys.append(float(laplace_dist(num, growth_rate, scale_param) * buy_write_irr(num, stock_price, option_price, strike_price, buy_write_risk(stock_price, option_price), days_to_exp)))
    yyyys.append(0)


plt.plot(xs, ys)
plt.plot(xs, yys)
plt.plot(xs, yyys)
plt.plot(xs, yyyys)
plt.hist(scaled_changes, density=True, bins=500)

plt.show()
