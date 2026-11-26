import numpy as np
from estimate import rasch_p, estimate_theta

def pick_next(theta_hat, pool, used):
    candidates = [i for i in range(len(pool)) if i not in used]
    return min(candidates, key=lambda i: abs(pool[i] - theta_hat))

def run_retest(theta_true, pool, n, adaptive, rng, prior_sd=1.5):
    used, ys, bs = set(), [], []
    theta_hat = 0.0
    for _ in range(n):
        if adaptive:
            i = pick_next(theta_hat, pool, used)
        else:
            i = int(rng.choice([j for j in range(len(pool)) if j not in used]))
        used.add(i)
        y = rng.random() < rasch_p(theta_true, pool[i])
        ys.append(y); bs.append(pool[i])
        theta_hat = estimate_theta(ys, bs, prior_sd)
    return theta_hat

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    pool = rng.normal(0, 1, 200)
    errs = {True: [], False: []}
    for _ in range(300):
        th = rng.normal(0, 1)
        for mode in (True, False):
            errs[mode].append(abs(run_retest(th, pool, 20, mode, rng) - th))
    print("mean error, adaptive:", round(np.mean(errs[True]), 3))
    print("mean error, random  :", round(np.mean(errs[False]), 3))