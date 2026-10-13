"""Dataset schemas: the single source of truth for column names, types and meaning.

Bump SCHEMA_VERSION whenever a column is added, removed, renamed or changes meaning.
"""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl

SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class Column:
    name: str
    dtype: pl.DataType
    description: str


@dataclass(frozen=True)
class FamilySchema:
    family: str
    title: str
    rules: str
    contents: str
    columns: tuple[Column, ...]
    sort_by: tuple[str, ...]
    sample_filter: pl.Expr
    sample_description: str

    @property
    def polars_schema(self) -> dict[str, pl.DataType]:
        return {c.name: c.dtype for c in self.columns}


SCHEMAS: dict[str, FamilySchema] = {
    s.family: s
    for s in [
        FamilySchema(
            family="subtraction",
            title="Subtraction games: Grundy values",
            rules=(
                "A heap of n tokens. A move removes s tokens for some s in the subtraction "
                "set S (s <= n). The player unable to move loses (normal play)."
            ),
            contents="Every n in 0..n_max for every listed subtraction set S.",
            columns=(
                Column("subtraction_set", pl.String(), "S as comma-separated ascending integers"),
                Column("n", pl.UInt32(), "heap size"),
                Column("grundy", pl.UInt32(), "Sprague-Grundy value g_S(n); 0 iff P-position"),
            ),
            sort_by=("subtraction_set", "n"),
            sample_filter=pl.col("n") <= 60,
            sample_description="rows with n <= 60",
        ),
        FamilySchema(
            family="wythoff",
            title="Wythoff's game: Grundy values",
            rules=(
                "Two heaps (x, y). A move removes any positive number of tokens from one heap, "
                "or the same positive number from both. Normal play."
            ),
            contents="Every position (x, y) with 0 <= x, y < n.",
            columns=(
                Column("x", pl.UInt32(), "first heap"),
                Column("y", pl.UInt32(), "second heap"),
                Column("grundy", pl.UInt32(), "Sprague-Grundy value G(x, y); 0 iff P-position"),
            ),
            sort_by=("x", "y"),
            sample_filter=(pl.col("x") < 32) & (pl.col("y") < 32),
            sample_description="rows with x, y < 32",
        ),
        FamilySchema(
            family="wythoff_subtraction",
            title="Wythoff subtraction games W(S): Grundy values",
            rules=(
                "Two heaps (x, y) and a finite subtraction set S. A move removes s tokens from "
                "one heap, or s tokens from both heaps, for some s in S. Normal play. This is "
                "the finite two-dimensional subtraction game with move vectors (s,0), (0,s), "
                "(s,s), s in S."
            ),
            contents="Every position (x, y) with 0 <= x, y < n, for every listed set S.",
            columns=(
                Column("subtraction_set", pl.String(), "S as comma-separated ascending integers"),
                Column("x", pl.UInt32(), "first heap"),
                Column("y", pl.UInt32(), "second heap"),
                Column("grundy", pl.UInt32(), "Sprague-Grundy value; 0 iff P-position"),
            ),
            sort_by=("subtraction_set", "x", "y"),
            sample_filter=(pl.col("x") < 16) & (pl.col("y") < 16),
            sample_description="rows with x, y < 16",
        ),
        FamilySchema(
            family="chomp4",
            title="4-row Chomp: P-positions",
            rules=(
                "Row lengths a >= b >= c >= d >= 0 with a >= 1. Square (0,0) is poisoned and "
                "cannot be taken. A move picks a square (i, j) != (0,0) inside the position "
                "and removes it with every square (i', j') where i' >= i and j' >= j. "
                "The player unable to move loses, so (1,0,0,0) is a P-position."
            ),
            contents=(
                "Every P-position with a <= max_a (and c <= max_c). Positions not listed, "
                "within those bounds, are N-positions. For each (b, c, d) at most one a gives "
                "a P-position."
            ),
            columns=(
                Column("a", pl.UInt32(), "length of row 1 (the row with the poisoned square)"),
                Column("b", pl.UInt32(), "length of row 2"),
                Column("c", pl.UInt32(), "length of row 3"),
                Column("d", pl.UInt32(), "length of row 4"),
            ),
            sort_by=("a", "b", "c", "d"),
            sample_filter=pl.col("a") <= 30,
            sample_description="P-positions with a <= 30",
        ),
    ]
}


def get_schema(family: str) -> FamilySchema:
    try:
        return SCHEMAS[family]
    except KeyError:
        raise ValueError(f"unknown family {family!r}; known: {sorted(SCHEMAS)}") from None


def validate(df: pl.DataFrame, family: str) -> None:
    """Raise if `df` does not match the family schema exactly (names, order, dtypes)."""
    expected = get_schema(family).polars_schema
    actual = dict(df.schema)
    if actual != expected:
        raise ValueError(f"schema mismatch for {family}: expected {expected}, got {actual}")
