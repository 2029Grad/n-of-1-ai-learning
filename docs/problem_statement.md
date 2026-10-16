Problem Statement

1. Question:

For one learner, does AI assistance build durable problem-solving skill, does the usage protocol (attempt-first-then-AI, AI-first, no AI) change the answer, and how few problems and days are enough to detect an effect?

2. Why it matters / what's known:

Studies of AI and learning are group-level: they report an average over many students and cannot say what AI does for one person. Their results also diverge by design and usage pattern, which averages cannot separate. Testing yourself looks like the obvious alternative, but the naive design is statistically starved. With a binary solve/fail outcome, detecting a 10-point gain (50% to 60%) at 80% power needs n = (1.96 + 0.84)^2 x (0.25 + 0.24) / 0.10^2, about 385 problems per arm. At 30 per arm, the standard error is about 0.128, z is about 0.78, and power is about 12%.

N-of-1 and replicated-crossover methods can estimate individual effects, but as far as I have found they have been used in clinical and psychological settings and not aimed at AI-assisted learning. The gap exists for a solvable reason: individual-level evidence is missing because naive designs need too many problems. The fix is measurement efficiency, which is a math and CS problem. (Verify these claims against the literature before presenting them anywhere.)

3. Hypothesis:

Adaptive retests calibrated to problem difficulty with item response theory reduce the number of problems per arm needed to detect a 10-point retest gain, compared with the binary-outcome design. I have not verified this, and the first simulation is the test of it. My prior on the protocols, to be edited by me: attempt-first retains more skill on unaided retests than AI-first.

4. What would surprise me:

Adaptive IRT retests do not reduce the required number of problems by a meaningful factor. That would mean the central idea fails.
The required number depends mostly on the assumed forgetting and carryover, so the simulation cannot support a design recommendation without real data.
A rising skill trend over time swamps the protocol effect even with randomization, which would mean the design needs a different control for time.

Definitions:

Durable skill: solve rate on an unaided retest of isomorphic variants about a week after practice.

Isomorphic variant: a problem with the same structure and difficulty but different surface details and numbers.

Difficulty calibration: a rating for each problem, such as a contest difficulty rating or an IRT difficulty estimate.

Simulated learner parameters: skill growth rate, forgetting rate, per-protocol effect, and per-protocol carryover.

Power target: 80% power at 5% significance for a 10-point gain, compared across the binary and adaptive designs.

Own data: collected only after school IRB sign-off. The simulation and engine need no app
