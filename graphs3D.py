import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

returns = pd.read_csv('TOL_returns.csv')
returns = returns[returns['marketDaysToExpiration'] > 12]
returns_calls = returns[returns['putCall'] == 'CALL']
returns_puts = returns[returns['putCall'] == 'PUT']

days_calls = returns_calls['marketDaysToExpiration']
strikes_calls = returns_calls['strikePrice']
vol_calls = returns_calls['annualized_volatility']
irr_calls = returns_calls['irr']
sharpe_calls = returns_calls['annualized_sharpe_ratio']

days_puts = returns_puts['marketDaysToExpiration']
strikes_puts = returns_puts['strikePrice']
vol_puts = returns_puts['annualized_volatility']
irr_puts = returns_puts['irr']
sharpe_puts = returns_puts['annualized_sharpe_ratio']

# ax = plt.axes(projection='3d', aspect='equalyz')
ax = plt.axes(projection='3d')

calls = ax.scatter(strikes_calls, vol_calls, irr_calls, c=days_calls, cmap='gist_earth', marker='*', alpha=1)
puts = ax.scatter(strikes_puts, vol_puts, irr_puts, c=days_puts, cmap='gist_earth', marker='o', alpha=1)
ax.set_xlabel('Strike Price')
ax.set_ylabel('Annualized Volatility')
ax.set_zlabel('IRR')
plt.colorbar(calls).set_label(label='Market Days to Expiration')

# # Sharpe Ratio
# calls = ax.scatter(strikes_calls, days_calls, sharpe_calls, c=irr_calls, cmap='gist_earth', marker='*', alpha=1)
# puts = ax.scatter(strikes_puts, days_puts, sharpe_puts, c=irr_puts, cmap='gist_earth', marker='o', alpha=1)
# ax.set_xlabel('Strike Price')
# ax.set_ylabel('Market Days to Expiration')
# ax.set_zlabel('Sharpe Ratio')
# plt.colorbar(calls).set_label(label='IRR')







# plt.title('PFE 12/3/22 Options Non-Annualized Returns and Volatility @ 0.01% Daily Growth')



plt.show()
