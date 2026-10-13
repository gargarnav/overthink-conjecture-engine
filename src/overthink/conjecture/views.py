# SPDX-License-Identifier: MIT
"""Turn a dataset table into integer sequences to mine. Nothing here is game-specific.

Views
-----
grouped      For every integer column Y that is a function of all other columns (detected
             from the data), and every other integer column X: fix the remaining columns
             (the group; integer group values limited to <= max_group_value) and read Y as
             a sequence over consecutive values of X.
zero_set     If the table has a `grundy` column, the P-positions (grundy == 0) form a new
             table "P" that gets the grouped and enumeration views.
enumeration  For tables that are sets of positions (no `grundy` value column) with at most
             two integer columns (per group of string columns):
             sort the rows and read each integer column, and their difference, as a
             sequence over the rank. If swapping the two columns maps the set to itself,
             only rows with first <= second are used.
second_order Parameters of first-order (additive) periodicity candidates (period, delta,
             n0) read as sequences over one integer group column, the others fixed.

Transforms applied to every grouped sequence: `raw` (Y) and `minus_index` (Y - X).

Sequences are cut at the first gap in X, so each one is a run of consecutive indices.
Identical sequences (same start and values) are mined once; the duplicates are listed
in `meta["aliases"]`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import polars as pl

from overthink.conjecture.types import Candidate, Sequence

PERIOD_KINDS = ("periodic", "additive_periodic")


def _int_cols(df: pl.DataFrame) -> list[str]:
    return [c for c in df.columns if df[c].dtype.is_integer()]


def functional_targets(df: pl.DataFrame) -> list[str]:
    """Non-constant integer columns whose value is determined by all the other columns."""
    out = []
    for t in _int_cols(df):
        others = [c for c in df.columns if c != t]
        if not others or df[t].n_unique() <= 1:
            continue
        k = df.group_by(others).agg(pl.col(t).n_unique().alias("_k"))["_k"].max()
        if k == 1:
            out.append(t)
    return out


def _contiguous_run(idx: list[int], vals: list[int]) -> tuple[int, list[int]]:
    pairs = sorted(zip(idx, vals, strict=True))
    start = pairs[0][0]
    run = []
    for k, (i, v) in enumerate(pairs):
        if i != start + k:
            break
        run.append(int(v))
    return start, run


def _fmt_group(group: dict[str, Any]) -> str:
    return ",".join(f"{k}={v}" for k, v in group.items()) or "-"


def grouped_views(df: pl.DataFrame, dataset: str, table: str, cfg: dict) -> list[Sequence]:
    max_g = cfg.get("max_group_value", 30)
    min_len = cfg.get("min_length", 30)
    transforms = cfg.get("transforms", ["raw", "minus_index"])
    ints = _int_cols(df)
    out = []
    for target in functional_targets(df):
        for index in ints:
            if index == target:
                continue
            group_cols = [c for c in df.columns if c not in (target, index)]
            sub = df
            for g in group_cols:
                if g in ints:
                    sub = sub.filter(pl.col(g) <= max_g)
            if sub.height == 0:
                continue
            if group_cols:
                groups = (
                    sub.group_by(group_cols).agg(pl.col(index), pl.col(target)).sort(group_cols)
                )
            else:
                groups = sub.select(pl.col(index).implode(), pl.col(target).implode())
            for row in groups.iter_rows(named=True):
                start, run = _contiguous_run(row[index], row[target])
                if len(run) < min_len:
                    continue
                group = {g: row[g] for g in group_cols}
                for tr in transforms:
                    values = run if tr == "raw" else [v - (start + i) for i, v in enumerate(run)]
                    meta = {
                        "dataset": dataset,
                        "table": table,
                        "view": "grouped",
                        "target": target,
                        "index": index,
                        "group": group,
                        "transform": tr,
                    }
                    sid = f"{dataset}/{table}|{target}~{index}|{_fmt_group(group)}|{tr}"
                    out.append(Sequence(sid, values, start, meta))
    return out


def enumeration_views(df: pl.DataFrame, dataset: str, table: str, cfg: dict) -> list[Sequence]:
    min_len = cfg.get("min_length", 30)
    ints = _int_cols(df)
    if not 1 <= len(ints) <= 2:
        return []
    group_cols = [c for c in df.columns if c not in ints]
    parts = df.partition_by(group_cols, as_dict=True) if group_cols else {(): df}
    out = []
    for key, part in sorted(parts.items(), key=lambda kv: str(kv[0])):
        group = dict(zip(group_cols, key, strict=True))
        rows = part.select(ints)
        symmetric = False
        if len(ints) == 2:
            x, y = ints
            swapped = rows.select(pl.col(y).alias(x), pl.col(x).alias(y))
            symmetric = rows.sort(ints).equals(swapped.sort(ints))
            if symmetric:
                rows = rows.filter(pl.col(x) <= pl.col(y))
        rows = rows.sort(ints)
        if rows.height < min_len:
            continue
        cols = {c: rows[c].to_list() for c in ints}
        if len(ints) == 2:
            cols[f"{ints[1]}-{ints[0]}"] = [b - a for a, b in zip(*cols.values(), strict=True)]
        for name, values in cols.items():
            meta = {
                "dataset": dataset,
                "table": table,
                "view": "enumeration",
                "column": name,
                "group": group,
                "symmetric_half": symmetric,
            }
            sid = f"{dataset}/{table}|enum:{name}|{_fmt_group(group)}"
            out.append(Sequence(sid, [int(v) for v in values], 0, meta))
    return out


def dedupe(seqs: list[Sequence]) -> list[Sequence]:
    seen: dict[tuple, Sequence] = {}
    for s in seqs:
        key = (s.start, tuple(s.values))
        if key in seen:
            seen[key].meta.setdefault("aliases", []).append({"id": s.id, "meta": dict(s.meta)})
        else:
            seen[key] = s
    return list(seen.values())


def dataset_tables(df: pl.DataFrame, cfg: dict) -> dict[str, pl.DataFrame]:
    """The tables views are built from: the data itself and, for Grundy data, its P-positions."""
    tables = {"data": df}
    if cfg.get("zero_set", True) and "grundy" in df.columns:
        tables["P"] = df.filter(pl.col("grundy") == 0).drop("grundy")
    return tables


def build_views(df: pl.DataFrame, dataset: str, cfg: dict) -> list[Sequence]:
    tables = dataset_tables(df, cfg)
    seqs = []
    for name, t in tables.items():
        seqs += grouped_views(t, dataset, name, cfg)
        # Enumeration lists the elements of a set of positions; a table of values is not one
        # (enumerating it would only restate its index column).
        if cfg.get("enumeration", True) and "grundy" not in t.columns:
            seqs += enumeration_views(t, dataset, name, cfg)
    seqs = dedupe(seqs)
    cap = cfg.get("max_sequences", 50_000)
    if len(seqs) > cap:
        raise ValueError(f"{dataset}: {len(seqs)} sequences exceeds max_sequences={cap}")
    return seqs


def second_order_views(cands: list[Candidate], seqs: list[Sequence], cfg: dict) -> list[Sequence]:
    """Sequences of first-order period parameters over one integer group column."""
    min_len = cfg.get("min_length", 12)
    by_id = {s.id: s for s in seqs}
    # (dataset, table, target, index, transform) -> {group tuple: params}
    families: dict[tuple, dict[tuple, dict]] = defaultdict(dict)
    for c in cands:
        if c.kind not in PERIOD_KINDS:
            continue
        s = by_id.get(c.sequence_id)
        if s is None:
            continue
        metas = [s.meta] + [a["meta"] for a in s.meta.get("aliases", [])]
        for m in metas:
            if m.get("view") != "grouped":
                continue
            fam = (m["dataset"], m["table"], m["target"], m["index"], m["transform"])
            families[fam][tuple(sorted(m["group"].items()))] = {
                "period": c.params["period"],
                "delta": c.params["delta"],
                "n0": c.params["n0"],
            }
    out = []
    for fam, by_group in sorted(families.items()):
        if not by_group:
            continue
        group_cols = [k for k, _ in next(iter(by_group))]
        for g in group_cols:
            if not all(isinstance(dict(k)[g], int) for k in by_group):
                continue
            lines: dict[tuple, dict[int, dict]] = defaultdict(dict)
            for key, params in by_group.items():
                d = dict(key)
                fixed = tuple((k, v) for k, v in key if k != g)
                lines[fixed][d[g]] = params
            for fixed, pts in sorted(lines.items()):
                xs = sorted(pts)
                for param in ("period", "delta", "n0"):
                    start, run = _contiguous_run(xs, [pts[x][param] for x in xs])
                    if len(run) < min_len:
                        continue
                    ds, table, target, index, tr = fam
                    meta = {
                        "dataset": ds,
                        "table": table,
                        "view": "second_order",
                        "source": {"target": target, "index": index, "transform": tr},
                        "param": param,
                        "over": g,
                        "fixed": dict(fixed),
                    }
                    sid = (
                        f"{ds}/{table}|{target}~{index}|{tr}|{param} over {g}"
                        f"|{_fmt_group(dict(fixed))}"
                    )
                    out.append(Sequence(sid, run, start, meta))
    return dedupe(out)
