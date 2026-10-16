Adaptive N-of-1 Experiments for AI-Assisted Learning

Research question: For a single learner, does AI assistance build durable problem-solving skill? Does the way it is used (attempt-first-then-AI, AI-first, no AI) change the answer? And how few problems are enough to know?

Why this problem?

Studies of AI and learning report group averages. They cannot say what AI does for one particular learner, and learners differ a lot in how they use it. The obvious fix, testing yourself, runs into a statistics problem: with a binary solve/fail outcome, detecting a 10-point gain in retest solve rate (50% to 60%) at 80% power needs about 385 problems per arm. At 30 problems per arm, power is about 12%.

As far as I have found, N-of-1 methods exist in clinical and psychological research but have not been applied to AI-assisted learning. This project asks whether better measurement can make an individual-level answer feasible in weeks instead of years.

Hypothesis (not yet verified): adaptive, difficulty-calibrated retests, using item response theory (IRT), reduce the number of problems needed per arm.

Approach
Simulation (no human-participant data). A simulated learner has a latent skill that grows with practice, decays with forgetting, and responds to each AI-usage protocol with carryover. Reproduce the ~385-per-arm result for the naive design, then test whether adaptive IRT retests shrink it.
Estimation and experiment engine. Bayesian learning-curve models, adaptive allocation across protocols, and adaptive testing.
Own-data pilot (after school IRB approval). Run the engine on my own competition-math training, with randomized usage protocol across matched problems and unaided retests on isomorphic variants about a week later.

Protocols compared
No AI
Attempt first, then AI
AI first
Measurement

Skill is measured on unaided retests of isomorphic variants of each problem, not the same problem, so the test measures skill and not memory.

Limits to keep in mind:
Simulation results depend on assumptions about forgetting and carryover, so they show what is feasible, not what is true.
A single N-of-1 series may not generalize. The longer plan is to aggregate across series.
Human-participant rules apply when the researcher is the subject. No personal data will be collected until IRB approval is in place.
Status

Started Oct 16, 2026. See LAB_NOTEBOOK.md for daily progress and docs/problem_statement.md for the full problem statement.
