"""Wythoff's game: two heaps; remove any positive number from one heap, or the same
positive number from both."""

from __future__ import annotations

import math

import numpy as np

from overthink import _core


def grundy_table(n: int) -> np.ndarray:
    """n x n array of Grundy values G(x, y), 0 <= x, y < n (Rust implementation)."""
    return _core.wythoff_grundy(n)


def grundy_table_reference(n: int) -> list[list[int]]:
    """Pure-Python Grundy table, straight from the definition. Test oracle."""
    g = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            opts = {g[x - k][y] for k in range(1, x + 1)}
            opts |= {g[x][y - k] for k in range(1, y + 1)}
            opts |= {g[x - k][y - k] for k in range(1, min(x, y) + 1)}
            v = 0
            while v in opts:
                v += 1
            g[x][y] = v
    return g


def p_positions_closed_form(k_max: int) -> list[tuple[int, int]]:
    """Wythoff's theorem: P-positions (floor(k*phi), floor(k*phi) + k) for k = 0..k_max.

    floor(k*phi) is computed exactly as (k + isqrt(5k^2)) // 2.
    """
    return [
        ((k + math.isqrt(5 * k * k)) // 2, (k + math.isqrt(5 * k * k)) // 2 + k)
        for k in range(k_max + 1)
    ]
