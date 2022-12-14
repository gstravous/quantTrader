import math
import sympy as smp

x = smp.Symbol('x')


def scale_parameter(std_dev): return std_dev / math.sqrt(2)


# probability density function
def norm_dist(x, mean, std_dev): return (1 / (std_dev * smp.sqrt(2 * smp.pi))) * smp.exp(-.5 * ((x - mean) / std_dev) ** 2)
def laplace_dist(x, mean, scale_parameter): return smp.Piecewise(((1 / (2 * scale_parameter)) * smp.exp((-1 * (x - mean)) / scale_parameter), x >= mean), ((1 / (2 * scale_parameter)) * smp.exp((x - mean) / scale_parameter), x < mean))
