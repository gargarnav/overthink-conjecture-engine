# SPDX-License-Identifier: MIT
"""Floor-linear (Beatty-type) miner: s(n) = floor(alpha * n + beta).

A sequence has this form for some real alpha, beta exactly when
    max_{i<j} (s_j - s_i - 1)/(j - i)  <  alpha  <  min_{i<j} (s_j - s_i + 1)/(j - i),
so the set of feasible slopes is an open interval computed exactly from the data.
The miner always reports the existence statement with the exact slope interval, plus
stronger guesses for the slope:
  * the simplest rational in the interval, if its denominator is small
    (such sequences are also additively periodic);
  * every named constant from `constants.CONSTANTS` lying in the interval.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import Any

import numpy as np

from overthink.conjecture.constants import CONSTANTS
from overthink.conjecture.types import Candidate, Sequence

METHOD = "floor-linear@1"


def alpha_interval(values: list[int], chunk: int = 512) -> tuple[Fraction, Fraction]:
    """Exact (L, U): s is floor-linear iff L < U, and then alpha ranges over (L, U)."""
    v = np.asarray(values, dtype=np.float64)
    n = len(v)
    best_lo, lo_pair = -math.inf, (0, 1)
    best_hi, hi_pair = math.inf, (0, 1)
    idx = np.arange(n)
    for i0 in range(0, n - 1, chunk):
        i = idx[i0 : i0 + chunk, None]
        dj = idx[None, :] - i
        mask = dj > 0
        diff = v[None, :] - v[i0 : i0 + chunk, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            lo = np.where(mask, (diff - 1) / dj, -np.inf)
            hi = np.where(mask, (diff + 1) / dj, np.inf)
        a = np.unravel_index(np.argmax(lo), lo.shape)
        if lo[a] > best_lo:
            best_lo, lo_pair = lo[a], (i0 + a[0], a[1])
        b = np.unravel_index(np.argmin(hi), hi.shape)
        if hi[b] < best_hi:
            best_hi, hi_pair = hi[b], (i0 + b[0], b[1])
    (i, j), (k, m) = (int(x) for x in lo_pair), (int(x) for x in hi_pair)
    lo_exact = Fraction(values[j] - values[i] - 1, j - i)
    hi_exact = Fraction(values[m] - values[k] + 1, m - k)
    return lo_exact, hi_exact


def simplest_between(lo: Fraction, hi: Fraction | None) -> Fraction:
    """Simplest rational (smallest denominator) in the open interval (lo, hi); hi=None is +inf."""
    fl = math.floor(lo)
    if hi is None or fl + 1 < hi:
        return Fraction(fl + 1)
    inner_hi = None if lo == fl else 1 / (lo - fl)
    return fl + 1 / simplest_between(1 / (hi - fl), inner_hi)


def beta_interval(values: list[int], start: int, alpha: Decimal | Fraction) -> tuple[float, float]:
    """[lo, hi) of beta with s(n) = floor(alpha*n + beta) for all observed n; empty if lo >= hi."""
    a = (
        Decimal(alpha.numerator) / Decimal(alpha.denominator)
        if isinstance(alpha, Fraction)
        else alpha
    )
    lo = max(Decimal(v) - a * (start + i) for i, v in enumerate(values))
    hi = min(Decimal(v + 1) - a * (start + i) for i, v in enumerate(values))
    return float(lo), float(hi)


def mine(seq: Sequence, cfg: dict[str, Any]) -> list[Candidate]:
    min_points = cfg.get("min_points", 30)
    max_points = cfg.get("max_points", 3000)
    vals = seq.values[:max_points]
    if len(vals) < min_points:
        return []
    diffs = set(np.diff(np.asarray(vals, dtype=object)).tolist())
    # floor(alpha n + beta) has consecutive differences in {floor(alpha), ceil(alpha)};
    # a single difference value is an arithmetic progression (left to other miners).
    if len(diffs) != 2 or max(diffs) - min(diffs) != 1:
        return []
    lo, hi = alpha_interval(vals)
    if not lo < hi:
        return []
    end = seq.start + len(vals) - 1
    base_evidence = {
        "observed_range": [seq.start, end],
        "alpha_interval": [str(lo), str(hi)],
        "alpha_interval_float": [float(lo), float(hi)],
        "support": len(vals) - 2,
    }

    def cand(alpha_name: str | None, alpha: str | None, statement: str, extra: dict) -> Candidate:
        return Candidate(
            kind="floor_linear",
            sequence_id=seq.id,
            params={
                "alpha_name": alpha_name,
                "alpha": alpha,
                "n0": seq.start,
                "alpha_interval": [str(lo), str(hi)],
            },
            statement=statement,
            evidence={**base_evidence, **extra},
            method=METHOD,
            sequence_meta=seq.meta,
        )

    # The weak statement (some real alpha works) is always proposed. Stronger guesses for
    # alpha (a simple rational, or a named constant) are proposed alongside it, so that a
    # refuted guess does not take the weak statement down with it.
    out = [
        cand(
            None,
            None,
            f"s(n) = floor(alpha*n + beta) for all n >= {seq.start}, for some real "
            f"alpha in ({float(lo):.10g}, {float(hi):.10g}) and beta",
            {},
        )
    ]
    q = simplest_between(lo, hi)
    if q.denominator <= cfg.get("max_rational_denominator", len(vals) // 4):
        b_lo, b_hi = beta_interval(vals, seq.start, q)
        out.append(
            cand(
                None,
                str(q),
                f"s(n) = floor(({q})*n + beta) for all n >= {seq.start}, "
                f"some beta in [{b_lo:.6g}, {b_hi:.6g})",
                {"beta_interval": [b_lo, b_hi]},
            )
        )
    allowed = cfg.get("constants")
    for name, value in CONSTANTS.items():
        if allowed is not None and name not in allowed:
            continue
        if float(lo) < float(value) < float(hi):
            b_lo, b_hi = beta_interval(vals, seq.start, value)
            if b_lo < b_hi:
                out.append(
                    cand(
                        name,
                        None,
                        f"s(n) = floor({name}*n + beta) for all n >= {seq.start}, "
                        f"some beta in [{b_lo:.6g}, {b_hi:.6g})",
                        {"beta_interval": [b_lo, b_hi]},
                    )
                )
    return out
