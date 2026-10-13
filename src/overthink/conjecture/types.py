# SPDX-License-Identifier: MIT
"""Core types: integer sequences to mine, and candidate conjectures about them."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Sequence:
    """An integer sequence s(start), s(start+1), ... extracted from a dataset.

    `meta` says where it came from (dataset, view, target/index columns, group, transform)
    so that a falsifier can re-extract the same sequence from larger data.
    """

    id: str
    values: list[int]
    start: int = 0
    meta: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.values)

    @property
    def end(self) -> int:
        """Last index covered (inclusive)."""
        return self.start + len(self.values) - 1


@dataclass
class Candidate:
    """A conjecture proposed by a miner: a statement about all indices n >= n0 of a sequence.

    `params` fully determine the statement, so `overthink.conjecture.checks.check` can
    test it on any (larger) version of the sequence.
    """

    kind: str
    sequence_id: str
    params: dict[str, Any]
    statement: str
    evidence: dict[str, Any]
    method: str
    sequence_meta: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        key = json.dumps([self.kind, self.sequence_id, self.params], sort_keys=True, default=str)
        return "C-" + hashlib.sha256(key.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "sequence_id": self.sequence_id,
            "statement": self.statement,
            "params": self.params,
            "evidence": self.evidence,
            "method": self.method,
            "sequence_meta": self.sequence_meta,
        }
