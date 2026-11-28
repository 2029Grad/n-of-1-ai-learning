import bisect
import csv
import itertools
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np

import simulate

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

FORGETTING = [0.02, 0.05, 0.10] # per-session forgetting rate (default is 0.05)
CARRYOVER = [0.0, 0.3, 0.6] # carryover fraction c (default is 0.3)
EFFECT_SCALE = [0.5, 1.0, 2.0] # multiplies every protocol effect (1.0 = EFFECT dict)
N_GRID = [20, 30, 40, 60, 80, 120, 160, 240, 320, 480, 640, 960, 1280]
N_TRIALS = 500 # candidate retest problems per arm
TARGET_POWER = 0.80
N_SESSIONS = 10 # training sessions (default)
WEEK_FORGET_MULTIPLIER = 2 # the week-later forgetting = 2 x per-session rate (0.10 at default 0.05)
ARM_A, ARM_B = "attempt_first", "none" 

rng = np.random.default_rng(2026)
GRID = np.linspace(-4, 4, 401)
PRIOR_SD = 1.5
PRIOR_LL = -0.5 * (GRID / PRIOR_SD) ** 2

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

@lru_cache(maxsize=None)
def retest_thetas(forget_rate, carryover, effect_scale):
    effect = {p: effect_scale * simulate.EFFECT[p] for p in simulate.PROTOCOLS}
    theta = {p: 0.0 for p in simulate.PROTOCOLS}
    for _ in range(N_SESSIONS):
        for p in simulate.PROTOCOLS:
            others = [effect[q] for q in simulate.PROTOCOLS if q != p]
            leak = carryover * np.mean(others)
            theta[p] = simulate.grow(theta[p], simulate.GROWTH + effect[p] + leak)
            theta[p] = simulate.forget(theta[p], forget_rate=forget_rate)
    return {p: simulate.forget(theta[p], forget_rate=WEEK_FORGET_MULTIPLIER * forget_rate)
            for p in simulate.PROTOCOLS}

def estimate(y, b):
    p = sigmoid(GRID[:, None] - b[None, :])
    ll = PRIOR_LL + (y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)).sum(axis=1)
    th = GRID[ll.argmax()]
    pr = sigmoid(th - b)
    return th, 1.0 / np.sqrt((pr * (1 - pr)).sum() + 1.0 / PRIOR_SD ** 2)

def bank_size(n):
    return max(200, 4 * n)

def retest_fixed(theta, n, rng):
    bank = rng.normal(0, 1, bank_size(n))
    b = rng.choice(bank, size=n, replace=False)
    y = rng.random(n) < sigmoid(theta - b)
    return estimate(y.astype(float), b)

def retest_adaptive(theta, n, rng):
    unused = np.sort(rng.normal(0, 1, bank_size(n))).tolist()
    ll = PRIOR_LL.copy()
    th_hat = 0.0
    used = []
    for _ in range(n):
        i = bisect.bisect_left(unused, th_hat)
        if i == 0:
            j = 0
        elif i == len(unused):
            j = i - 1
        else:
            j = i if unused[i] - th_hat < th_hat - unused[i - 1] else i - 1
        b = unused.pop(j)
        used.append(b)
        correct = rng.random() < sigmoid(theta - b)
        pr = sigmoid(GRID - b)
        ll += np.log(pr + 1e-12) if correct else np.log(1 - pr + 1e-12)
        th_hat = GRID[ll.argmax()]
    pr = sigmoid(th_hat - np.array(used))
    return th_hat, 1.0 / np.sqrt((pr * (1 - pr)).sum() + 1.0 / PRIOR_SD ** 2)

def detects_effect(n, design, forgetting, carryover, effect, rng):
    thetas = retest_thetas(forgetting, carryover, effect)
    run = retest_fixed if design == "fixed" else retest_adaptive
    est_a, se_a = run(thetas[ARM_A], n, rng)
    est_b, se_b = run(thetas[ARM_B], n, rng)
    return abs(est_a - est_b) / np.hypot(se_a, se_b) > 1.96

def power_at(n, design, forgetting, carryover, effect, trials=None):
    trials = trials or N_TRIALS
    return sum(detects_effect(n, design, forgetting, carryover, effect, rng) for _ in range(trials)) / trials

def problems_needed(design, forgetting, carryover, effect):
    for n in N_GRID:
        if power_at(n, design, forgetting, carryover, effect) >= TARGET_POWER:
            return n
    return f">{N_GRID[-1]}"

def run_checks():
    print("Check 1: my training loop reproduces simulate.run_experiment at your defaults")
    t = retest_thetas(simulate.FORGET, simulate.C, 1.0)
    for seed in range(5):
        r = np.random.default_rng(seed)
        mine = {p: simulate.practice_session(t[p], 20, r)[1].mean() for p in simulate.PROTOCOLS}
        assert mine == simulate.run_experiment(seed=seed), f"mismatch at seed {seed}"
    print("  passed (5 seeds identical)")
    print("Check 2: with zero effect, both designs should reject about 5% of the time")
    for design in ("fixed", "adaptive"):
        rate = power_at(80, design, simulate.FORGET, 0.0, 0.0, trials=1000)
        print(f"  {design}: {rate:.3f}  (should be near 0.05)")
    print("Check 3: power at your defaults, so you can see the designs work")
    for n in (20, 80, 320):
        f = power_at(n, "fixed", simulate.FORGET, simulate.C, 1.0, trials=300)
        a = power_at(n, "adaptive", simulate.FORGET, simulate.C, 1.0, trials=300)
        print(f"  n={n:>3}  fixed {f:.2f}   adaptive {a:.2f}")
    gap = t[ARM_A] - t[ARM_B]
    print(f"True skill gap between {ARM_A} and {ARM_B} at your defaults: {gap:.3f}")

def run_table():
    rows = []
    start = time.time()
    for k, (f, c, e) in enumerate(itertools.product(FORGETTING, CARRYOVER, EFFECT_SCALE), 1):
        t = retest_thetas(f, c, e)
        row = {"forgetting": f, "carryover": c, "effect_scale": e,
               "true_skill_gap": round(float(t[ARM_A] - t[ARM_B]), 3),
               "fixed_n": problems_needed("fixed", f, c, e),
               "adaptive_n": problems_needed("adaptive", f, c, e)}
        rows.append(row)
        print(f"[{k}/27, {time.time() - start:.0f}s]", row, flush=True)
    with open(RESULTS / "sensitivity.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("Saved", RESULTS / "sensitivity.csv")

if __name__ == "__main__":
    run_checks() if "--check" in sys.argv else run_table()