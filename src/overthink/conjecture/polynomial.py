# SPDX-License-Identifier: MIT
"""Polynomial and quasi-polynomial miner (difference tables).

Finds a modulus m and degree k such that, for all observed n >= n0, s(n) = P_r(n) with
r = n mod m and each P_r a polynomial of degree <= k with rational coefficients. Lower
cases are left to the periodicity miner: degree <= 1 with m = 1 is additive periodicity,
and degree 0 is ordinary periodicity.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import numpy as np

from overthink.conjecture.types import Candidate, Sequence

METHOD = "difference-table@1"


def _last_nonzero_kth_difference(sub: list[int], k: int) -> int | None:
    """Smallest j such that the k-th forward differences of sub vanish from j on,
    or None if there are none to check."""
    d = np.array(sub, dtype=object)
    for _ in range(k):
        d = d[1:] - d[:-1]
    if len(d) == 0:
        return None
    nz = np.nonzero(d != 0)[0]
    return int(nz[-1]) + 1 if len(nz) else 0


def fit_polynomial(points: list[tuple[int, int]]) -> list[Fraction]:
    """Exact coefficients [c_0, c_1, ...] of the interpolating polynomial (lowest degree first)."""
    k = len(points)
    rows = [[Fraction(x) ** j for j in range(k)] + [Fraction(y)] for x, y in points]
    for col in range(k):
        piv = next(r for r in range(col, k) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        for r in range(k):
            if r != col and rows[r][col] != 0:
                f = rows[r][col] / rows[col][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[col], strict=True)]
    coeffs = [rows[i][k] / rows[i][i] for i in range(k)]
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def eval_polynomial(coeffs: list[Fraction], n: int) -> Fraction:
    return sum((c * Fraction(n) ** j for j, c in enumerate(coeffs)), Fraction(0))


def format_polynomial(coeffs: list[Fraction]) -> str:
    terms = []
    for j in range(len(coeffs) - 1, -1, -1):
        c = coeffs[j]
        if c == 0:
            continue
        cs = str(c) if c.denominator == 1 else f"({c})"
        if j == 0:
            terms.append(cs)
            continue
        mono = "n" if j == 1 else f"n^{j}"
        terms.append(mono if c == 1 else f"-{mono}" if c == -1 else f"{cs}*{mono}")
    return " + ".join(terms) if terms else "0"


def find_quasi_polynomial(
    values: list[int], max_degree: int, max_modulus: int, min_support: int
) -> tuple[int, int, int, int] | None:
    """Return (m, k, t, support) with t the 0-based start offset, minimizing t + m*(k+1)."""
    n = len(values)
    best = None
    for m in range(1, max_modulus + 1):
        for k in range(1, max_degree + 1):
            if m == 1 and k <= 1:
                continue
            t = 0
            for r in range(m):
                sub = values[r::m]
                j = _last_nonzero_kth_difference(sub, k + 1)
                if j is None:
                    t = n
                    break
                t = max(t, r + j * m)
            npar = m * (k + 1)
            support = n - t - npar
            if support < min_support:
                continue
            if best is None or t + npar < best[2] + best[0] * (best[1] + 1):
                best = (m, k, t, support)
    return best


def mine(seq: Sequence, cfg: dict[str, Any]) -> list[Candidate]:
    found = find_quasi_polynomial(
        seq.values,
        max_degree=cfg.get("max_degree", 4),
        max_modulus=cfg.get("max_modulus", 6),
        min_support=cfg.get("min_support", 20),
    )
    if found is None:
        return []
    m, k, t, support = found
    n0 = seq.start + t
    polys: dict[int, list[Fraction]] = {}
    for i in range(t, t + m):
        r = (seq.start + i) % m
        pts = [(seq.start + j, seq.values[j]) for j in range(i, len(seq.values), m)][: k + 1]
        polys[r] = fit_polynomial(pts)
    degree = max(len(c) - 1 for c in polys.values())
    # Lower cases belong to the periodicity miner (same statement, simpler form).
    if degree == 0 or (m == 1 and degree <= 1):
        return []
    if m == 1:
        kind = "polynomial"
        statement = f"s(n) = {format_polynomial(polys[0])} for all n >= {n0}"
    else:
        kind = "quasi_polynomial"
        cases = "; ".join(f"n = {r} mod {m}: {format_polynomial(polys[r])}" for r in sorted(polys))
        statement = f"for all n >= {n0}, s(n) = [{cases}]"
    return [
        Candidate(
            kind=kind,
            sequence_id=seq.id,
            params={
                "modulus": m,
                "n0": n0,
                "polynomials": {str(r): [str(c) for c in polys[r]] for r in sorted(polys)},
            },
            statement=statement,
            evidence={
                "observed_range": [seq.start, seq.end],
                "degree": degree,
                "support": support,
            },
            method=METHOD,
            sequence_meta=seq.meta,
        )
    ]
