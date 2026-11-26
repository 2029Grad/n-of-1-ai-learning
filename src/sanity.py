import numpy as np
from estimate import rasch_p, estimate_theta
from adaptive import pick_next

rng = np.random.default_rng(42)

# Check 1: with a huge retest, the estimator recovers theta
for th in (-1.5, 0.0, 1.0):
    b = rng.normal(0, 1, 20000)
    y = rng.random(20000) < rasch_p(th, b)
    assert abs(estimate_theta(y, b) - th) < 0.1
print("check 1 passed")

# Check 2: pick_next returns the closest difficulty
pool = rng.normal(0, 1, 200)
i = pick_next(0.5, pool, set())
assert abs(pool[i] - 0.5) <= min(abs(d - 0.5) for j, d in enumerate(pool) if j != i) + 1e-12
print("check 2 passed")

# Check 3: no repeats within one retest
used = set()
for _ in range(30):
    j = pick_next(0.0, pool, used)
    assert j not in used
    used.add(j)
print("check 3 passed")