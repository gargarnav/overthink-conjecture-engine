"""Machine-checkable claims about a dataset table, for proposers (e.g. an LLM) that state more
than single-sequence laws.

A claim is a JSON object. Expressions are Python-like and parsed with a strict whitelist
(arithmetic, comparisons, `and`/`or`/`not`, `a if c else b`, `x in (1, 2)`, and the functions
abs, min, max, floor, sqrt), then compiled to vectorized Polars expressions. Nothing is
`eval`-ed. Integer columns are widened to Int64 first, so `y - x` cannot wrap around.

Kinds
-----
predicate     {"kind": "predicate", "table", "group"?, "where"?, "assert"}
              `assert` holds on every row of `table` matching `group` (column == value) and
              `where`.
translation   {"kind": "translation", "table", "group"?, "where"?, "shift": {col: d, ...},
               "value": col, "delta"?: 0}
              For every row r matching group/where whose shifted row r + shift exists:
              value(r + shift) == value(r) + delta. (Periodicity along any direction.)
statistic     {"kind": "statistic", "table", "group"?, "where"?, "expr", "value", "tolerance"}
              The mean of `expr` over the matching rows lies within `tolerance` of `value`.
"""

from __future__ import annotations

import ast
from functools import reduce
from typing import Any

import polars as pl

KINDS = ("predicate", "translation", "statistic")
_FUNCS = {"abs", "min", "max", "floor", "sqrt"}


class ClaimError(ValueError):
    """A claim that is malformed or uses something outside the whitelist."""


def compile_expr(src: str, columns: list[str]) -> pl.Expr:
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError as e:
        raise ClaimError(f"syntax error in {src!r}: {e.msg}") from None
    return _to_polars(tree.body, set(columns), src)


def _to_polars(node: ast.AST, cols: set[str], src: str) -> pl.Expr:
    rec = lambda n: _to_polars(n, cols, src)
    if isinstance(node, ast.Constant) and isinstance(node.value, (bool, int, float)):
        return pl.lit(node.value)
    if isinstance(node, ast.Name):
        if node.id in cols:
            return pl.col(node.id)
        raise ClaimError(f"unknown name {node.id!r} in {src!r}; columns: {sorted(cols)}")
    if isinstance(node, ast.BinOp):
        a, b = rec(node.left), rec(node.right)
        ops = {
            ast.Add: lambda: a + b,
            ast.Sub: lambda: a - b,
            ast.Mult: lambda: a * b,
            ast.FloorDiv: lambda: a // b,
            ast.Mod: lambda: a % b,
            ast.Div: lambda: a / b,
            ast.Pow: lambda: a.pow(b),
        }
        if type(node.op) in ops:
            return ops[type(node.op)]()
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -rec(node.operand)
        if isinstance(node.op, ast.Not):
            return ~rec(node.operand)
    if isinstance(node, ast.BoolOp):
        parts = [rec(v) for v in node.values]
        return (
            reduce(lambda x, y: x & y, parts)
            if isinstance(node.op, ast.And)
            else reduce(lambda x, y: x | y, parts)
        )
    if isinstance(node, ast.Compare):
        terms, left = [], node.left
        for op, right in zip(node.ops, node.comparators, strict=True):
            if isinstance(op, (ast.In, ast.NotIn)):
                if not isinstance(right, (ast.Tuple, ast.List)) or not all(
                    isinstance(e, ast.Constant) for e in right.elts
                ):
                    raise ClaimError(f"'in' needs a literal tuple of constants in {src!r}")
                t = rec(left).is_in([e.value for e in right.elts])
                terms.append(~t if isinstance(op, ast.NotIn) else t)
            else:
                a, b = rec(left), rec(right)
                cmp = {
                    ast.Eq: a == b,
                    ast.NotEq: a != b,
                    ast.Lt: a < b,
                    ast.LtE: a <= b,
                    ast.Gt: a > b,
                    ast.GtE: a >= b,
                }
                if type(op) not in cmp:
                    raise ClaimError(f"unsupported comparison in {src!r}")
                terms.append(cmp[type(op)])
            left = right
        return reduce(lambda x, y: x & y, terms)
    if isinstance(node, ast.IfExp):
        return pl.when(rec(node.test)).then(rec(node.body)).otherwise(rec(node.orelse))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
        name, args = node.func.id, [rec(a) for a in node.args]
        if name not in _FUNCS:
            raise ClaimError(f"function {name!r} not allowed in {src!r}")
        if name == "abs" and len(args) == 1:
            return args[0].abs()
        if name == "floor" and len(args) == 1:
            return args[0].floor()
        if name == "sqrt" and len(args) == 1:
            return args[0].sqrt()
        if name in ("min", "max") and len(args) >= 2:
            return pl.min_horizontal(args) if name == "min" else pl.max_horizontal(args)
        raise ClaimError(f"bad arguments to {name} in {src!r}")
    raise ClaimError(f"unsupported syntax {type(node).__name__} in {src!r}")


def _widen(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(pl.col(c).cast(pl.Int64) for c in df.columns if df[c].dtype.is_integer())


def validate(claim: dict[str, Any], tables: dict[str, pl.DataFrame]) -> None:
    """Raise ClaimError unless the claim is well-formed for these tables."""
    kind = claim.get("kind")
    if kind not in KINDS:
        raise ClaimError(f"kind must be one of {KINDS}, got {kind!r}")
    if claim.get("table") not in tables:
        raise ClaimError(f"unknown table {claim.get('table')!r}; tables: {sorted(tables)}")
    cols = tables[claim["table"]].columns
    for g in claim.get("group", {}) or {}:
        if g not in cols:
            raise ClaimError(f"unknown group column {g!r}")
    exprs = [claim.get("where")] + {
        "predicate": [claim.get("assert")],
        "translation": [],
        "statistic": [claim.get("expr")],
    }[kind]
    for e in exprs:
        if e is not None:
            compile_expr(e, cols)
    if kind == "predicate" and not claim.get("assert"):
        raise ClaimError("predicate needs 'assert'")
    if kind == "translation":
        shift = claim.get("shift")
        if not isinstance(shift, dict) or not shift or any(c not in cols for c in shift):
            raise ClaimError("translation needs 'shift' {column: offset} over existing columns")
        if claim.get("value") not in cols:
            raise ClaimError("translation needs 'value' naming a column")
    if kind == "statistic" and (
        not claim.get("expr") or "value" not in claim or "tolerance" not in claim
    ):
        raise ClaimError("statistic needs 'expr', 'value' and 'tolerance'")


def _domain(claim: dict[str, Any], df: pl.DataFrame) -> pl.DataFrame:
    df = _widen(df)
    for col, v in (claim.get("group") or {}).items():
        df = df.filter(pl.col(col) == v)
    if claim.get("where"):
        df = df.filter(compile_expr(claim["where"], df.columns))
    return df


def check_claim(claim: dict[str, Any], tables: dict[str, pl.DataFrame]) -> dict[str, Any]:
    """Status `holds` / `violated` / `insufficient`, rows checked, and a counterexample."""
    validate(claim, tables)
    full = tables[claim["table"]]
    dom = _domain(claim, full)
    keys = [c for c in dom.columns if c != claim.get("value")]
    if claim["kind"] == "predicate":
        ok = dom.with_columns(compile_expr(claim["assert"], dom.columns).alias("_ok"))
        bad = ok.filter(~pl.col("_ok").fill_null(False))
        res = {"n_checked": dom.height, "n_violations": bad.height}
        if bad.height:
            res["counterexample"] = bad.drop("_ok").sort(dom.columns).row(0, named=True)
    elif claim["kind"] == "translation":
        shift, value, delta = claim["shift"], claim["value"], int(claim.get("delta", 0))
        target = _widen(full)
        for col, v in (claim.get("group") or {}).items():
            target = target.filter(pl.col(col) == v)
        moved = target.with_columns([pl.col(c) - int(d) for c, d in shift.items()]).rename(
            {value: "_shifted"}
        )
        joined = dom.join(moved, on=[c for c in dom.columns if c != value], how="inner")
        bad = joined.filter(pl.col("_shifted") != pl.col(value) + delta)
        res = {"n_checked": joined.height, "n_violations": bad.height}
        if bad.height:
            row = bad.sort(keys).row(0, named=True)
            res["counterexample"] = {
                **{k: row[k] for k in keys},
                value: row[value],
                "value_at_shift": row["_shifted"],
                "predicted": row[value] + delta,
            }
    else:
        vals = dom.select(compile_expr(claim["expr"], dom.columns).cast(pl.Float64).alias("_v"))
        mean = vals["_v"].mean() if dom.height else None
        res = {
            "n_checked": dom.height,
            "observed": mean,
            "claimed": claim["value"],
            "tolerance": claim["tolerance"],
        }
        res["n_violations"] = (
            0 if (mean is not None and abs(mean - claim["value"]) <= claim["tolerance"]) else 1
        )
    if res["n_checked"] == 0:
        res["status"] = "insufficient"
    else:
        res["status"] = "holds" if res["n_violations"] == 0 else "violated"
    return res
