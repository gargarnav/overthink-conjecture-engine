"""Append-only conjecture registry.

The registry is a JSONL file of events. Nothing is ever edited or deleted; the current
state of each conjecture comes from replaying its events in order.

Event types
    proposed        a miner (or later the LLM proposer) proposed the conjecture
    falsification   the conjecture was tested on larger data (status survived/refuted/untestable)
    known           matched to the literature/OEIS (with source)
    proved          a Lean proof compiled (with method: general / decide / native_decide)

Status rules (see docs/methodology.md §1)
    * "refuted" is permanent: a stored counterexample is never overridden.
    * "proved" outranks "survived" and "known".
    * Otherwise the latest falsification decides between survived and untestable.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path("registry/events.jsonl")
EVENT_TYPES = ("proposed", "falsification", "known", "proved")


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class Registry:
    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = Path(path)

    def append(self, events: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as f:
            for e in events:
                if e.get("type") not in EVENT_TYPES:
                    raise ValueError(f"unknown event type {e.get('type')!r}")
                if "conjecture_id" not in e:
                    raise ValueError("event without conjecture_id")
                f.write(json.dumps({"recorded_at": _now(), **e}, default=str) + "\n")

    def events(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open() as f:
            return [json.loads(line) for line in f if line.strip()]

    def state(self) -> dict[str, dict[str, Any]]:
        st: dict[str, dict[str, Any]] = {}
        for e in self.events():
            cid = e["conjecture_id"]
            if e["type"] == "proposed":
                entry = st.setdefault(
                    cid,
                    {
                        "id": cid,
                        "conjecture": e["conjecture"],
                        "status": "proposed",
                        "proposals": [],
                        "history": [],
                    },
                )
                entry["proposals"].append(e["provenance"])
                continue
            entry = st.get(cid)
            if entry is None:
                raise ValueError(f"{e['type']} event for unknown conjecture {cid}")
            entry["history"].append(e)
            if entry["status"] == "refuted":
                continue
            if e["type"] == "falsification":
                if entry["status"] != "proved":
                    entry["status"] = e["status"]
            elif e["type"] == "proved":
                entry["status"] = "proved"
            elif e["type"] == "known" and entry["status"] != "proved":
                entry["status"] = "known"
        return st

    def ingest_run(self, run_dir: Path) -> int:
        """Record a 'proposed' event for every candidate of a mining run."""
        run_dir = Path(run_dir)
        info = json.loads((run_dir / "run.json").read_text())
        ds_hash = {d["id"]: d["content_sha256"] for d in info["datasets"]}
        events = []
        with (run_dir / "candidates.jsonl").open() as f:
            for line in f:
                c = json.loads(line)
                ds = c["sequence_meta"].get("dataset")
                events.append(
                    {
                        "type": "proposed",
                        "conjecture_id": c["id"],
                        "conjecture": c,
                        "provenance": {
                            "run_id": info["run_id"],
                            "config_path": info["config_path"],
                            "dataset": ds,
                            "dataset_content_sha256": ds_hash.get(ds),
                            "method": c["method"],
                            "model": None,
                            "random_seed": info.get("random_seed"),
                            "git_sha": info["provenance"]["git_sha"],
                            "git_dirty": info["provenance"]["git_dirty"],
                        },
                    }
                )
        self.append(events)
        return len(events)
