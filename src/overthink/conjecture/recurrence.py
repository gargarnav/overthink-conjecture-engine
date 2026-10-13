"""Linear recurrences with constant rational coefficients (Berlekamp-Massey over Q).

Finds the shortest recurrence s(n) = c_1 s(n-1) + ... + c_L s(n-L) that generates the
observed sequence from some offset on. A recurrence of order L is determined by 2L terms,
so the evidence is the number of terms observed beyond those 2L.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from overthink.conjecture.types import Candidate, Sequence

METHOD = "berlekamp-massey@1"


def berlekamp_massey(values: list[int], max_order: int) -> list[Fraction] | None:
    """Coefficients [c_1..c_L] of the shortest recurrence generating `values`, or None if
    its order would exceed `max_order`."""
    s = [Fraction(v) for v in values]
    conn, prev = [Fraction(1)], [Fraction(1)]  # connection polynomials C(x), B(x)
    order, shift, prev_disc = 0, 1, Fraction(1)
    for n in range(len(s)):
        disc = s[n] + sum(conn[i] * s[n - i] for i in range(1, min(order, len(conn) - 1) + 1))
        if disc == 0:
            shift += 1
            continue
        coef = disc / prev_disc
        new = conn + [Fraction(0)] * max(0, len(prev) + shift - len(conn))
        for i, b in enumerate(prev):
            new[i + shift] -= coef * b
        if 2 * order <= n:
            prev, prev_disc, order, shift = conn, disc, n + 1 - order, 1
            if order > max_order:
                return None
        else:
            shift += 1
        conn = new
    conn = conn + [Fraction(0)] * (order + 1 - len(conn))
    return [-c for c in conn[1 : order + 1]]


def _fmt(c: Fraction) -> str:
    return str(c.numerator) if c.denominator == 1 else f"({c})"


def mine(seq: Sequence, cfg: dict[str, Any]) -> list[Candidate]:
    max_order = cfg.get("max_order", 12)
    min_support = cfg.get("min_support", 20)
    n = len(seq.values)
    for frac in cfg.get("suffix_starts", [0, 0.125, 0.25, 0.5]):
        t = int(frac * n)
        tail = seq.values[t:]
        coeffs = berlekamp_massey(tail, max_order)
        if coeffs is None or len(coeffs) == 0:
            continue
        order = len(coeffs)
        support = len(tail) - 2 * order
        if support < min_support:
            continue
        n0 = seq.start + t
        terms = " + ".join(f"{_fmt(c)}*s(n-{i})" for i, c in enumerate(coeffs, start=1) if c != 0)
        return [
            Candidate(
                kind="linear_recurrence",
                sequence_id=seq.id,
                params={"coefficients": [str(c) for c in coeffs], "n0": n0},
                statement=f"s(n) = {terms} for all n >= {n0 + order}",
                evidence={
                    "observed_range": [seq.start, seq.end],
                    "order": order,
                    "support": support,
                },
                method=METHOD,
                sequence_meta=seq.meta,
            )
        ]
    return []
