# SPDX-License-Identifier: MIT
"""Functional dependencies as conjectures: mining, checking, falsification."""

import json

import polars as pl
import yaml

from overthink.conjecture.dependencies import check_table, mine_tables
from overthink.conjecture.run import run_mining
from overthink.conjecture.views import dataset_tables
from overthink.data.families import build
from overthink.data.store import generate
from overthink.falsify.falsifier import falsify_run


def _targets(cands):
    return {(c.params["table"], c.params["target"]) for c in cands}


def test_chomp4_unique_extension_and_its_siblings_are_proposed():
    df = build("chomp4", {"max_a": 25})
    cands = mine_tables({"data": df}, "chomp")
    assert _targets(cands) == {("data", t) for t in "abcd"}
    d = next(c for c in cands if c.params["target"] == "d")
    assert d.params["determinants"] == ["a", "b", "c"]
    assert d.evidence["distinct_determinant_tuples"] == df.height


def test_wythoff_value_column_not_proposed_but_p_pairing_is():
    df = build("wythoff", {"n": 60})
    cands = mine_tables(dataset_tables(df, {}), "w")
    assert ("data", "grundy") not in _targets(cands)  # definitional
    assert {("P", "x"), ("P", "y")} <= _targets(cands)  # each heap size has one partner


def test_check_table_finds_violation():
    df = pl.DataFrame({"x": [0, 1, 1, 2], "y": [5, 6, 7, 8]})
    res = check_table({"table": "data", "target": "y", "determinants": ["x"]}, {"data": df})
    assert res["status"] == "violated"
    assert res["counterexample"]["determinants"] == {"x": 1}
    assert res["counterexample"]["observed"] == [6, 7]


def test_fd_candidates_falsified_on_larger_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for ds, n in [("w", 120), ("w_big", 1200)]:
        cfg = tmp_path / f"{ds}.yaml"
        cfg.write_text(json.dumps({"dataset": ds, "family": "wythoff", "params": {"n": n}}))
        generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    run_cfg = {
        "run_name": "fd",
        "datasets": [{"id": "w", "proposal_window": {"x": 99, "y": 99}}],
        "views": {"min_length": 30},
        "miners": {"functional_dependencies": {"enabled": True}},
    }
    (tmp_path / "run.yaml").write_text(yaml.safe_dump(run_cfg))
    run_dir = run_mining(tmp_path / "run.yaml", runs_dir=tmp_path / "runs")
    out = falsify_run(run_dir, runs_dir=tmp_path / "runs", dataset_map={"w": "w_big"})
    res = [json.loads(line) for line in (out / "falsification.jsonl").open()]
    fds = [r for r in res if r["kind"] == "functional_dependency"]
    assert fds and all(r["status"] == "survived" for r in fds)
    assert all(
        r["per_sequence"][0]["full_rows"] > r["per_sequence"][0]["proposal_rows"] for r in fds
    )
