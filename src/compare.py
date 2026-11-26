import numpy as np, csv, sys
from adaptive import run_retest

N_SIMS = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
LENGTHS = [5, 10, 20, 40]
rng = np.random.default_rng(2026)
pool = rng.normal(0, 1, 200)

rows = []
for n in LENGTHS:
    fixed_err, adapt_err = [], []
    for _ in range(N_SIMS):
        th = rng.normal(0, 1)          # same learner for both designs
        fixed_err.append(abs(run_retest(th, pool, n, False, rng) - th))
        adapt_err.append(abs(run_retest(th, pool, n, True, rng) - th))
    rows.append((n, np.mean(fixed_err), np.mean(adapt_err)))
    print(f"n={n:>2}  fixed={rows[-1][1]:.3f}  adaptive={rows[-1][2]:.3f}", flush=True)

with open("../results/comparison.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["retest_length", "fixed_mean_error", "adaptive_mean_error"])
    for n, a, b in rows:
        w.writerow([n, round(a, 4), round(b, 4)])