import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

P1, P2, ALPHA = 0.50, 0.60, 0.05 # true solve rates in the two arms, test level
Z_A = norm.ppf(1 - ALPHA / 2)
rng = np.random.default_rng(2026)

def analytic_power(n):
    se = np.sqrt(P1 * (1 - P1) / n + P2 * (1 - P2) / n)
    return norm.cdf(abs(P2 - P1) / se - Z_A)

def simulated_power(n, trials=5000):
    x1 = rng.binomial(n, P1, trials)
    x2 = rng.binomial(n, P2, trials)
    pooled = (x1 + x2) / (2 * n)
    se = np.sqrt(2 * pooled * (1 - pooled) / n)
    z = np.divide(x2 / n - x1 / n, se, out=np.zeros(trials), where=se > 0)
    return np.mean(np.abs(z) > Z_A)

ns = np.arange(10, 501)
sim_ns = [10, 30, 60, 100, 150, 200, 250, 300, 385, 450]
sim_power = [simulated_power(n) for n in sim_ns]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(ns, [analytic_power(n) for n in ns], label="Analytic power")
ax.scatter(sim_ns, sim_power, color="black", zorder=3, label="Simulated (5,000 trials each)")
ax.axhline(0.8, linestyle="--", color="gray", linewidth=1)
ax.text(12, 0.82, "80% power", color="gray")
for n in (30, 385):
    ax.annotate(f"n = {n}: {analytic_power(n):.0%}", (n, analytic_power(n)),
                textcoords="offset points", xytext=(10, -18), fontsize=9)
ax.set_xlabel("Problems per arm (n)")
ax.set_ylabel("Power to detect the difference")
ax.set_title("Naive two-arm design: true solve rates 50% vs 60%")
ax.set_ylim(0, 1.02)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(RESULTS / "power_vs_n.png", dpi=200)
plt.close(fig)
print("Saved", RESULTS / "power_vs_n.png")
for n, s in zip(sim_ns, sim_power):
    print(f"  n={n:>3}  simulated {s:.3f}   analytic {analytic_power(n):.3f}")

with open(RESULTS / "comparison.csv") as f:
    rows = list(csv.DictReader(f))
lengths = [int(r["retest_length"]) for r in rows]
fixed = [float(r["fixed_mean_error"]) for r in rows]
adaptive = [float(r["adaptive_mean_error"]) for r in rows]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(lengths, fixed, marker="o", label="Fixed difficulty")
ax.plot(lengths, adaptive, marker="o", label="Adaptive difficulty")
ax.set_xticks(lengths)
ax.set_xlabel("Retest length (problems)")
ax.set_ylabel("Mean absolute error in skill estimate (lower is better)")
ax.set_title("Adaptive vs fixed retests (2,000 simulated learners per point)")
ax.set_ylim(0, max(fixed) * 1.1)
ax.legend()
fig.tight_layout()
fig.savefig(RESULTS / "error_vs_retest_length.png", dpi=200)
plt.close(fig)
print("Saved", RESULTS / "error_vs_retest_length.png")