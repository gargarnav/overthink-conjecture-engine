# SPDX-License-Identifier: MIT
"""Compare X. Sun (2004, PhD thesis, Temple University), Table 2.1 "Periodic Properties of Some
Four-rowed P-positions", with this project's exact data (chomp4_a3000_c60, a <= 3000).

Sun writes a position bottom-up as row increments [x1, x2, x3, x4] = [d, c-d, b-c, a-b]
(checked on his example [2,0,2] = rows (4,2,2), a P-position). T = [x1, x2] fixes (c, d);
p = period; S = value of x3 = b - c where the periodic property starts. Blank = no entry.
"""

import polars as pl

from overthink.conjecture.periodic import find_period

SUN = {  # T: (p, S) or None for a blank entry, transcribed from Table 2.1
    (1, 0): None,
    (2, 0): None,
    (2, 1): (1, 4),
    (2, 2): (2, 3),
    (2, 3): None,
    (2, 4): None,
    (2, 5): None,
    (2, 6): (1, 4),
    (2, 7): None,
    (3, 0): None,
    (3, 1): (2, 4),
    (3, 2): (4, 4),
    (3, 3): (8, 11),
    (3, 4): (8, 13),
    (3, 5): (16, 12),
    (3, 6): None,
    (4, 0): (2, 4),
    (4, 1): None,
    (4, 2): (8, 8),
    (4, 3): None,
    (4, 4): None,
    (4, 5): None,
    (5, 0): None,
    (5, 1): (8, 14),
    (5, 2): None,
}
df = pl.read_parquet("data_out/chomp4_a3000_c60/data.parquet")
rows = []
for (x1, x2), sun in SUN.items():
    d, c = x1, x1 + x2
    g = df.filter((pl.col("c") == c) & (pl.col("d") == d)).sort("b")
    bs, a_s = g["b"].to_list(), g["a"].to_list()
    # infinitely many P-positions <=> a(b) keeps existing up to the truncation edge
    run = [a for i, a in enumerate(a_s) if bs[i] == c + i]
    finite = len(run) < 1000
    ours = None
    if not finite:
        f = find_period(run, max_period=200, min_repeats=3, min_support=20)
        if f:
            p, delta, t, _ = f
            ours = (p, t)  # t = offset from b = c, i.e. the x3 value where it starts
    rows.append(
        {
            "T": f"[{x1},{x2}]",
            "(c,d)": f"({c},{d})",
            "P-positions": len(a_s),
            "ours (p, start x3)": "finite" if finite else str(ours),
            "Sun (p, S)": str(sun) if sun else "blank",
            "period agrees": None if (finite or not sun) else ours[0] == sun[0],
            "start agrees": None if (finite or not sun) else ours[1] == sun[1],
        }
    )
t = pl.DataFrame(rows)
with pl.Config(tbl_rows=40, tbl_width_chars=200):
    print(t)
print(
    "blank <-> finite:",
    all((r["Sun (p, S)"] == "blank") == (r["ours (p, start x3)"] == "finite") for r in rows),
)
