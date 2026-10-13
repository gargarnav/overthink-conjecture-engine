# SPDX-License-Identifier: MIT
"""`overthink run`: one config runs generate -> mine -> falsify -> compare with a manifest."""

import json

import yaml

from overthink.pipeline import run


def test_run_end_to_end_and_reproduce(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "ds.yaml").write_text(
        yaml.safe_dump({"dataset": "w", "family": "wythoff", "params": {"n": 300}})
    )
    (tmp_path / "mine.yaml").write_text(
        yaml.safe_dump(
            {
                "run_name": "m",
                "datasets": [{"id": "w", "proposal_window": {"x": 29, "y": 29}}],
                "views": {"min_length": 15},
                "miners": {},
            }
        )
    )
    cfg = {
        "name": "t",
        "data_dir": "d",
        "meta_dir": "meta",
        "steps": [{"generate": "ds.yaml"}, {"mine": "mine.yaml"}, {"falsify": {}}],
    }
    (tmp_path / "run.yaml").write_text(yaml.safe_dump(cfg))
    first = run(tmp_path / "run.yaml", runs_dir=tmp_path / "runs")
    m1 = json.loads((first / "manifest.json").read_text())
    assert [s["step"] for s in m1["steps"]] == ["generate", "mine", "falsify"]
    assert m1["random_seeds"] is None and len(m1["config_sha256"]) == 64
    mine_dir = m1["steps"][1]["output"]
    fals_dir = m1["steps"][2]["output"]
    cfg["steps"].append(
        {"compare": {"candidates": mine_dir, "falsification": fals_dir, "datasets": "meta"}}
    )
    (tmp_path / "run2.yaml").write_text(yaml.safe_dump(cfg))
    m2 = json.loads(
        (run(tmp_path / "run2.yaml", runs_dir=tmp_path / "runs") / "manifest.json").read_text()
    )
    assert m2["comparison_pass"] is True
    assert m2["steps"][-1]["result"]["dataset_w_identical"] is True
