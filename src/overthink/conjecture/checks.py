# SPDX-License-Identifier: MIT
"""Test a candidate conjecture against a (typically much longer) version of its sequence.

`check` returns a dict with
    status: "holds" | "violated" | "insufficient" | "unsupported"
    first_counterexample: smallest index n where the statement fails (if known)
    counterexample: {"n", "observed", "predicted"} at that index (predicted may be a range)
    checked_range: [first, last] index whose value was used
    n_checked: number of individual relations verified
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import Any

from overthink.conjecture.constants import CONSTANTS
from overthink.conjecture.floorlinear import alpha_interval
from overthink.conjecture.polynomial import eval_polynomial
from overthink.conjecture.types import Sequence


def _result(
    status: str,
    first: int | None,
    rng: list[int] | None,
    n: int,
    observed: int | None = None,
    predicted: Any = None,
) -> dict[str, Any]:
    out = {"status": status, "first_counterexample": first, "checked_range": rng, "n_checked": n}
    if first is not None:
        out["counterexample"] = {"n": first, "observed": observed, "predicted": predicted}
    return out


def _value_getter(seq: Sequence):
    def s(n: int) -> int:
        return seq.values[n - seq.start]

    return s


def check(kind: str, params: dict[str, Any], seq: Sequence) -> dict[str, Any]:
    s = _value_getter(seq)
    n0 = max(params["n0"], seq.start)
    end = seq.end

    if kind in ("periodic", "additive_periodic"):
        p, delta = params["period"], params["delta"]
        count = 0
        for n in range(n0, end - p + 1):
            if s(n + p) - s(n) != delta:
                return _result("violated", n + p, [n0, end], count, s(n + p), s(n) + delta)
            count += 1
        return _result("holds" if count else "insufficient", None, [n0, end], count)

    if kind == "linear_recurrence":
        coeffs = [Fraction(c) for c in params["coefficients"]]
        order = len(coeffs)
        count = 0
        for n in range(n0 + order, end + 1):
            pred = sum(c * s(n - i) for i, c in enumerate(coeffs, start=1))
            if pred != s(n):
                return _result("violated", n, [n0, end], count, s(n), str(pred))
            count += 1
        return _result("holds" if count else "insufficient", None, [n0, end], count)

    if kind in ("polynomial", "quasi_polynomial"):
        m = params["modulus"]
        polys = {int(r): [Fraction(c) for c in cs] for r, cs in params["polynomials"].items()}
        count = 0
        for n in range(n0, end + 1):
            pred = eval_polynomial(polys[n % m], n)
            if pred != s(n):
                return _result("violated", n, [n0, end], count, s(n), str(pred))
            count += 1
        return _result("holds" if count else "insufficient", None, [n0, end], count)

    if kind == "floor_linear":
        vals = seq.values[n0 - seq.start :]
        if len(vals) < 2:
            return _result("insufficient", None, [n0, end], 0)
        if params.get("alpha") is None and params.get("alpha_name") is None:
            lo, hi = alpha_interval(vals)
            if lo < hi:
                return _result("holds", None, [n0, end], len(vals))
            # Binary search for the shortest infeasible prefix: its last index is the
            # first n at which no (alpha, beta) fits all terms so far.
            good, bad = 2, len(vals)
            while bad - good > 1:
                mid = (good + bad) // 2
                lo_m, hi_m = alpha_interval(vals[:mid])
                good, bad = (mid, bad) if lo_m < hi_m else (good, mid)
            n_bad = n0 + bad - 1
            return _result(
                "violated", n_bad, [n0, end], bad - 1, vals[bad - 1], "no real slope fits"
            )
        if params.get("alpha") is not None:
            q = Fraction(params["alpha"])
            alpha = Decimal(q.numerator) / Decimal(q.denominator)
        else:
            alpha = CONSTANTS[params["alpha_name"]]
        # Scan forward, maintaining the feasible beta interval; the first n that empties it
        # is the first counterexample.
        lo, hi = Decimal("-Infinity"), Decimal("Infinity")
        for i, v in enumerate(vals):
            n = n0 + i
            lo = max(lo, Decimal(v) - alpha * n)
            hi = min(hi, Decimal(v + 1) - alpha * n)
            if lo >= hi:
                return _result("violated", n, [n0, end], i, v, "outside feasible beta range")
        return _result("holds", None, [n0, end], len(vals))

    return _result("unsupported", None, None, 0)
