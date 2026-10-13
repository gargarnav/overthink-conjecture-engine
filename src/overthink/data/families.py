"""Builders: turn a family's `params` into a DataFrame matching its schema."""

from __future__ import annotations

from collections.abc import Callable
from itertools import combinations
from typing import Any

import numpy as np
import polars as pl

from overthink.data.schema import get_schema
from overthink.games import chomp, subtraction, wythoff


def _subtraction_sets(params: dict[str, Any]) -> list[list[int]]:
    sets = [sorted({int(x) for x in s}) for s in params.get("sets", [])]
    if "all_subsets_of" in params:
        m = int(params["all_subsets_of"])
        max_size = int(params.get("max_size", m))
        for k in range(1, max_size + 1):
            sets.extend(list(c) for c in combinations(range(1, m + 1), k))
    if not sets:
        raise ValueError("subtraction: give 'sets' and/or 'all_subsets_of'")
    return sorted({tuple(s): s for s in sets}.values())


def build_subtraction(params: dict[str, Any]) -> pl.DataFrame:
    n_max = int(params["n_max"])
    frames = []
    for s in _subtraction_sets(params):
        frames.append(
            pl.DataFrame(
                {
                    "subtraction_set": ",".join(map(str, s)),
                    "n": np.arange(n_max + 1, dtype=np.uint32),
                    "grundy": subtraction.grundy(s, n_max),
                }
            )
        )
    return pl.concat(frames)


def build_wythoff(params: dict[str, Any]) -> pl.DataFrame:
    n = int(params["n"])
    g = wythoff.grundy_table(n)
    x, y = np.indices((n, n), dtype=np.uint32)
    return pl.DataFrame({"x": x.ravel(), "y": y.ravel(), "grundy": g.ravel()})


def build_wythoff_subtraction(params: dict[str, Any]) -> pl.DataFrame:
    n = int(params["n"])
    x, y = np.indices((n, n), dtype=np.uint32)
    frames = []
    for s in _subtraction_sets(params):
        g = wythoff.subtraction_grundy_table(s, n)
        frames.append(
            pl.DataFrame(
                {
                    "subtraction_set": ",".join(map(str, s)),
                    "x": x.ravel(),
                    "y": y.ravel(),
                    "grundy": g.ravel(),
                }
            )
        )
    return pl.concat(frames)


def build_chomp4(params: dict[str, Any]) -> pl.DataFrame:
    max_a = int(params["max_a"])
    max_c = params.get("max_c")
    arr = chomp.chomp4_p_positions(max_a, None if max_c is None else int(max_c))
    return pl.DataFrame({k: arr[:, i] for i, k in enumerate("abcd")})


BUILDERS: dict[str, Callable[[dict[str, Any]], pl.DataFrame]] = {
    "subtraction": build_subtraction,
    "wythoff": build_wythoff,
    "chomp4": build_chomp4,
    "wythoff_subtraction": build_wythoff_subtraction,
}


def build(family: str, params: dict[str, Any]) -> pl.DataFrame:
    """Build the dataset, cast to the family schema, and sort canonically."""
    schema = get_schema(family)
    df = BUILDERS[family](params)
    df = df.select(pl.col(c.name).cast(c.dtype) for c in schema.columns)
    return df.sort(schema.sort_by)
