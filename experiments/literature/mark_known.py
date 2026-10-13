# SPDX-License-Identifier: MIT
"""Append `known` events to the registry for surviving conjectures that exactly match a
published statement (same (c, d), period and start). Idempotent: skips IDs already known.

usage: uv run python -I experiments/literature/mark_known.py
"""

from overthink.registry.store import Registry

SUN = (
    "X. Sun, Computer-Assisted and Computer-Generated Research in Combinatorial Games and "
    "Pattern-Avoidance (PhD thesis, Temple University, May 2004), Table 2.1; "
    "https://cst.temple.edu/sites/cst/files/theses9/xysun.pdf"
)
BROUWER = (
    "A. E. Brouwer, The game of Chomp, https://aeb.win.tue.nl/games/chomp.html "
    "(3-rowed Chomp, P-positions for small r)"
)
WW = "E. Berlekamp, J. Conway, R. Guy, Winning Ways (2-rowed Chomp: P-positions (b+1, b))"
GARG = "A. Garg, arXiv:2604.25952v2 (2026), Lemma 1 (Unique Extension)"

# (c, d): (period, start b, source). Sun's start S is in x3 = b - c.
EXACT = {
    (3, 2): (1, 3 + 4, SUN),
    (4, 2): (2, 4 + 3, SUN),
    (8, 2): (1, 8 + 4, SUN),
    (4, 3): (2, 4 + 4, SUN),
    (5, 3): (4, 5 + 4, SUN),
    (7, 3): (8, 7 + 13, SUN),
    (8, 3): (16, 8 + 12, SUN),
    (4, 4): (2, 4 + 4, SUN),
    (0, 0): (1, 0, WW),
    (2, 0): (1, 2, BROUWER),
    (5, 0): (1, 7, BROUWER),
}

reg = Registry()
state = reg.state()
events = []
for cid, e in state.items():
    c = e["conjecture"]
    if e["status"] in ("known", "refuted", "proved"):
        continue
    meta = c.get("sequence_meta", {})
    if (
        c["kind"] == "functional_dependency"
        and c["params"]["target"] == "d"
        and meta.get("dataset", "").startswith("chomp4")
    ):
        events.append(
            {
                "type": "known",
                "conjecture_id": cid,
                "source": GARG,
                "note": "proved there; one-move argument",
            }
        )
        continue
    if c["kind"] != "additive_periodic" or not meta.get("dataset", "").startswith("chomp4"):
        continue
    if meta.get("target") != "a" or meta.get("index") != "b":
        continue
    key = (meta["group"]["c"], meta["group"]["d"])
    if key in EXACT:
        period, start, src = EXACT[key]
        if (
            c["params"]["period"] == period
            and c["params"]["delta"] == period
            and c["params"]["n0"] == start
        ):
            events.append(
                {
                    "type": "known",
                    "conjecture_id": cid,
                    "source": src,
                    "note": f"exact match: (c, d) = {key}, period {period}, start b = {start}",
                }
            )
reg.append(events)
print(f"marked {len(events)} conjectures as known")
for ev in events:
    print(" ", ev["conjecture_id"], ev["note"][:80])
