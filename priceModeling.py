import math
import sympy as smp

x = smp.Symbol('x')


def scale_parameter(std_dev): return std_dev / math.sqrt(2)


# probability of x percent move in stock
def norm_dist(x, mean, std_dev): return (1 / (std_dev * smp.sqrt(2 * smp.pi))) * smp.exp(-.5 * ((x - mean) / std_dev) ** 2)
def laplace_dist(x, mean, scale_parameter): return smp.Piecewise(((1 / (2 * scale_parameter)) * smp.exp((-1 * (x - mean)) / scale_parameter), x >= mean), ((1 / (2 * scale_parameter)) * smp.exp((x - mean) / scale_parameter), x < mean))
def laplace_dist_abs(x, mean, scale_parameter): return (1 / (2 * scale_parameter)) * smp.exp((-1 * abs(x - mean)) / scale_parameter)


# expected stock price x days from today, due to overall stock growth + fluctuations due to dividend
def expected_mean_price(x, start_price, yearly_growth_rate, dividend_pay, dividend_spacing, days_to_dividend): return start_price + yearly_growth_rate / 252 * x + dividend_pay / dividend_spacing * x - dividend_pay * (1 + (x - days_to_dividend) // dividend_spacing)