import numpy as np
from math import sqrt, ceil
from statistics import NormalDist

P1, P2 = 0.50, 0.60 
Z_ALPHA = 1.96         
Z_BETA = 0.84 

def n_needed(p1=P1, p2=P2):
    return (Z_ALPHA + Z_BETA) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2

def power_formula(n, p1=P1, p2=P2):
    se = sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)  
    z = (p2 - p1) / se 
    return NormalDist().cdf(z - Z_ALPHA)

def power_simulated(n, p1=P1, p2=P2, trials=5000, seed=0):
    rng = np.random.default_rng(seed)
    a = rng.binomial(n, p1, size=trials)
    b = rng.binomial(n, p2, size=trials)
    pa, pb = a / n, b / n
    pooled = (a + b) / (2 * n)
    se = np.sqrt(2 * pooled * (1 - pooled) / n) + 1e-12
    z = (pb - pa) / se
    return np.mean(z > Z_ALPHA)

if __name__ == "__main__":
    print("Problems needed per group:", ceil(n_needed()))
    print("n    formula  simulated")
    for n in [20, 30, 100, 385, 1000]:
        print(n, round(power_formula(n), 3), round(power_simulated(n), 3))