import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

# returns = pd.read_csv('TOL_returns.csv')
# returns = returns[returns['marketDaysToExpiration'] > 12]
# returns_calls = returns[returns['putCall'] == 'CALL']
# returns_puts = returns[returns['putCall'] == 'PUT']
#
# days_calls = returns_calls['marketDaysToExpiration']
# strikes_calls = returns_calls['strikePrice']
# vol_calls = returns_calls['annualized_volatility']
# irr_calls = returns_calls['irr']
# sharpe_calls = returns_calls['annualized_sharpe_ratio']
#
# days_puts = returns_puts['marketDaysToExpiration']
# strikes_puts = returns_puts['strikePrice']
# vol_puts = returns_puts['annualized_volatility']
# irr_puts = returns_puts['irr']
# sharpe_puts = returns_puts['annualized_sharpe_ratio']
#
# # ax = plt.axes(projection='3d', aspect='equalyz')
# ax = plt.axes(projection='3d')
#
# calls = ax.scatter(strikes_calls, vol_calls, irr_calls, c=days_calls, cmap='gist_earth', marker='*', alpha=1)
# puts = ax.scatter(strikes_puts, vol_puts, irr_puts, c=days_puts, cmap='gist_earth', marker='o', alpha=1)
# ax.set_xlabel('Strike Price')
# ax.set_ylabel('Annualized Volatility')
# ax.set_zlabel('IRR')
# plt.colorbar(calls).set_label(label='Market Days to Expiration')

# plt.show()




from sympy.plotting import plot3d
import sympy as smp
from sympy import *
from priceModeling import laplace_dist, norm_dist, scale_parameter, laplace_dist_abs
import math

x, y = symbols('x y', real=True)

mean = 0
std_dev = 1
std_dev_exp = std_dev * sqrt(20)
std_dev_div_to_exp = std_dev * sqrt(5)



plot3d(laplace_dist_abs(x, mean, std_dev_exp) * laplace_dist_abs(y, mean, std_dev_exp), (x, -20, 20), (y, -20, 20))
plot3d(laplace_dist_abs(x, mean, std_dev_exp) * laplace_dist_abs(y - x, mean, std_dev_div_to_exp), (x, -20, 20), (y, -20, 20))
# plot3d(laplace_dist_abs(x, mean, std_dev_exp) * laplace_dist_abs(y, mean, std_dev_exp) - .5 * laplace_dist_abs(x, mean, std_dev_exp) * laplace_dist_abs(y, mean, std_dev_div_to_exp), (x, -20, 20), (y, -20, 20))
