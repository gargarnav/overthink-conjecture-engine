"""Run all classical miners on one sequence and select by description length.

Every miner runs on every sequence. Each candidate gets a description length: the number
of integers or reals needed to state it, including the initial terms it does not explain
(its preperiod). Only the candidates with the minimal description length are kept as
conjectures; the others are recorded in `evidence["alternatives"]`. This stops e.g. a
Beatty sequence floor(alpha*n) being reported as "additively periodic from n = 173 on",
which can look true near a convergent of alpha. OEIS matches are kept separately.
"""

from __future__ import annotations

from typing import Any

from overthink.conjecture import floorlinear, oeis, periodic, polynomial, recurrence
from overthink.conjecture.oeis import OEISSnapshot
from overthink.conjecture.types import Candidate, Sequence


def description_length(c: Candidate, seq_start: int) -> int:
    pre = c.params.get("n0", seq_start) - seq_start
    if c.kind in ("periodic", "additive_periodic"):
        return pre + c.params["period"] + (c.params["delta"] != 0)
    if c.kind in ("polynomial", "quasi_polynomial"):
        return pre + sum(len(p) for p in c.params["polynomials"].values())
    if c.kind == "linear_recurrence":
        return pre + 2 * len(c.params["coefficients"])
    if c.kind == "floor_linear":
        return pre + 2
    raise ValueError(c.kind)


def mine_sequence(
    seq: Sequence, cfg: dict[str, Any], snapshot: OEISSnapshot | None = None
) -> list[Candidate]:
    structural = (
        periodic.mine(seq, cfg.get("periodic", {}))
        + polynomial.mine(seq, cfg.get("polynomial", {}))
        + recurrence.mine(seq, cfg.get("recurrence", {}))
        + floorlinear.mine(seq, cfg.get("floor_linear", {}))
    )
    kept: list[Candidate] = []
    if structural:
        costs = [description_length(c, seq.start) for c in structural]
        best = min(costs)
        for c, cost in zip(structural, costs, strict=True):
            c.evidence["description_length"] = cost
        for c, cost in zip(structural, costs, strict=True):
            if cost == best:
                c.evidence["alternatives"] = [
                    {"kind": o.kind, "statement": o.statement, "description_length": oc}
                    for o, oc in zip(structural, costs, strict=True)
                    if o is not c and oc != best
                ]
                kept.append(c)
    return kept + oeis.mine(seq, cfg.get("oeis", {}), snapshot)
