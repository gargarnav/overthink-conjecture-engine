# SPDX-License-Identifier: MIT
"""Ultimate (additive) periodicity miner.

Finds p >= 1, delta and n0 such that s(n + p) = s(n) + delta for every observed n >= n0.
delta = 0 is ordinary ultimate periodicity. Among all (p, n0) that fit, it chooses the
one with the shortest description (preperiod + period), breaking ties by smaller p.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from overthink.conjecture.types import Candidate, Sequence

METHOD = "periodic@1"


def _as_array(values: list[int]) -> np.ndarray:
    if values and max(abs(v) for v in values) >= 2**62:
        return np.array(values, dtype=object)
    return np.array(values, dtype=np.int64)


def find_period(
    values: list[int],
    max_period: int,
    min_repeats: int,
    min_support: int,
    min_tail_fraction: float = 0.0,
) -> tuple[int, int, int, int] | None:
    """Return (p, delta, t, support) with t the 0-based offset where the relation starts,
    or None. `support` counts verified predictions: indices n >= t with n + p observed.
    The periodic regime must cover at least `min_tail_fraction` of the observed terms."""
    v = _as_array(values)
    n = len(v)
    best: tuple[int, int, int, int] | None = None
    for p in range(1, min(max_period, n // min_repeats) + 1):
        d = v[p:] - v[:-p]
        delta = d[-1]
        bad = np.nonzero(d != delta)[0]
        t = int(bad[-1]) + 1 if len(bad) else 0
        if n - t < min_repeats * p or n - t < min_tail_fraction * n:
            continue
        support = n - t - p
        if support < min_support:
            continue
        if best is None or t + p < best[2] + best[0]:
            best = (p, int(delta), t, support)
    return best


def mine(seq: Sequence, cfg: dict[str, Any]) -> list[Candidate]:
    found = find_period(
        seq.values,
        max_period=cfg.get("max_period", 200),
        min_repeats=cfg.get("min_repeats", 3),
        min_support=cfg.get("min_support", 20),
        min_tail_fraction=cfg.get("min_tail_fraction", 0.0),
    )
    if found is None:
        return []
    p, delta, t, support = found
    n0 = seq.start + t
    block = seq.values[t : t + p]
    if delta == 0:
        kind = "periodic"
        statement = f"s(n + {p}) = s(n) for all n >= {n0}"
    else:
        kind = "additive_periodic"
        statement = f"s(n + {p}) = s(n) + {delta} for all n >= {n0}"
    return [
        Candidate(
            kind=kind,
            sequence_id=seq.id,
            params={"period": p, "delta": delta, "n0": n0},
            statement=statement,
            evidence={
                "observed_range": [seq.start, seq.end],
                "support": support,
                "preperiod_length": t,
                "block": block if len(block) <= 64 else block[:64] + ["..."],
            },
            method=METHOD,
            sequence_meta=seq.meta,
        )
    ]
