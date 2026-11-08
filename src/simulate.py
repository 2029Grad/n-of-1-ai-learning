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

def grow(theta, amount=GROWTH):
    return theta + amount

def forget(theta, forget_rate=FORGET, baseline=BASELINE):
    return baseline + (theta - baseline) * (1 - forget_rate)

def demo_part1():
    rng = np.random.default_rng(42)
    theta = 0.0
    for session in range(1, 11):
        diffs, solved = practice_session(theta, 10, rng)
        theta = grow(theta)
        theta = forget(theta)
        print(session, "theta =", round(theta, 3), "solve rate =", solved.mean())

if __name__ == "__main__":
    demo_part1()