#Lab Notebook

#Entry 0: Oct 16, 2026

Direction change: replaced the earlier curriculum-learning-for-physical-systems plan with an adaptive N-of-1 experimentation engine for AI-assisted learning. It is ML/CS-primary, it is a question I face every study session, and the gap is a measurement problem I can work on.

Goal today: set up the repo and README, write the problem statement, read an introduction to N-of-1/crossover designs and IRT, build the simulated learner, and reproduce the ~385-per-arm power result.

Why: the power result shows why the naive self-test fails. A simulated learner lets me test adaptive retests before collecting any human data.

Open questions:

How should carryover between protocols be modeled?
What counts as an isomorphic variant for competition math?
What are the exact steps and timeline for school IRB approval?

Next: commit after each working piece, and log numbers in the next entry.

#Entry 1: Oct 31, 2026

IRT Basics Reading:

- Every task has some sense of error, human and computer. We cannot get rid of all of these errors so we develop theories to handle them. One of the biggest ones is the IRT or item response theory.
- Classical Test Thoery or CTT believe errors can cancel each other out through summation. However, summation has its limits.
- IRT focuses on individual responses and evaluates each attribute to find the probability.
- Rasch model: P(ypi=1) = exp(θp-bi)/1+exp(θp-bi)
  - P(ypi=1) shows probability a person p getting one point on item i
  - θp = person p's attribute and bi = item i's difficulty
- Works for binary and polytomous responses
- 3 basic assumptions
  - Unidimensionality: Only one dimension of a person's attribute dominates response probability. Violation causes multidimensional IRT models.
  - Monotonicity: Probability increases as attribute increases. Ideal point models not subject to monotonicity.
  - Local Independence: Association of person's responses to different terms is due to attribute
- Advantages:
  - Precision and Granularity
  - Separation of Attributes and Characteristics
  - Adaptability to Diverse Pattern Responses
  - Individualized/Adaptive Assessment
  - Comprehensive Item Analysis

#Entry 2: November 7, 2026

Issues in N-of-1 Trials Paper:

- Serial Correlation Penalty
  - Measurements taken close together in time exhibit strong serial correlation (AR(1)), which reduces effective sample size and significantly lowers statistical power to detect treatment effects.
- Period Stacking Remedy
  - Breaking a fixed total number of observations (T) into more frequent, shorter alternation periods (e.g., shifting from 1p x 2i to 40p x 2i) largely mitigates the power loss caused by serial correlation.
- Washout Trade-offs
  - In the absence of carryover, inserting washout periods slightly decreases statistical power because positive correlation across different active/placebo periods actually helps reduce the variance of the treatment difference.
- Heteroscedasticity Effects
  - Unequal variances between treatments impact power depending on effect size; small effect sizes benefit from unequal variances under low serial correlation, but suffer under high serial correlation.
- Detecting Carryover
  - Statistical power to detect carryover effects is generally weak unless a larger block of measurements is concentrated in the initial baseline/treatment period compared to subsequent alternating periods.

To model carryover in simulate.py, I will need to simulate how a previous treatment's physiological effect lingers into the next period before fully decaying.

#Entry 3: November 8, 2026

Added simulate.py and simulated a student who tested a set of problems. Got varying results depending on how many problems and what the scores were (in percent) based on whether they had already attempted it, used AI, or neither.
With 5,000 retest problems the scores were about 0.66 (none), 0.74 (attempt-first), and 0.69 (AI-first), matching the effects that were set.
With 20 problems the order changed between seeds, even though the true effects never changed.

#Entry 4: November 20, 2026

Worked on reproducing the 385-per-arm power result.
Essentially working at the question at how many problems should be in a retest in order to increase the probability of a 10 point increase.
The formula says about 385 problems per group for 80% power to detect 50% vs 60%.
Simulation (5,000 trials): n=30 gives about 11.7% power, n=385 gives about 80.4%.
With the number of problems I’d realistically do, a real 10-point effect would usually be missed.

#Entry 5: November 26, 2026

The goal was to estimate a learner's skill (theta) from their right/wrong answers, given known problem difficulties.
I built a Rasch-model estimator. P(solve) = 1 / (1 + e^-(theta - b)). It tries every theta from -4 to 4 on a 401-point grid and picks the value that makes the observed answers most likely. It has an optional weak Normal(0, 1.5^2) prior. 
Simulated one learner (true theta 0.8, 500 problems with difficulty from N(0,1), seed 0). Estimated theta was 0.86, off by 0.06.
What I learned: The estimate is noisy because answers are random, and more problems means less noise. Pure maximum likelihood goes to the edge of the grid (+/-4) if every answer so far is right or every answer is wrong, which would be a problem for short retests. The weak prior keeps the estimate finite.
**Next: Adaptive selection rule.**

#Entry 6: November 26, 2026

The goal was to pick each next retest problem to give the most information about skill.
Pick_next chooses the unused problem whose difficulty is closest to the current skill estimate. run_retest gives an n-problem retest, either adaptive or with random difficulties, and returns the final estimate. Both designs use the same estimator with prior sd 1.5, so the comparison is fair. I used the prior in both because with pure maximum likelihood one answer sends the estimate to the grid edge and the adaptive rule would chase a bad estimate.
**Results** 20-problem retest, 300 simulated learners, seed 1, 200-problem pool. **Mean error, adaptive: 0.34. Mean error, random: 0.378.**
What I learned: Adaptive was better in this run. With only 300 learners the gap is about the size of the noise, so one run doesn't prove anything. The seed fixes the numbers, so the run is reproducible.
**Next: Sanity checks, then a bigger comparison.**

#Entry 7: November 26, 2026

The goal was to check that the estimator and adaptive rule behave correctly before trusting the comparison.
**Checks** 
(1) With 20,000 problems, the estimator recovers true theta (-1.5, 0, 1.0) to within 0.1. 
(2) pick_next returns the problem with the closest difficulty. 
(3) No problem is given twice in one retest. 
**All checks passed.**
**Next** Adaptive vs fixed comparison.


#Entry 8: November 26, 2026

The goal was to test whether an adaptive retest estimates skill more accurately than a fixed-difficulty retest at the same length.
**Setup** Rasch model, 200-problem pool with difficulties from N(0,1), true skill from N(0,1) with the same learner used in both designs, weak prior (sd 1.5) in both, seed 2026, 2,000 simulated learners per retest length. Metric: mean |estimated theta - true theta|.
| Retest length | Fixed | Adaptive | Improvement |
|---------------|-------|----------|-------------|
|       5       | 0.631 |   0.591  |      6%     |
|       10      | 0.503 |   0.460  |      9%     |
|       20      | 0.397 |   0.354  |     11%     |
|       40      | 0.289 |   0.255  |     12%     |
**Results** Adaptive had lower error at every retest length, by about 6 to 12%, and the benefit grew a little with length. Error falls roughly as 1/sqrt(n), so by that rough scaling a fixed retest would need about 25 problems to match what adaptive gets from 20. This is an estimate from the table, not a measurement.
**Limitations** The simulation assumes the Rasch model is true and every difficulty is known exactly. Real problems are noisier than that. I haven't yet measured the per-learner difference with a standard error, so the "gap is real" claim is not formally tested.
**Next: Plots (power vs n, error vs retest length), then the sensitivity analysis.**

#Entry 9: November 27, 2026

The goal was to turn the power and comparison results into two plots and a short results summary in the README.
Made `results/power_vs_n.png` (power vs problems per arm for true solve rates 0.50 vs 0.60, analytic curve plus 5,000-trial Monte Carlo points) and `results/error_vs_retest_length.png` (mean absolute error in skill estimate vs retest length, fixed vs adaptive).
The graphs show simulated power at n=30 was [your number from the printout] (analytic 0.12) and about [your number] at n=385 (analytic 0.80). The adaptive retest had lower error than the fixed retest at every length (5, 10, 20, 40), by about 6 to 12%.
**Limitations:** The error plot shows means only, with no confidence intervals. It assumes the Rasch model is true and difficulties are known exactly.
**Next:** Sensitivity analysis over forgetting, carryover, and effect size.

#Entry 10: November 27, 2026

**Setup:** 3 values each for per-session forgetting rate (0.02, 0.05, 0.10), carryover fraction c (0, 0.3, 0.6), and protocol effect scale (0.5x, 1x, 2x of the effect sizes in simulate.py): 27 combinations. For each, the retest problems per arm needed for 80% power to detect attempt_first vs none, with a fixed and an adaptive retest, 500 experiments per point, seed 2026. Both designs use the same Rasch estimator and the same z-test on estimated skill. Table: results/sensitivity.csv.
**Checks:** My training loop matches simulate.run_experiment exactly at the defaults; with zero effect both designs reject about 5% of the time.
**What the answer depends on:** The problems per arm needed for 80% power depend most on the true protocol effect size: the median fell about 8-fold across its three values, from about 1,280 at half the default effect to 480 at the default and 160 at double for the fixed design, and from 960 to 320 to 120 for the adaptive design. Forgetting rate and carryover mattered much less, each changing the median by about 1.6 to 2 times across its three values (for the fixed design, 280 to 560 across forgetting and 280 to 480 across carryover), and more of either made the effect harder to detect. The adaptive design needed fewer problems than the fixed design at every level of every knob, by roughly 12% to 33% in the medians (for example 480 vs 320 at the default effect size), but because the grid is coarse and these are group medians, the exact saving is uncertain.
**Limitations:** Training in my simulator has no randomness, so power reflects measurement noise only. Sample sizes come from a grid, so each is "at most this many". The bank holds 4x the retest length in problems; with a smaller bank the adaptive advantage would shrink. Results hold only for this simulator. The medians leave out combinations that did not reach 80% power by 1,280 problems per arm, so the numbers at the smallest effect size are lower bounds.
**Next:** Finish building the tool and ship it out to 10 people to start working on the paper.