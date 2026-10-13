"""Falsify a mining run: re-test every candidate on the full (larger) dataset.

For each dataset of the run, the same views (same config) are rebuilt on the full data
without the proposal window. Every candidate is then checked on each sequence it applies
to: the sequence it was mined from, plus any sequences that were identical to it in the
proposal window (its aliases), which may differ at larger scale.

Per candidate:
    refuted     some sequence violates it (counterexamples stored)
    survived    it holds on every sequence it applies to (first-order: each must have new
                terms at full scale)
    untestable  otherwise (sequence missing at full scale, or no new terms)

Second-order candidates are tested by re-running the frozen first-order miners on the full
data, rebuilding the second-order sequences from those parameters, and checking.

For each refuted first-order candidate, the miners also re-propose on the full sequence.
Those re-proposals are new, unfalsified conjectures and are labelled as such.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

from overthink.conjecture.checks import check
from overthink.conjecture.mine import mine_sequence
from overthink.conjecture.run import new_run_dir
from overthink.conjecture.types import Candidate, Sequence
from overthink.conjecture.views import build_views, second_order_views
from overthink.data.store import load, provenance
from overthink.registry.store import Registry


def _index(seqs: list[Sequence]) -> dict[str, Sequence]:
    idx = {}
    for s in seqs:
        idx[s.id] = s
        for a in s.meta.get("aliases", []):
            idx[a["id"]] = Sequence(a["id"], s.values, s.start, a["meta"])
    return idx


def _consistent(prop: Sequence, full: Sequence) -> bool:
    """The full sequence must agree with the proposal sequence where both are defined."""
    lo, hi = max(prop.start, full.start), min(prop.end, full.end)
    return all(
        prop.values[n - prop.start] == full.values[n - full.start] for n in range(lo, hi + 1)
    )


def _test(
    cand: dict,
    scope: list[str],
    prop_idx: dict,
    full_idx: dict,
    miner_cfg: dict,
    second_order: bool,
) -> dict[str, Any]:
    per_seq = []
    for sid in scope:
        prop, full = prop_idx.get(sid), full_idx.get(sid)
        if full is None:
            per_seq.append(
                {
                    "sequence_id": sid,
                    "status": "untestable",
                    "reason": "sequence not present at full scale",
                }
            )
            continue
        # Second-order values are re-estimated at full scale, so they may legitimately
        # differ from the proposal values; that difference is what is being tested.
        if prop is not None and not second_order and not _consistent(prop, full):
            per_seq.append(
                {
                    "sequence_id": sid,
                    "status": "untestable",
                    "reason": "extraction mismatch between proposal and full data",
                }
            )
            continue
        res = check(cand["kind"], cand["params"], full)
        prop_len = len(prop) if prop is not None else None
        res.update(
            {
                "sequence_id": sid,
                "proposal_range": [prop.start, prop.end] if prop is not None else None,
                "full_range": [full.start, full.end],
                "new_terms": full.end - prop.end if prop is not None else None,
                "extension_factor": round(len(full) / prop_len, 2) if prop_len else None,
            }
        )
        if second_order and prop is not None:
            # The evidence here is re-estimation from 10x more first-order data, not more groups.
            res["parameters_changed_at_full_scale"] = [
                n
                for n in range(max(prop.start, full.start), min(prop.end, full.end) + 1)
                if prop.values[n - prop.start] != full.values[n - full.start]
            ]
        elif res["status"] == "holds" and prop is not None and full.end <= prop.end:
            res["status"], res["reason"] = "untestable", "no new terms at full scale"
        if res["status"] == "violated" and not second_order:
            res["reproposals_unfalsified"] = [
                {"kind": c.kind, "statement": c.statement, "params": c.params}
                for c in mine_sequence(full, miner_cfg)
            ]
        per_seq.append(res)
    statuses = [r["status"] for r in per_seq]
    if "violated" in statuses:
        status = "refuted"
    elif statuses and all(s == "holds" for s in statuses):
        status = "survived"
    else:
        status = "untestable"
    return {"status": status, "per_sequence": per_seq}


def falsify_run(
    run_dir: Path,
    runs_dir: Path,
    data_dir: Path = Path("data_out"),
    meta_dir: Path = Path("datasets"),
    registry: Registry | None = None,
) -> Path:
    run_dir = Path(run_dir)
    info = json.loads((run_dir / "run.json").read_text())
    cfg = info["config"]
    miner_cfg = cfg.get("miners", {})
    so_cfg = cfg.get("second_order", {})
    cands = [json.loads(line) for line in (run_dir / "candidates.jsonl").open()]
    prop_seqs = [
        Sequence(d["id"], d["values"], d["start"], d["meta"])
        for d in map(json.loads, (run_dir / "sequences.jsonl").open())
    ]
    prop_idx = _index(prop_seqs)

    out_dir, _ = new_run_dir(runs_dir, f"falsify-{info['run_id']}")
    t_start = time.perf_counter()
    results, ds_info = [], []
    for ds in cfg["datasets"]:
        t0 = time.perf_counter()
        manifest_path = meta_dir / ds["id"] / "manifest.json"
        full = load(data_dir / ds["id"], manifest_path=manifest_path)
        manifest = json.loads(manifest_path.read_text())
        window = ds.get("proposal_window") or {}
        scale = {c: round(full[c].max() / mx, 2) if mx else None for c, mx in window.items()}
        full_seqs = build_views(full, ds["id"], cfg.get("views", {}))
        full_idx = _index(full_seqs)
        ds_cands = [c for c in cands if c["sequence_meta"].get("dataset") == ds["id"]]
        so_cands = [c for c in ds_cands if c["sequence_meta"].get("view") == "second_order"]
        full_so_idx: dict[str, Sequence] = {}
        if so_cands:
            full_first: list[Candidate] = [
                x for s in full_seqs for x in mine_sequence(s, miner_cfg)
            ]
            full_so_idx = _index(second_order_views(full_first, full_seqs, so_cfg))
        for c in ds_cands:
            is_so = c["sequence_meta"].get("view") == "second_order"
            prop = prop_idx.get(c["sequence_id"])
            scope = [c["sequence_id"]] + [
                a["id"] for a in (prop.meta.get("aliases", []) if prop else [])
            ]
            res = _test(
                c,
                scope,
                prop_idx,
                full_so_idx if is_so else full_idx,
                so_cfg.get("miners", miner_cfg) if is_so else miner_cfg,
                second_order=is_so,
            )
            results.append(
                {
                    "conjecture_id": c["id"],
                    "kind": c["kind"],
                    "sequence_id": c["sequence_id"],
                    "statement": c["statement"],
                    "second_order": is_so,
                    **res,
                }
            )
        ds_info.append(
            {
                "id": ds["id"],
                "content_sha256": manifest["content_sha256"],
                "full_rows": full.height,
                "proposal_window": window,
                "scale_factor": scale,
                "full_sequences": len(full_seqs),
                "candidates": len(ds_cands),
                "seconds": round(time.perf_counter() - t0, 2),
            }
        )

    with (out_dir / "falsification.jsonl").open("w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    summary = {
        "falsify_run_id": out_dir.name,
        "mining_run_id": info["run_id"],
        "seconds": round(time.perf_counter() - t_start, 2),
        "datasets": ds_info,
        "counts": dict(Counter(r["status"] for r in results)),
        "counts_by_kind": {
            k: dict(Counter(r["status"] for r in results if r["kind"] == k))
            for k in sorted({r["kind"] for r in results})
        },
        "rule": "refuted if violated on any sequence in scope; survived if it holds on all "
        "and at least one has new terms; otherwise untestable",
        "provenance": provenance(),
    }
    (out_dir / "falsify.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    (out_dir / "summary.md").write_text(render_summary(summary, results))

    if registry is not None:
        ingested_runs = {p["run_id"] for e in registry.state().values() for p in e["proposals"]}
        if info["run_id"] not in ingested_runs:
            registry.ingest_run(run_dir)
        registry.append(
            [
                {
                    "type": "falsification",
                    "conjecture_id": r["conjecture_id"],
                    "status": r["status"],
                    "falsify_run_id": out_dir.name,
                    "datasets": [d["content_sha256"] for d in ds_info],
                    "per_sequence": r["per_sequence"],
                }
                for r in results
            ]
        )
    return out_dir


def render_summary(s: dict[str, Any], results: list[dict]) -> str:
    lines = [
        f"# Falsification `{s['falsify_run_id']}`",
        "",
        f"Mining run: `{s['mining_run_id']}` · {s['seconds']} s",
        "",
        f"Rule: {s['rule']}.",
        "",
        "| Dataset | Window | Scale factor | Candidates |",
        "|---|---|---|---|",
    ]
    for d in s["datasets"]:
        lines.append(
            f"| `{d['id']}` | `{d['proposal_window']}` | `{d['scale_factor']}` | "
            f"{d['candidates']} |"
        )
    lines += ["", f"Overall: {s['counts']}", "", "| Kind | Status counts |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in s["counts_by_kind"].items()]
    for status in ("refuted", "untestable", "survived"):
        rs = [r for r in results if r["status"] == status]
        if not rs:
            continue
        lines += [
            "",
            f"## {status.capitalize()} ({len(rs)})",
            "",
            "| Sequence | Statement | Detail |",
            "|---|---|---|",
        ]
        for r in rs:
            det = []
            for p in r["per_sequence"]:
                if p.get("counterexample"):
                    ce = p["counterexample"]
                    det.append(
                        f"n={ce['n']}: observed {ce['observed']}, predicted {ce['predicted']}"
                    )
                elif p.get("reason"):
                    det.append(p["reason"])
                elif p.get("extension_factor"):
                    det.append(
                        f"{p['n_checked']} checks, range {p['full_range']} "
                        f"({p['extension_factor']}x)"
                    )
            st = r["statement"].replace("|", "\\|")
            lines.append(f"| `{r['sequence_id']}` | {st} | {'; '.join(det[:2])} |")
    return "\n".join(lines) + "\n"
