import numpy as np

def p_solve(theta, b):
    #chance that a student with skill theta solves a problem of difficulty b
    return 1 / (1 + np.exp(-(theta - b)))

def practice_session(theta, n_problems, rng):
    #student attempts n_problems new problems, returns difficulties and which were solved
    difficulties = rng.normal(0, 1, size=n_problems)
    probs = p_solve(theta, difficulties)
    solved = rng.random(n_problems) < probs
    return difficulties, solved

GROWTH = 0.10     # how much skill rises per session
FORGET = 0.05     # fraction of skill lost between sessions
BASELINE = 0.0    # where skill decays toward

PROTOCOLS = ["none", "attempt_first", "ai_first"]
EFFECT = {"none": 0.00, "attempt_first": 0.08, "ai_first": 0.03}
C = 0.3   # carryover fraction

def grow(theta, amount=GROWTH):
    return theta + amount

def forget(theta, forget_rate=FORGET, baseline=BASELINE):
    return baseline + (theta - baseline) * (1 - forget_rate)


def run_experiment(n_sessions=10, n_retest=20, seed=0):
    rng = np.random.default_rng(seed)
    theta = {p: 0.0 for p in PROTOCOLS}

    #training phase
    for _ in range(n_sessions):
        for p in PROTOCOLS:
            others = [EFFECT[q] for q in PROTOCOLS if q != p]
            leak = C * np.mean(others)
            theta[p] = grow(theta[p], GROWTH + EFFECT[p] + leak)
            theta[p] = forget(theta[p])

    #one week later: more forgetting, then an UNAIDED retest
    results = {}
    for p in PROTOCOLS:
        t = forget(theta[p], forget_rate=0.10)
        _, solved = practice_session(t, n_retest, rng)
        results[p] = solved.mean()
    return results

def demo_part1():
    rng = np.random.default_rng(42)
    theta = 0.0
    for session in range(1, 11):
        diffs, solved = practice_session(theta, 10, rng)
        theta = grow(theta)
        theta = forget(theta)
        print(session, "theta =", round(theta, 3), "solve rate =", solved.mean())

def demo_part2():
    for seed in range(5):
        res = run_experiment(seed=seed)
        print(seed, {k: round(float(v), 2) for k, v in res.items()})

if __name__ == "__main__":
    demo_part1()
    demo_part2()