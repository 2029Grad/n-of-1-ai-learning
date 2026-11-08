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
