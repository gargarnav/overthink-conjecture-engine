"""A mining run: datasets -> views -> classical miners -> candidates, with provenance.

Output directory `<runs_dir>/<run_name>-<UTC timestamp>/`:
    run.json           config, provenance, dataset hashes, counts, timings
    sequences.jsonl    every mined sequence (id, start, values, meta)
    candidates.jsonl   every candidate conjecture
    summary.md         human-readable overview
"""

from __future__ import annotations

import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
import yaml

from overthink.conjecture.dependencies import mine_tables
from overthink.conjecture.mine import mine_sequence
from overthink.conjecture.oeis import OEISSnapshot
from overthink.conjecture.types import Candidate, Sequence
from overthink.conjecture.views import build_views, dataset_tables, second_order_views
from overthink.data.store import load, provenance


def new_run_dir(runs_dir: Path, name: str) -> tuple[Path, str]:
    """Create `<runs_dir>/<name>-<UTC timestamp>[-k]`, never reusing an existing directory."""
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    base = Path(runs_dir) / f"{name}-{stamp}"
    path, k = base, 1
    while True:
        try:
            path.mkdir(parents=True, exist_ok=False)
            return path, stamp
        except FileExistsError:
            k += 1
            path = base.with_name(f"{base.name}-{k}")


def apply_window(df: pl.DataFrame, window: dict[str, int] | None) -> pl.DataFrame:
    for col, mx in (window or {}).items():
        df = df.filter(pl.col(col) <= mx)
    return df


def run_mining(
    config_path: Path,
    runs_dir: Path,
    data_dir: Path = Path("data_out"),
    meta_dir: Path = Path("datasets"),
) -> Path:
    cfg = yaml.safe_load(Path(config_path).read_text())
    run_dir, stamp = new_run_dir(runs_dir, cfg["run_name"])

    miner_cfg = cfg.get("miners", {})
    snap_path = miner_cfg.get("oeis", {}).get("snapshot")
    snapshot = OEISSnapshot(Path(snap_path)) if snap_path else None
    so_cfg = cfg.get("second_order", {})

    all_seqs: list[Sequence] = []
    all_cands: list[Candidate] = []
    datasets_info = []
    t_start = time.perf_counter()
    for ds in cfg["datasets"]:
        t0 = time.perf_counter()
        manifest_path = meta_dir / ds["id"] / "manifest.json"
        df = load(data_dir / ds["id"], manifest_path=manifest_path)
        manifest = json.loads(manifest_path.read_text())
        df = apply_window(df, ds.get("proposal_window"))
        seqs = build_views(df, ds["id"], cfg.get("views", {}))
        cands = [c for s in seqs for c in mine_sequence(s, miner_cfg, snapshot)]
        if miner_cfg.get("functional_dependencies", {}).get("enabled", False):
            cands += mine_tables(dataset_tables(df, cfg.get("views", {})), ds["id"])
        so_seqs: list[Sequence] = []
        if so_cfg.get("enabled", False):
            so_seqs = second_order_views(cands, seqs, so_cfg)
            so_miner_cfg = so_cfg.get("miners", miner_cfg)
            cands += [c for s in so_seqs for c in mine_sequence(s, so_miner_cfg, snapshot)]
        all_seqs += seqs + so_seqs
        all_cands += cands
        datasets_info.append(
            {
                "id": ds["id"],
                "content_sha256": manifest["content_sha256"],
                "proposal_window": ds.get("proposal_window"),
                "rows_in_window": df.height,
                "sequences": len(seqs),
                "second_order_sequences": len(so_seqs),
                "candidates": len(cands),
                "seconds": round(time.perf_counter() - t0, 2),
            }
        )

    with (run_dir / "sequences.jsonl").open("w") as f:
        for s in all_seqs:
            f.write(
                json.dumps(
                    {"id": s.id, "start": s.start, "values": s.values, "meta": s.meta}, default=str
                )
                + "\n"
            )
    with (run_dir / "candidates.jsonl").open("w") as f:
        for c in all_cands:
            f.write(json.dumps(c.to_dict(), default=str) + "\n")
    run_info: dict[str, Any] = {
        "run_id": run_dir.name,
        "config_path": str(config_path),
        "config": cfg,
        "started_at": stamp,
        "seconds": round(time.perf_counter() - t_start, 2),
        "datasets": datasets_info,
        "counts_by_kind": dict(Counter(c.kind for c in all_cands)),
        "oeis_snapshot": None
        if snapshot is None
        else {"path": str(snapshot.path), "entries": snapshot.n_entries},
        "random_seed": None,
        "provenance": provenance(),
    }
    (run_dir / "run.json").write_text(json.dumps(run_info, indent=2, default=str) + "\n")
    (run_dir / "summary.md").write_text(render_summary(run_info, all_cands))
    return run_dir


def render_summary(info: dict[str, Any], cands: list[Candidate]) -> str:
    lines = [
        f"# Mining run `{info['run_id']}`",
        "",
        (
            f"Config: `{info['config_path']}` · git `{info['provenance']['git_sha']}`"
            f"{' (dirty)' if info['provenance']['git_dirty'] else ''} · "
            f"{info['seconds']} s"
        ),
        "",
        "| Dataset | Window | Rows | Sequences | 2nd-order | Candidates |",
        "|---|---|---|---|---|---|",
    ]
    for d in info["datasets"]:
        lines.append(
            f"| `{d['id']}` | `{d['proposal_window']}` | {d['rows_in_window']:,} | "
            f"{d['sequences']} | {d['second_order_sequences']} | {d['candidates']} |"
        )
    lines += [
        "",
        "Candidates by kind: "
        + ", ".join(f"{k} {v}" for k, v in sorted(info["counts_by_kind"].items())),
        "",
        "All candidates are **unverified proposals** until the falsifier has tested them.",
        "",
    ]
    by_ds: dict[str, list[Candidate]] = {}
    for c in cands:
        by_ds.setdefault(c.sequence_meta.get("dataset", "?"), []).append(c)
    for ds, cs in by_ds.items():
        lines += [f"## {ds}", "", "| Sequence | Kind | Statement | Support |", "|---|---|---|---|"]
        for c in cs:
            st = c.statement.replace("|", "\\|")
            lines.append(
                f"| `{c.sequence_id}` | {c.kind} | {st} | {c.evidence.get('support', '')} |"
            )
        lines.append("")
    return "\n".join(lines)
