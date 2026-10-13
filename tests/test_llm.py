"""LLM proposer: packet, providers, ingestion and falsification of claims."""

import json

import pytest
import yaml

from overthink.conjecture.llm import MockProvider, Packet, SessionProvider, build_packet, ingest
from overthink.data.store import generate
from overthink.falsify.falsifier import falsify_run


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "w.yaml"
    cfg.write_text(
        json.dumps(
            {
                "dataset": "w",
                "family": "wythoff_subtraction",
                "params": {"sets": [[1], [1, 2]], "n": 200},
            }
        )
    )
    generate(cfg, out_dir=tmp_path / "data_out", meta_dir=tmp_path / "datasets")
    run_cfg = {
        "run_name": "t",
        "datasets": [{"id": "w", "proposal_window": {"x": 19, "y": 19}}],
        "views": {"min_length": 10},
        "miners": {},
    }
    path = tmp_path / "run.yaml"
    path.write_text(yaml.safe_dump(run_cfg))
    return path


def test_packet_only_contains_window(setup, tmp_path):
    pk = build_packet(
        setup, None, tmp_path / "data_out", tmp_path / "datasets", grid=16, grundy_cells=8
    )
    assert "subtraction_set = 1,2" in pk.text and "## Claim language" in pk.text
    assert "x, y < 16" in pk.text and len(pk.sha256) == 64


def test_mock_proposals_falsified(setup, tmp_path):
    pk = build_packet(setup, None, tmp_path / "data_out", tmp_path / "datasets", grid=16)
    run_dir = ingest(
        pk, tmp_path / "p.md", MockProvider(), setup, tmp_path / "runs", tmp_path / "data_out"
    )
    info = json.loads((run_dir / "run.json").read_text())
    assert info["proposer"]["model"] == "mock-0" and info["counts"]["accepted"] == 2
    out = falsify_run(run_dir, runs_dir=tmp_path / "runs")
    res = {r["statement"]: r for r in map(json.loads, (out / "falsification.jsonl").open())}
    assert res["Grundy values are non-negative."]["status"] == "survived"
    naive = res["The only P-positions lie on the diagonal."]
    assert naive["status"] == "refuted"
    assert naive["per_sequence"][0]["reason"] == "false already on the proposal-window data"


def test_session_provider_requires_matching_packet(setup, tmp_path):
    pk = Packet("hello", {})
    doc = {"model": "some-model", "packet_sha256": "0" * 64, "proposals": []}
    (tmp_path / "s.json").write_text(json.dumps(doc))
    with pytest.raises(ValueError, match="SHA-256"):
        SessionProvider(tmp_path / "s.json").propose(pk)


def test_invalid_claims_are_rejected_not_run(setup, tmp_path):
    pk = Packet("x", {})
    doc = {
        "model": "m",
        "packet_sha256": pk.sha256,
        "proposals": [
            {
                "id": "bad",
                "statement": "s",
                "claim": {"kind": "predicate", "table": "data", "assert": "__import__('os')"},
            },
            {
                "id": "ok",
                "statement": "P-positions have x, y even for S={1}",
                "claim": {
                    "kind": "predicate",
                    "table": "P",
                    "group": {"subtraction_set": "1"},
                    "assert": "x % 2 == 0 and y % 2 == 0",
                },
            },
        ],
    }
    (tmp_path / "s.json").write_text(json.dumps(doc))
    run_dir = ingest(
        pk,
        tmp_path / "p",
        SessionProvider(tmp_path / "s.json"),
        setup,
        tmp_path / "runs",
        tmp_path / "data_out",
    )
    info = json.loads((run_dir / "run.json").read_text())
    assert info["counts"] == {"proposals": 2, "accepted": 1, "rejected": 1}
    out = falsify_run(run_dir, runs_dir=tmp_path / "runs")
    (r,) = [json.loads(line) for line in (out / "falsification.jsonl").open()]
    assert r["status"] == "survived"
