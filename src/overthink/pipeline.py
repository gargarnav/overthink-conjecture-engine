# SPDX-License-Identifier: MIT
"""`overthink run CONFIG`: run an experiment end to end from one config file.

Config:
    name: <experiment name>
    data_dir: data_out          # optional
    meta_dir: datasets          # optional (dataset cards/manifests)
    steps:
      - generate: <dataset config path>
      - mine: <mining config path>
      - falsify: {dataset_map: {<run dataset>: <test dataset>}}   # uses the last mining run
      - compare: {candidates: <committed run dir>, falsification: <committed falsify dir>,
                  datasets: <committed manifests dir>}  # regenerated data hashes are checked

Writes `<runs_dir>/<name>-<timestamp>/manifest.json`: git commit and dirty flag, config SHA-256,
seeds (none: every step is deterministic), per-step timestamps and runtimes, outputs, cost
(API spend from any LLM step; compute is wall-clock seconds), and the comparison result.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from overthink.conjecture.run import new_run_dir, run_mining
from overthink.data.store import generate, provenance
from overthink.falsify.falsifier import falsify_run


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _compare(step: dict[str, Any], mine_dir: Path | None, fals_dirs: list[Path]) -> dict:
    """Compare regenerated outputs with committed ones: same candidate ids and statements, and
    the same falsification status for every candidate."""
    out: dict[str, Any] = {}
    for ds, h in (step.get("_generated") or {}).items():
        committed = Path(step.get("datasets", "datasets")) / ds / "manifest.json"
        if committed.exists():
            ok = json.loads(committed.read_text())["content_sha256"] == h
            out[f"dataset_{ds}_identical"] = ok
    if "candidates" in step and mine_dir is not None:

        def key(p: Path) -> set[tuple[str, str]]:
            return {(c["id"], c["statement"]) for c in map(json.loads, p.open())}

        a = key(mine_dir / "candidates.jsonl")
        b = key(Path(step["candidates"]) / "candidates.jsonl")
        out["candidates_identical"] = a == b
        out["candidates"] = len(a)
    if "falsification" in step and fals_dirs:

        def statuses(p: Path) -> dict[str, str]:
            return {r["conjecture_id"]: r["status"] for r in map(json.loads, p.open())}

        sa = statuses(fals_dirs[0] / "falsification.jsonl")
        sb = statuses(Path(step["falsification"]) / "falsification.jsonl")
        out["falsification_identical"] = sa == sb
    out["pass"] = all(v for k, v in out.items() if k.endswith("identical"))
    return out


def run(config_path: Path, runs_dir: Path = Path("experiments/runs")) -> Path:
    raw = Path(config_path).read_bytes()
    cfg = yaml.safe_load(raw)
    data_dir = Path(cfg.get("data_dir", "data_out"))
    meta_dir = Path(cfg.get("meta_dir", "datasets"))
    run_dir, _ = new_run_dir(runs_dir, cfg["name"])
    manifest: dict[str, Any] = {
        "name": cfg["name"],
        "config_path": str(config_path),
        "config_sha256": hashlib.sha256(raw).hexdigest(),
        "random_seeds": None,
        "started_at": _now(),
        "provenance": provenance(),
        "steps": [],
    }
    mine_dir: Path | None = None
    fals_dirs: list[Path] = []
    generated: dict[str, str] = {}
    t_all = time.perf_counter()
    for step in cfg["steps"]:
        ((kind, arg),) = step.items()
        t0, rec = time.perf_counter(), {"step": kind, "started_at": _now()}
        if kind == "generate":
            m = generate(Path(arg), out_dir=data_dir, meta_dir=meta_dir)
            rec.update(
                dataset=m["dataset"], content_sha256=m["content_sha256"], rows=m["row_count"]
            )
            generated[m["dataset"]] = m["content_sha256"]
        elif kind == "mine":
            mine_dir = run_mining(Path(arg), runs_dir=run_dir, data_dir=data_dir, meta_dir=meta_dir)
            rec["output"] = str(mine_dir)
        elif kind == "falsify":
            if mine_dir is None:
                raise ValueError("falsify step needs a preceding mine step")
            d = falsify_run(
                mine_dir,
                runs_dir=run_dir,
                data_dir=data_dir,
                meta_dir=meta_dir,
                dataset_map=(arg or {}).get("dataset_map"),
            )
            fals_dirs.append(d)
            rec["output"] = str(d)
            rec["counts"] = json.loads((d / "falsify.json").read_text())["counts"]
        elif kind == "compare":
            rec["result"] = _compare({**arg, "_generated": generated}, mine_dir, fals_dirs)
            manifest["comparison_pass"] = rec["result"]["pass"]
        else:
            raise ValueError(f"unknown step {kind!r}")
        rec["seconds"] = round(time.perf_counter() - t0, 2)
        manifest["steps"].append(rec)
    manifest["finished_at"] = _now()
    manifest["seconds"] = round(time.perf_counter() - t_all, 2)
    manifest["cost"] = {"api_usd": 0.0, "compute_seconds": manifest["seconds"]}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str) + "\n")
    return run_dir
