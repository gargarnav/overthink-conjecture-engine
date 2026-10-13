"""Functional dependencies as conjectures.

If, in a table of positions, column T never takes two different values for the same
values of all the other columns, that is a statement about the game ("T is determined by
the rest"). Example: in 4-row Chomp P-positions, d is determined by (a, b, c), which is
Unique Extension.

A value column of a table of values (`grundy` in a table that lists every position) is
determined by construction, so it is not proposed.
"""

from __future__ import annotations

from typing import Any

import polars as pl

from overthink.conjecture.types import Candidate
from overthink.conjecture.views import functional_targets

METHOD = "functional-dependency@1"
VALUE_COLUMNS = ("grundy",)


def mine_tables(tables: dict[str, pl.DataFrame], dataset: str) -> list[Candidate]:
    out = []
    for name, df in tables.items():
        for target in functional_targets(df):
            if name == "data" and target in VALUE_COLUMNS:
                continue
            dets = [c for c in df.columns if c != target]
            n_keys = df.select(dets).n_unique()
            out.append(
                Candidate(
                    kind="functional_dependency",
                    sequence_id=f"{dataset}/{name}|FD:{target}<-({','.join(dets)})",
                    params={"table": name, "target": target, "determinants": dets},
                    statement=(
                        f"In {dataset}/{name}, {target} is determined by "
                        f"({', '.join(dets)}): no two rows share ({', '.join(dets)}) "
                        f"with different {target}"
                    ),
                    evidence={
                        "rows": df.height,
                        "distinct_determinant_tuples": n_keys,
                        "support": df.height,
                    },
                    method=METHOD,
                    sequence_meta={"dataset": dataset, "table": name, "view": "table"},
                )
            )
    return out


def check_table(params: dict[str, Any], tables: dict[str, pl.DataFrame]) -> dict[str, Any]:
    df = tables.get(params["table"])
    if df is None:
        return {"status": "untestable", "reason": "table not present", "n_checked": 0}
    target, dets = params["target"], params["determinants"]
    bad = (
        df.group_by(dets)
        .agg(pl.col(target).unique().alias("_vals"))
        .filter(pl.col("_vals").list.len() > 1)
    )
    res: dict[str, Any] = {
        "status": "holds" if bad.height == 0 else "violated",
        "n_checked": df.height,
        "first_counterexample": None,
    }
    if bad.height:
        row = bad.sort(dets).row(0, named=True)
        res["counterexample"] = {
            "determinants": {d: row[d] for d in dets},
            "observed": sorted(row["_vals"]),
            "predicted": "a single value",
        }
    return res
