"""Chomp on Young-diagram positions with a poisoned corner.

A k-row position is a non-increasing tuple of row lengths r[0] >= ... >= r[k-1] >= 0
with r[0] >= 1. Square (0, 0) in the first row is poisoned and may not be taken, so the
single-square position (1, 0, ..., 0) is terminal, hence a P-position. A move picks
square (i, j) != (0, 0) with j < r[i] and sets r[t] = min(r[t], j) for all t >= i.
"""

from __future__ import annotations

from itertools import combinations_with_replacement

import numpy as np

from overthink import _core

Position = tuple[int, ...]


def options(pos: Position) -> list[Position]:
    """All positions reachable from `pos` in one move."""
    out = []
    for i, ri in enumerate(pos):
        for j in range(1 if i == 0 else 0, ri):
            out.append(pos[:i] + tuple(min(r, j) for r in pos[i:]))
    return out


def all_positions(k: int, n: int) -> list[Position]:
    """All k-row positions with first row at most n."""
    return [
        tuple(sorted(c, reverse=True))
        for c in combinations_with_replacement(range(n + 1), k)
        if max(c) >= 1
    ]


def p_positions_reference(k: int, n: int) -> set[Position]:
    """Brute-force P-positions of k-row Chomp with first row <= n. Test oracle."""
    is_p: dict[Position, bool] = {}
    for pos in sorted(all_positions(k, n), key=sum):  # options always have smaller sum
        is_p[pos] = not any(is_p[o] for o in options(pos))
    return {p for p, v in is_p.items() if v}


def chomp4_p_positions(
    max_a: int, max_c: int | None = None, max_d: int | None = None
) -> np.ndarray:
    """All P-positions (a, b, c, d) of 4-row Chomp with a <= max_a (and c <= max_c, d <= max_d).
    max_d = 0 gives exactly the P-positions of 3-row Chomp (with d = 0 appended).

    Returns an (N, 4) uint32 array with columns a, b, c, d, ordered by (c, d, b).
    Rust implementation; see rust/src/chomp4.rs for the algorithm.
    """
    if max_c is None:
        max_c = max_a
    a, b, c, d = _core.chomp4_p_positions(max_c, max_a, max_d)
    return np.column_stack([a, b, c, d])
