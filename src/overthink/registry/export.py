# SPDX-License-Identifier: MIT
"""Export the conjecture registry as an open dataset, one row per conjecture.

Proof status vocabulary:
  open             proposed, or untestable at the falsification scale
  refuted          a counterexample was found (kept: failures are data)
  verified-finite  survived falsification on a finite range (evidence, not proof)
  proved-lean      a Lean proof compiles (file and theorem names given)
`literature` gives the source when the statement matches published work.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import polars as pl
import yaml

from overthink.registry.store import Registry

LEAN_FILES = {
    "OverthinkLean.Chomp": "lean/OverthinkLean/Chomp.lean",
    "OverthinkLean.WythoffSubtraction": "lean/OverthinkLean/WythoffSubtraction.lean",
    "OverthinkLean.Generated.SubtractionPeriodicity": "lean/OverthinkLean/Generated/SubtractionPeriodicity.lean",
}
STATUS = {
    "proved": "proved-lean",
    "refuted": "refuted",
    "survived": "verified-finite",
    "untestable": "open",
    "proposed": "open",
}


def _manifests(meta_dir: Path) -> dict[str, dict]:
    out = {}
    for m in meta_dir.glob("*/manifest.json"):
        d = json.loads(m.read_text())
        out[d["dataset"]] = d
    return out


def _window(config_path: str | None, dataset: str | None) -> dict | None:
    if not config_path or not Path(config_path).exists():
        return None
    cfg = yaml.safe_load(Path(config_path).read_text())
    for ds in cfg.get("datasets", []):
        if ds.get("id") == dataset:
            return ds.get("proposal_window")
    return None


def _proposer(method: str) -> tuple[str, str]:
    if method.startswith("llm:"):
        # model identifiers are kept in registry/events.jsonl; the export uses neutral labels
        return "llm", f"{method.split(':')[1]} provider (interactive AI assistant)"
    return "classical", method


def rows(registry: Registry, meta_dir: Path = Path("datasets")) -> list[dict[str, Any]]:
    manifests = _manifests(meta_dir)
    by_hash = {m["content_sha256"]: k for k, m in manifests.items()}
    out = []
    for cid, e in sorted(registry.state().items()):
        c = e["conjecture"]
        ds = c.get("sequence_meta", {}).get("dataset")
        prov = e["proposals"][0]
        fals = [h for h in e["history"] if h.get("type") == "falsification"]
        proved = [h for h in e["history"] if h.get("type") == "proved"]
        known = [h for h in e["history"] if h.get("type") == "known"]
        status = (
            STATUS[e["status"]]
            if e["status"] != "known"
            else ("verified-finite" if any(f["status"] == "survived" for f in fals) else "open")
        )
        counterexamples, checks, tested_on = [], 0, set()
        for f in fals:
            tested_on |= {by_hash.get(h, h) for h in f.get("datasets", [])}
            for p in f.get("per_sequence", []):
                checks += int(p.get("n_checked") or 0)
                if p.get("counterexample"):
                    counterexamples.append(
                        {"sequence_id": p.get("sequence_id"), **p["counterexample"]}
                    )
        proposer, model = _proposer(c["method"])
        lean_modules = sorted({h.get("lean_module") for h in proved if h.get("lean_module")})
        out.append(
            {
                "id": cid,
                "statement": c["statement"],
                "statement_machine": json.dumps(
                    {"kind": c["kind"], "sequence_id": c["sequence_id"], "params": c["params"]},
                    sort_keys=True,
                    default=str,
                ),
                "game_family": manifests.get(ds, {}).get("family"),
                "dataset": ds,
                "proposal_window": json.dumps(_window(prov.get("config_path"), ds)),
                "proposer": proposer,
                "method": model,
                "falsification_datasets": json.dumps(sorted(tested_on)),
                "falsification_checks": checks,
                "counterexamples": json.dumps(counterexamples, default=str),
                "proof_status": status,
                "lean_files": json.dumps([LEAN_FILES.get(m, m) for m in lean_modules]),
                "lean_theorems": json.dumps(
                    sorted({t for h in proved for t in h.get("lean_theorems", [])})
                ),
                "literature": json.dumps([h.get("source") for h in known]),
                "proposed_at": prov.get("recorded_at") or e["history"][0].get("recorded_at")
                if e["history"]
                else None,
                "last_event_at": e["history"][-1]["recorded_at"] if e["history"] else None,
                "proposal_run": prov.get("run_id"),
            }
        )
    return out


def export(registry: Registry, out_dir: Path) -> dict[str, int]:
    data = rows(registry)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pl.DataFrame(data)
    df.write_parquet(out_dir / "conjectures.parquet", compression="zstd")
    with (out_dir / "conjectures.jsonl").open("w") as f:
        for r in data:
            f.write(json.dumps(r, default=str) + "\n")
    counts = df.group_by("proof_status").len().sort("proof_status")
    return dict(zip(counts["proof_status"].to_list(), counts["len"].to_list(), strict=True))
