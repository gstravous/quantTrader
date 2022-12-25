import sympy as smp
import priceModeling as pm
from priceModeling import x
import getVolatility as vol
import math


vega =.01

smp.integrate(pm.laplace_dist(x, 0, pm.scale_parameter(vol.scale_daily_volatility(.0926009 * vega, days_to_div))), (x, -math.inf, req_extrinsic_move))