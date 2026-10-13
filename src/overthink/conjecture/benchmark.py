"""Benchmark the classical miners on planted synthetic sequences.

For each planted sequence: mine at the proposal length, then check every candidate on a
10x extension. Reported per family:
  recovered  - some candidate of an accepted kind holds on the 10x extension
  exact      - (periodic families) recovered with exactly the planted period, delta, n0
  wrong      - number of candidates that FAIL on the 10x extension (false conjectures)
  other_true - candidates that hold on the extension but are not of an accepted kind
  silent     - nothing proposed
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import Any

from overthink.conjecture.checks import check
from overthink.conjecture.mine import mine_sequence
from overthink.conjecture.synthetic import GENERATORS
from overthink.conjecture.types import Sequence


def run_benchmark(
    miner_cfg: dict[str, Any], n_per_family: int, seed: int, scale: int = 10
) -> dict[str, dict[str, Any]]:
    rng = random.Random(seed)
    stats: dict[str, Counter] = defaultdict(Counter)
    failures: dict[str, list] = defaultdict(list)
    for family, gen in GENERATORS.items():
        for i in range(n_per_family):
            planted = gen(rng)
            seq = Sequence(f"synthetic/{family}/{i}", planted.make(planted.length))
            long_seq = Sequence(seq.id, planted.make(planted.length * scale))
            cands = mine_sequence(seq, miner_cfg)
            st = stats[family]
            st["n"] += 1
            st["candidates"] += len(cands)
            if not cands:
                st["silent"] += 1
            recovered = exact = False
            for c in cands:
                res = check(c.kind, c.params, long_seq)
                if res["status"] == "violated":
                    st["wrong"] += 1
                    failures[family].append(
                        {"statement": c.statement, "check": res, "planted": planted.expected}
                    )
                elif res["status"] == "holds" and c.kind not in planted.accepted_kinds:
                    st["other_true"] += 1
                elif res["status"] == "holds":
                    recovered = True
                    exp = planted.expected
                    if "period" in exp and all(
                        c.params.get(k) == exp[k] for k in ("period", "delta", "n0")
                    ):
                        exact = True
            st["recovered"] += recovered
            st["exact"] += exact
    report = {}
    for family, st in stats.items():
        report[family] = dict(st)
        report[family]["failures_sample"] = failures[family][:3]
    return report
