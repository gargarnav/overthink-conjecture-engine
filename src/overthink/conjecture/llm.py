"""LLM proposer: provider-agnostic interface, data packets, and ingestion into a run.

Flow
----
1. `build_packet` renders ONLY the proposal-window data (plus the classical miners' output
   for the same window and the claim language) into a text packet, saved with its SHA-256.
2. A `Provider` reads the packet and returns proposals: natural-language statements, each
   with a machine-checkable claim (`overthink.conjecture.claims`).
3. `ingest` validates the claims and writes a run directory in the same format as a mining
   run, so `overthink falsify` tests the proposals exactly like classical candidates.

Providers
---------
mock       deterministic toy proposals, for tests and dry runs (no model).
session    proposals written by an AI assistant in an interactive session (no API access),
           stored as JSON that names the model and the SHA-256 of the packet it was given.
           The JSON must be committed before falsification.
anthropic  API provider; not configured in this project yet (no API key).

Usage tracking: every run records packet size, approximate input tokens (chars / 4), output
size, and API cost (0 for mock and session).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import polars as pl

from overthink.conjecture.claims import ClaimError, validate
from overthink.conjecture.run import apply_window, new_run_dir
from overthink.conjecture.types import Candidate
from overthink.conjecture.views import dataset_tables
from overthink.data.schema import get_schema
from overthink.data.store import load, provenance

CLAIM_LANGUAGE = (Path(__file__).with_name("claims.py")).read_text().split('"""')[1]


@dataclass
class Packet:
    text: str
    meta: dict[str, Any]

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode()).hexdigest()


def _grid(df: pl.DataFrame, n: int) -> list[str]:
    """P-pattern of a Grundy table: row x, column y; '#' = P-position, '.' = N-position."""
    g = df.filter((pl.col("x") < n) & (pl.col("y") < n)).sort("x", "y")
    vals = g["grundy"].to_numpy().reshape(n, n)
    return ["".join("#" if v == 0 else "." for v in row) for row in vals]


def build_packet(
    config_path: Path,
    mining_run_dir: Path | None,
    data_dir: Path,
    meta_dir: Path,
    grid: int = 48,
    grundy_cells: int = 12,
) -> Packet:
    """Render the proposal-window data of each 2D Grundy dataset in a mining config."""
    import yaml

    cfg = yaml.safe_load(Path(config_path).read_text())
    parts = [
        "# Data packet for an AI conjecture proposer",
        "",
        (
            "You are given exact data from the PROPOSAL WINDOW only. Propose conjectures that you "
            "expect to hold far beyond it (they will be tested on 10x larger data you have not "
            "seen). Each proposal needs a natural-language statement, a one-line rationale, and "
            "a machine-checkable claim in the language below. Prefer statements the classical "
            "miners (listed at the end) cannot express: characterizations of the P-positions, "
            "periodicity along any direction, region structure, densities."
        ),
        "",
        "## Claim language",
        CLAIM_LANGUAGE.strip(),
        "",
    ]
    for ds in cfg["datasets"]:
        manifest = json.loads((meta_dir / ds["id"] / "manifest.json").read_text())
        schema = get_schema(manifest["family"])
        df = apply_window(load(data_dir / ds["id"]), ds.get("proposal_window"))
        if not {"x", "y", "grundy"} <= set(df.columns):
            raise ValueError(f"{ds['id']}: packet builder expects x, y, grundy columns")
        group_cols = [c for c in df.columns if c not in ("x", "y", "grundy")]
        parts += [
            f"## Dataset `{ds['id']}`",
            "",
            f"Game: {schema.rules}",
            (
                f"Proposal window: {ds.get('proposal_window')}. Tables: `data` (columns "
                f"{df.columns}) and `P` (the rows of `data` with grundy == 0, without grundy)."
            ),
            "",
        ]
        groups = df.select(group_cols).unique().sort(group_cols).rows() if group_cols else [()]
        for key in groups:
            sub = df
            for c, v in zip(group_cols, key, strict=True):
                sub = sub.filter(pl.col(c) == v)
            label = ", ".join(f"{c} = {v}" for c, v in zip(group_cols, key, strict=True))
            parts += [
                f"### {label or 'all'}",
                "",
                f"P-pattern for x, y < {grid} (row = x from 0, column = y from 0; # = P-position):",
                "```",
            ]
            parts += _grid(sub, grid)
            g = sub.filter((pl.col("x") < grundy_cells) & (pl.col("y") < grundy_cells))
            g = g.sort("x", "y")["grundy"].to_numpy().reshape(grundy_cells, grundy_cells)
            parts += ["```", f"Grundy values for x, y < {grundy_cells} (row = x):", "```"]
            parts += [" ".join(f"{v:2d}" for v in row) for row in g]
            parts += ["```", ""]
    if mining_run_dir is not None:
        parts += ["## Classical miners' proposals for the same window (for reference)", ""]
        for line in (Path(mining_run_dir) / "candidates.jsonl").open():
            c = json.loads(line)
            parts.append(f"- `{c['sequence_id']}`: {c['statement']}")
    text = "\n".join(parts) + "\n"
    meta = {
        "config_path": str(config_path),
        "mining_run": str(mining_run_dir),
        "grid": grid,
        "grundy_cells": grundy_cells,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    return Packet(text, meta)


class Provider(Protocol):
    name: str
    model: str

    def propose(self, packet: Packet) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...


class MockProvider:
    """Deterministic toy proposals (one true by construction, one usually false)."""

    name, model = "mock", "mock-0"

    def propose(self, packet: Packet):
        props = [
            {
                "id": "mock-1",
                "statement": "Grundy values are non-negative.",
                "rationale": "Trivially true; checks the plumbing.",
                "claim": {"kind": "predicate", "table": "data", "assert": "grundy >= 0"},
            },
            {
                "id": "mock-2",
                "statement": "The only P-positions lie on the diagonal.",
                "rationale": "A deliberately naive guess.",
                "claim": {"kind": "predicate", "table": "P", "assert": "x == y"},
            },
        ]
        return props, {"api_cost_usd": 0.0, "approx_input_tokens": len(packet.text) // 4}


class SessionProvider:
    """Proposals written by an AI assistant in an interactive session, read from JSON."""

    name = "session"

    def __init__(self, path: Path):
        self.path = Path(path)
        self.doc = json.loads(self.path.read_text())
        self.model = self.doc["model"]

    def propose(self, packet: Packet):
        if self.doc["packet_sha256"] != packet.sha256:
            raise ValueError("proposals were written for a different packet (SHA-256 mismatch)")
        out_chars = sum(len(json.dumps(p)) for p in self.doc["proposals"])
        return self.doc["proposals"], {
            "api_cost_usd": 0.0,
            "approx_input_tokens": len(packet.text) // 4,
            "output_chars": out_chars,
            "note": self.doc.get("note", "interactive session; no API call"),
        }


class AnthropicProvider:
    name, model = "anthropic", "unconfigured"

    def propose(self, packet: Packet):
        raise NotImplementedError(
            "No API key is configured for this project. Use the "
            "session provider, or add an API implementation here."
        )


def ingest(
    packet: Packet,
    packet_path: Path,
    provider: Provider,
    config_path: Path,
    runs_dir: Path,
    data_dir: Path = Path("data_out"),
) -> Path:
    """Validate a provider's proposals and write them as a run directory for `falsify`."""
    import yaml

    cfg = yaml.safe_load(Path(config_path).read_text())
    proposals, usage = provider.propose(packet)
    run_dir, stamp = new_run_dir(runs_dir, f"llm-{provider.name}-{cfg['run_name']}")
    cands, rejected = [], []
    for ds in cfg["datasets"]:
        window_tables = dataset_tables(
            apply_window(load(data_dir / ds["id"]), ds.get("proposal_window")), cfg.get("views", {})
        )
        for p in proposals:
            if p.get("dataset", ds["id"]) != ds["id"]:
                continue
            claim = p["claim"]
            try:
                validate(claim, window_tables)
            except ClaimError as e:
                rejected.append({"id": p.get("id"), "reason": str(e), "proposal": p})
                continue
            cid = hashlib.sha256(json.dumps(claim, sort_keys=True).encode()).hexdigest()[:10]
            cands.append(
                Candidate(
                    kind=f"claim_{claim['kind']}",
                    sequence_id=f"{ds['id']}/{claim['table']}|claim:{cid}",
                    params=claim,
                    statement=p["statement"],
                    evidence={"proposal_id": p.get("id"), "rationale": p.get("rationale", "")},
                    method=f"llm:{provider.name}:{provider.model}",
                    sequence_meta={"dataset": ds["id"], "table": claim["table"], "view": "claim"},
                )
            )
    (run_dir / "candidates.jsonl").write_text(
        "".join(json.dumps(c.to_dict(), default=str) + "\n" for c in cands)
    )
    (run_dir / "sequences.jsonl").write_text("")
    (run_dir / "rejected.jsonl").write_text(
        "".join(json.dumps(r, default=str) + "\n" for r in rejected)
    )
    manifests = {
        ds["id"]: json.loads((Path("datasets") / ds["id"] / "manifest.json").read_text())[
            "content_sha256"
        ]
        for ds in cfg["datasets"]
    }
    info = {
        "run_id": run_dir.name,
        "config_path": str(config_path),
        "config": cfg,
        "started_at": stamp,
        "datasets": [{"id": k, "content_sha256": v} for k, v in manifests.items()],
        "proposer": {
            "provider": provider.name,
            "model": provider.model,
            "packet_path": str(packet_path),
            "packet_sha256": packet.sha256,
            "usage": usage,
        },
        "counts": {"proposals": len(proposals), "accepted": len(cands), "rejected": len(rejected)},
        "random_seed": None,
        "provenance": provenance(),
    }
    (run_dir / "run.json").write_text(json.dumps(info, indent=2, default=str) + "\n")
    return run_dir
