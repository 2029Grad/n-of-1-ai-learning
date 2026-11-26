import numpy as np

GRID = np.linspace(-4, 4, 401)

def rasch_p(theta, b):
    return 1.0 / (1.0 + np.exp(-(theta - b)))

def estimate_theta(outcomes, difficulties, prior_sd=None):
    """Grid-search estimate of skill theta under the Rasch model.
    prior_sd=None -> pure maximum likelihood.
    prior_sd=1.5  -> weak Normal(0, 1.5^2) prior (keeps the estimate finite
                     when every answer so far is right or wrong)."""
    y = np.asarray(outcomes, dtype=float)
    b = np.asarray(difficulties, dtype=float)
    p = rasch_p(GRID[:, None], b[None, :])
    ll = (y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)).sum(axis=1)
    if prior_sd is not None:
        ll = ll - 0.5 * (GRID / prior_sd) ** 2
    return GRID[np.argmax(ll)]

if __name__ == "__main__":
    rng = np.random.default_rng()   # no seed, so it varies every run
    for n in (20, 200, 2000):
        errs = []
        for _ in range(100):
            th = 0.8
            b = rng.normal(0, 1, n)
            y = rng.random(n) < rasch_p(th, b)
            errs.append(abs(estimate_theta(y, b, prior_sd=1.5) - th))
        print(n, "problems -> average error", round(float(np.mean(errs)), 3))