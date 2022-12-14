import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('dark_background')
ax = plt.axes(projection='3d')


financials = pd.read_csv('financials.csv')
financials['net_debt_to_ebitda'] = (financials['debtusd'] - financials['cashnequsd']) / financials['ebitdausd']
financials = financials[financials['net_debt_to_ebitda'].between(financials['net_debt_to_ebitda'].quantile(.15), financials['net_debt_to_ebitda'].quantile(.85))]
financials = financials[financials['marketcap'].between(financials['marketcap'].quantile(.15), financials['marketcap'].quantile(.85))]


volatility = pd.read_csv('daily_volatility.csv')
volatility = volatility[volatility['daily_volatility_%'] != '']
volatility['ticker'] = volatility['symbol']
volatility = volatility[volatility['daily_volatility_%'].between(volatility['daily_volatility_%'].quantile(.15), volatility['daily_volatility_%'].quantile(.85))]

merged = financials.merge(volatility, on='ticker')


ax.scatter(merged['net_debt_to_ebitda'], merged['marketcap'], merged['daily_volatility_%'], alpha=1)

ax.set_xlabel('Net Debt to EBITDA')
ax.set_ylabel('Market Cap')
ax.set_zlabel('Daily Volatility')

plt.show()
