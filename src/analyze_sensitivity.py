import csv, statistics
from collections import defaultdict

rows = list(csv.DictReader(open("n-of-1-ai-learning/results/sensitivity.csv")))
for col in ("fixed_n", "adaptive_n"):
    for knob in ("forgetting", "carryover", "effect_scale"):
        groups = defaultdict(list)
        for r in rows:
            if r[col].isdigit(): # skip ">1280" rows
                groups[r[knob]].append(int(r[col]))
        print(col, knob, {k: statistics.median(v) for k, v in groups.items()})