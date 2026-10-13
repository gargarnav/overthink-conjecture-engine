# SPDX-License-Identifier: MIT
"""Falsifier and registry: refutation, survival, untestable cases, status rules."""

import json

import pytest
import yaml

from overthink.conjecture.run import run_mining
from overthink.data.store import generate
from overthink.falsify.falsifier import falsify_run
from overthink.registry.store import Registry


@pytest.fixture
def mined(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "s.yaml"
    cfg.write_text(
        json.dumps(
            {
                "dataset": "s",
                "family": "subtraction",
                "params": {"sets": [[1, 3, 4], [2, 5, 7]], "n_max": 600},
            }
        )
    )
    generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    run_cfg = {
        "run_name": "t",
        "datasets": [{"id": "s", "proposal_window": {"n": 59}}],
        "views": {"min_length": 30},
        "miners": {},
    }
    (tmp_path / "run.yaml").write_text(yaml.safe_dump(run_cfg))
    return run_mining(tmp_path / "run.yaml", runs_dir=tmp_path / "runs")


def _results(out_dir):
    return {
        r["conjecture_id"]: r for r in map(json.loads, (out_dir / "falsification.jsonl").open())
    }


def _inject(run_dir, mutate):
    """Rewrite the run's candidates with `mutate` applied to the first periodic one."""
    path = run_dir / "candidates.jsonl"
    cands = [json.loads(line) for line in path.open()]
    target = next(c for c in cands if c["kind"] == "periodic" and "1,3,4" in c["sequence_id"])
    false = json.loads(json.dumps(target))
    mutate(false)
    false["id"] = "C-injected"
    path.write_text("".join(json.dumps(c) + "\n" for c in [*cands, false]))
    return target


def test_true_candidates_survive(mined, tmp_path):
    out = falsify_run(mined, runs_dir=tmp_path / "runs")
    res = _results(out)
    s134 = [
        r
        for r in res.values()
        if "subtraction_set=1,3,4|raw" in r["sequence_id"] and r["kind"] == "periodic"
    ]
    assert s134 and all(r["status"] == "survived" for r in s134)
    p = s134[0]["per_sequence"][0]
    assert p["new_terms"] == 600 - 59 and p["extension_factor"] > 10


def test_false_candidate_is_refuted_with_counterexample(mined, tmp_path):
    def wrong_period(c):
        c["params"]["period"] = 14
        c["params"]["n0"] = 40  # holds in the window only by coincidence of the true period 7
        c["params"]["delta"] = 1

    _inject(mined, wrong_period)
    res = _results(falsify_run(mined, runs_dir=tmp_path / "runs"))
    r = res["C-injected"]
    assert r["status"] == "refuted"
    ce = r["per_sequence"][0]["counterexample"]
    assert ce["n"] == 54 and ce["observed"] != ce["predicted"]
    assert any(
        "s(n + 7) = s(n)" in x["statement"] for x in r["per_sequence"][0]["reproposals_unfalsified"]
    )


def test_candidate_for_missing_sequence_is_untestable(mined, tmp_path):
    def missing(c):
        c["sequence_id"] = "s/data|grundy~n|subtraction_set=9,9|raw"

    _inject(mined, missing)
    assert (
        _results(falsify_run(mined, runs_dir=tmp_path / "runs"))["C-injected"]["status"]
        == "untestable"
    )


def test_registry_records_and_refuted_is_permanent(mined, tmp_path):
    reg = Registry(tmp_path / "registry" / "events.jsonl")

    def wrong(c):
        c["params"]["delta"] = 1

    _inject(mined, wrong)
    falsify_run(mined, runs_dir=tmp_path / "runs", registry=reg)
    st = reg.state()
    assert st["C-injected"]["status"] == "refuted"
    survived = [e for e in st.values() if e["status"] == "survived"]
    assert survived
    # Re-falsifying (e.g. at another scale) does not resurrect a refuted conjecture,
    # and the mining run is not ingested twice.
    falsify_run(mined, runs_dir=tmp_path / "runs", registry=reg)
    st2 = reg.state()
    assert st2["C-injected"]["status"] == "refuted"
    assert len(st2["C-injected"]["proposals"]) == 1
    assert len(st2["C-injected"]["history"]) == 2
    # known / proved transitions
    cid = survived[0]["id"]
    reg.append([{"type": "known", "conjecture_id": cid, "source": "test"}])
    assert reg.state()[cid]["status"] == "known"
    reg.append([{"type": "proved", "conjecture_id": cid, "method": "decide"}])
    assert reg.state()[cid]["status"] == "proved"


def test_registry_rejects_bad_events(tmp_path):
    reg = Registry(tmp_path / "e.jsonl")
    with pytest.raises(ValueError):
        reg.append([{"type": "deleted", "conjecture_id": "x"}])
    reg.append([{"type": "known", "conjecture_id": "nope", "source": "s"}])
    with pytest.raises(ValueError, match="unknown conjecture"):
        reg.state()


def test_second_order_survival_and_refutation(tmp_path, monkeypatch):
    """Toy family: y = x mod (g+2), except group g=15 shifts by 1 from x=500 on.
    Window x <= 99 shows period(g) = g+2 and n0(g) = 0 for every g; full data breaks n0."""
    import numpy as np
    import polars as pl

    from overthink.data import families, schema

    def build_toy(params):
        n = params["n"]
        g, x = np.meshgrid(np.arange(26), np.arange(n), indexing="ij")
        y = x % (g + 2) + ((g == 15) & (x >= 500))
        return pl.DataFrame({"g": g.ravel(), "x": x.ravel(), "y": y.ravel()})

    toy = schema.FamilySchema(
        family="toy",
        title="toy",
        rules="",
        contents="",
        columns=tuple(schema.Column(c, pl.UInt32(), c) for c in ("g", "x", "y")),
        sort_by=("g", "x"),
        sample_filter=pl.col("x") < 5,
        sample_description="",
    )
    monkeypatch.setitem(schema.SCHEMAS, "toy", toy)
    monkeypatch.setitem(families.BUILDERS, "toy", build_toy)
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "toy.yaml"
    cfg.write_text(json.dumps({"dataset": "toy", "family": "toy", "params": {"n": 1000}}))
    generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    run_cfg = {
        "run_name": "toy",
        "datasets": [{"id": "toy", "proposal_window": {"x": 99}}],
        "views": {"min_length": 30, "max_group_value": 30},
        "miners": {},
        "second_order": {
            "enabled": True,
            "min_length": 12,
            "miners": {
                "periodic": {"min_support": 8},
                "polynomial": {"min_support": 8},
                "recurrence": {"min_support": 8},
                "floor_linear": {"min_points": 12},
            },
        },
    }
    (tmp_path / "run.yaml").write_text(yaml.safe_dump(run_cfg))
    run_dir = run_mining(tmp_path / "run.yaml", runs_dir=tmp_path / "runs")
    res = _results(falsify_run(run_dir, runs_dir=tmp_path / "runs"))
    so = {r["sequence_id"].split("|")[3]: r for r in res.values() if r["second_order"]}
    assert so["period over g"]["status"] == "survived"
    assert so["period over g"]["statement"] == "s(n + 1) = s(n) + 1 for all n >= 0"
    # n0(g) = 0 and delta(g) = 0 coincide in the window, so they are one candidate whose
    # scope covers both; it is refuted because n0 breaks at g = 15 at full scale.
    zero = next(
        r
        for r in res.values()
        if r["second_order"] and any("|n0 over g|" in p["sequence_id"] for p in r["per_sequence"])
    )
    assert zero["status"] == "refuted"
    by_seq = {p["sequence_id"].split("|")[3]: p for p in zero["per_sequence"]}
    assert by_seq["n0 over g"]["counterexample"]["n"] == 15
    assert by_seq["delta over g"]["status"] == "holds"
    first = [r for r in res.values() if not r["second_order"] and "g=15|raw" in r["sequence_id"]]
    assert first and all(r["status"] == "refuted" for r in first)


def test_falsify_against_larger_dataset(mined, tmp_path):
    cfg = tmp_path / "s_big.yaml"
    cfg.write_text(
        json.dumps(
            {
                "dataset": "s_big",
                "family": "subtraction",
                "params": {"sets": [[1, 3, 4], [2, 5, 7]], "n_max": 1800},
            }
        )
    )
    generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    out = falsify_run(mined, runs_dir=tmp_path / "runs", dataset_map={"s": "s_big"})
    info = json.loads((out / "falsify.json").read_text())
    assert info["datasets"][0]["falsified_against"] == "s_big"
    assert info["datasets"][0]["scale_factor"] == {"n": round(1800 / 59, 2)}
    res = _results(out)
    p = next(r for r in res.values() if "subtraction_set=1,3,4|raw" in r["sequence_id"])
    assert p["status"] == "survived" and p["per_sequence"][0]["full_range"][1] == 1800


def test_registry_export_statuses(mined, tmp_path):
    from overthink.registry.export import rows

    reg = Registry(tmp_path / "registry" / "events.jsonl")

    def wrong(c):
        c["params"]["delta"] = 1

    _inject(mined, wrong)
    falsify_run(mined, runs_dir=tmp_path / "runs", registry=reg)
    out = {r["id"]: r for r in rows(reg, meta_dir=tmp_path / "datasets")}
    assert out["C-injected"]["proof_status"] == "refuted"
    assert json.loads(out["C-injected"]["counterexamples"])
    assert {r["proof_status"] for r in out.values()} <= {"refuted", "verified-finite"}
    assert all(r["game_family"] == "subtraction" for r in out.values())
