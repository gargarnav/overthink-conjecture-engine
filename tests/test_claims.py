"""Claim language: safe compilation and checking."""

import numpy as np
import polars as pl
import pytest

from overthink.conjecture.claims import ClaimError, check_claim, compile_expr, validate
from overthink.games import wythoff


@pytest.fixture
def tables():
    g = wythoff.subtraction_grundy_table([1], 40)
    x, y = np.indices(g.shape, dtype=np.uint32)
    df = pl.DataFrame({"subtraction_set": "1", "x": x.ravel(), "y": y.ravel(), "grundy": g.ravel()})
    return {"data": df, "P": df.filter(pl.col("grundy") == 0).drop("grundy")}


@pytest.mark.parametrize(
    "bad",
    [
        "__import__('os')",
        "x.__class__",
        "open('f')",
        "lambda: 1",
        "[i for i in x]",
        "x if y",
        "nosuchcol > 1",
        "x in y",
    ],
)
def test_whitelist_rejects(bad):
    with pytest.raises(ClaimError):
        compile_expr(bad, ["x", "y"])


def test_expression_semantics():
    df = pl.DataFrame({"x": [3, 4, 9], "y": [5, 1, 9]})
    out = df.select(
        compile_expr("y - x", df.columns).alias("d"),
        compile_expr("(x % 2 == 0) or (x == y)", df.columns).alias("b"),
        compile_expr("min(x, y) if x > 3 else -1", df.columns).alias("m"),
        compile_expr("x in (3, 9) and not y < 5", df.columns).alias("i"),
    )
    assert out["d"].to_list() == [2, -3, 0]
    assert out["b"].to_list() == [False, True, True]
    assert out["m"].to_list() == [-1, 1, 9]
    assert out["i"].to_list() == [True, False, True]


def test_predicate_true_and_false(tables):
    true = {
        "kind": "predicate",
        "table": "data",
        "group": {"subtraction_set": "1"},
        "assert": "(grundy == 0) == (x % 2 == 0 and y % 2 == 0)",
    }
    assert check_claim(true, tables)["status"] == "holds"
    false = {"kind": "predicate", "table": "P", "assert": "x == y"}
    res = check_claim(false, tables)
    assert res["status"] == "violated" and res["counterexample"] == {
        "subtraction_set": "1",
        "x": 0,
        "y": 2,
    }


def test_unsigned_columns_do_not_wrap(tables):
    claim = {"kind": "predicate", "table": "P", "where": "y < x", "assert": "y - x < 0"}
    assert check_claim(claim, tables)["status"] == "holds"


def test_translation():
    # value = (x + 2y) mod 3 has period 3 in y and period 3 in x, but not period 1 in y
    x, y = np.indices((30, 30))
    df = pl.DataFrame({"x": x.ravel(), "y": y.ravel(), "v": ((x + 2 * y) % 3).ravel()})
    t = {"data": df}
    assert (
        check_claim({"kind": "translation", "table": "data", "shift": {"y": 3}, "value": "v"}, t)[
            "status"
        ]
        == "holds"
    )
    diag = {"kind": "translation", "table": "data", "shift": {"x": 1, "y": 1}, "value": "v"}
    assert check_claim(diag, t)["status"] == "holds"  # x + 2y changes by 3
    res = check_claim({"kind": "translation", "table": "data", "shift": {"y": 1}, "value": "v"}, t)
    assert res["status"] == "violated"
    assert res["counterexample"]["value_at_shift"] != res["counterexample"]["predicted"]
    assert (
        check_claim(
            {
                "kind": "translation",
                "table": "data",
                "shift": {"y": 1},
                "value": "v",
                "where": "y < 0",
            },
            t,
        )["status"]
        == "insufficient"
    )


def test_statistic(tables):
    dens = {
        "kind": "statistic",
        "table": "data",
        "expr": "grundy == 0",
        "value": 0.25,
        "tolerance": 0.01,
    }
    assert check_claim(dens, tables)["status"] == "holds"
    assert check_claim({**dens, "value": 0.4}, tables)["status"] == "violated"


def test_validate_catches_malformed(tables):
    with pytest.raises(ClaimError):
        validate({"kind": "predicate", "table": "data"}, tables)
    with pytest.raises(ClaimError):
        validate(
            {"kind": "translation", "table": "data", "shift": {"z": 1}, "value": "grundy"}, tables
        )
    with pytest.raises(ClaimError):
        validate({"kind": "nope", "table": "data"}, tables)
