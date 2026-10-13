"""Views (dataset -> sequences) and the end-to-end mining run."""

import json

import polars as pl
import yaml

from overthink.conjecture.types import Candidate
from overthink.conjecture.views import (
    build_views,
    enumeration_views,
    functional_targets,
    grouped_views,
    second_order_views,
)
from overthink.data.store import generate


def test_functional_targets():
    # (g, y) pairs are all distinct, so x is determined by them too.
    df = pl.DataFrame({"g": [0, 0, 1, 1], "x": [0, 1, 0, 1], "y": [5, 6, 5, 7]})
    assert functional_targets(df) == ["x", "y"]
    # Here y repeats within g=0, so x is not determined; y is.
    df2 = pl.DataFrame({"g": [0, 0, 0], "x": [0, 1, 2], "y": [5, 5, 6]})
    assert functional_targets(df2) == ["y"]


def test_grouped_views_cut_at_gaps_and_filter_groups():
    rows = [(g, x, 10 * g + x) for g in range(3) for x in list(range(40)) + [45, 46]]
    df = pl.DataFrame(rows, schema=["g", "x", "y"], orient="row")
    seqs = grouped_views(
        df, "ds", "data", {"max_group_value": 1, "min_length": 30, "transforms": ["raw"]}
    )
    ys = {s.id: s for s in seqs if s.meta["target"] == "y" and s.meta["index"] == "x"}
    assert set(ys) == {"ds/data|y~x|g=0|raw", "ds/data|y~x|g=1|raw"}
    s = ys["ds/data|y~x|g=1|raw"]
    assert (s.start, len(s), s.values[:3]) == (0, 40, [10, 11, 12])


def test_enumeration_view_uses_symmetric_half():
    pairs = [(0, 0)] + [(k, 2 * k) for k in range(1, 40)] + [(2 * k, k) for k in range(1, 40)]
    df = pl.DataFrame(pairs, schema=["x", "y"], orient="row")
    seqs = enumeration_views(df, "ds", "P", {"min_length": 30})
    by_col = {s.meta["column"]: s.values for s in seqs}
    assert by_col["x"] == list(range(40))
    assert by_col["y-x"] == list(range(40))
    assert all(s.meta["symmetric_half"] for s in seqs)


def test_build_views_dedupes_with_aliases():
    df = pl.DataFrame(
        {"x": list(range(40)) * 2, "g": [0] * 40 + [1] * 40, "y": [2 * v for v in range(40)] * 2}
    )
    seqs = build_views(df, "ds", {"min_length": 30, "transforms": ["raw"], "enumeration": False})
    ys = [s for s in seqs if s.meta.get("target") == "y" and s.meta.get("index") == "x"]
    assert len(ys) == 1  # g=0 and g=1 give the same sequence
    assert ys[0].meta["aliases"][0]["meta"]["group"] == {"g": 1}


def test_second_order_views_over_group_column():
    seqs = []
    cands = []
    from overthink.conjecture.types import Sequence

    for c in range(15):
        meta = {
            "dataset": "ds",
            "table": "data",
            "view": "grouped",
            "target": "a",
            "index": "b",
            "group": {"c": c},
            "transform": "raw",
        }
        s = Sequence(f"s{c}", [0] * 40, 0, meta)
        seqs.append(s)
        cands.append(
            Candidate(
                "periodic", s.id, {"period": c + 1, "delta": 0, "n0": 2 * c}, "", {}, "t", meta
            )
        )
    so = second_order_views(cands, seqs, {"min_length": 12})
    by_param = {s.meta["param"]: s.values for s in so}
    assert by_param["period"] == [c + 1 for c in range(15)]
    assert by_param["n0"] == [2 * c for c in range(15)]


def test_mining_run_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for ds, fam, params in [
        ("w", "wythoff", {"n": 120}),
        ("s", "subtraction", {"sets": [[1, 3, 4], [1, 2, 3]], "n_max": 200}),
    ]:
        cfg = tmp_path / f"{ds}.yaml"
        cfg.write_text(json.dumps({"dataset": ds, "family": fam, "params": params}))
        generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    run_cfg = {
        "run_name": "t",
        "datasets": [
            {"id": "w", "proposal_window": {"x": 99, "y": 99}},
            {"id": "s", "proposal_window": {"n": 199}},
        ],
        "views": {"min_length": 30},
        "miners": {},
        "second_order": {"enabled": True},
    }
    (tmp_path / "run.yaml").write_text(yaml.safe_dump(run_cfg))
    from overthink.conjecture.run import run_mining

    run_dir = run_mining(tmp_path / "run.yaml", runs_dir=tmp_path / "runs")
    cands = [json.loads(line) for line in (run_dir / "candidates.jsonl").open()]
    statements = {(c["sequence_id"], c["statement"]) for c in cands}
    assert any("enum:x" in sid and "floor(phi*n" in st for sid, st in statements)
    assert any(
        "subtraction_set=1,3,4|raw" in sid and "s(n + 7) = s(n)" in st for sid, st in statements
    )
    info = json.loads((run_dir / "run.json").read_text())
    assert {d["id"] for d in info["datasets"]} == {"w", "s"}
    assert (run_dir / "summary.md").exists()
