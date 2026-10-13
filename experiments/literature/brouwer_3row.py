# SPDX-License-Identifier: MIT
"""Compare published 3-row Chomp periodicity data with this project's solver and miner.

Source: A. E. Brouwer, "The game of Chomp" (https://aeb.win.tue.nl/games/chomp.html), table of
(r, start, period) for P-positions (p, q, r) of 3-rowed Chomp, with corrections by G. Nivasch.
Here r = c (bottom row), q = b, p = a, and 3-row Chomp = 4-row Chomp with d = 0 (max_d = 0).
"start" is the q from which p - q is periodic; our n0 is the b from which a(b+p) = a(b) + p.

usage: uv run python -I experiments/literature/brouwer_3row.py [max_r]
"""

import sys
import time

import numpy as np

from overthink.conjecture.periodic import find_period
from overthink.games.chomp import chomp4_p_positions

PUBLISHED = {  # r: (start q, period)
    120: (170, 2),
    400: (566, 2),
    402: (571, 4),
    422: (597, 2),
    585: (828, 4),
    890: (1258, 4),
    892: (1265, 4),
    2027: (2867, 3),
    6541: (9250, 9),
}
max_r = int(sys.argv[1]) if len(sys.argv) > 1 else 2100
rs = [r for r in PUBLISHED if r <= max_r]
# p - q grows to about 0.6 r on these rows; leave room for several periods past the start
max_a = max(PUBLISHED[r][0] + (2 * r) // 3 + 300 for r in rs)
t0 = time.time()
P = chomp4_p_positions(max_a, max_c=max(rs), max_d=0)
print(
    f"solved 3-row Chomp, c <= {max(rs)}, a <= {max_a}: {len(P):,} P-positions, "
    f"{time.time() - t0:.0f} s"
)
for r in rs:
    g = P[P[:, 2] == r]
    g = g[np.argsort(g[:, 1])]
    b, a = g[:, 1].tolist(), g[:, 0].tolist()
    run = [x for i, x in enumerate(a) if b[i] == r + i]
    found = find_period(run, max_period=200, min_repeats=3, min_support=20)
    start, period = PUBLISHED[r]
    if found is None:
        print(f"r={r:5d}: no period found within a <= {max_a} (run reaches b={r + len(run) - 1})")
        continue
    p, delta, t, _ = found
    print(
        f"r={r:5d}: published period {period}, start q={start} | ours period {p}, "
        f"start b={r + t} | period agrees: {p == period}, start agrees: {r + t == start}"
    )
