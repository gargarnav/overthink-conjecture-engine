"""Subtraction games: a heap of n tokens; a move removes s tokens for some s in S."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from overthink import _core


def _check_moves(moves: Iterable[int]) -> list[int]:
    moves = sorted({int(s) for s in moves})
    if not moves or moves[0] < 1:
        raise ValueError("subtraction set must be non-empty positive integers")
    return moves


def grundy(moves: Iterable[int], n_max: int) -> np.ndarray:
    """Grundy values g(0..n_max) (Rust implementation)."""
    return _core.subtraction_grundy(_check_moves(moves), n_max)


def grundy_reference(moves: Iterable[int], n_max: int) -> list[int]:
    """Pure-Python Grundy values g(0..n_max), straight from the definition. Test oracle."""
    moves = _check_moves(moves)
    g: list[int] = []
    for n in range(n_max + 1):
        opts = {g[n - s] for s in moves if s <= n}
        v = 0
        while v in opts:
            v += 1
        g.append(v)
    return g
