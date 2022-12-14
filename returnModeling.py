import sympy as smp


x = smp.Symbol('x')  # x = expiration price

# PROFIT IN DOLLARS; X AS PERCENTAGE MOVE IN STOCK PRICE
# RISK IN DOLLARS


def buy_write_risk(stock_price, option_price): return (stock_price - option_price) * 100
def buy_write_profit(x, stock_price, option_price, strike_price): return smp.Piecewise(((strike_price - stock_price) / stock_price + option_price / stock_price, x >= (strike_price - stock_price) / stock_price), (x + option_price / stock_price, x < (strike_price - stock_price) / stock_price)) * stock_price * 100
def buy_write_irr(x, stock_price, option_price, strike_price, risk, days, dividends_received): return smp.Piecewise((((((strike_price - stock_price + option_price + dividends_received) * 100) / risk) / days) * 252, x * stock_price >= strike_price - stock_price), (((((x * stock_price + option_price + dividends_received) * 100) / risk) / days) * 252, x * stock_price < strike_price - stock_price))


def cash_secured_put_risk(strike_price, option_price): return (strike_price - option_price) * 100
def cash_secured_put_profit(x, stock_price, option_price, strike_price): return smp.Piecewise((option_price / stock_price, x >= (strike_price - stock_price) / stock_price), (x - (strike_price - stock_price) / stock_price + option_price / stock_price, x < (strike_price - stock_price) / stock_price)) * stock_price * 100

