# SPDX-License-Identifier: MIT
"""Match sequences against a local OEIS snapshot (the `stripped` file from oeis.org).

Each line of the snapshot looks like `A000045 ,0,1,1,2,3,5,8,13,`. Matching is exact:
the first `min_terms` observed values must appear as consecutive terms of an OEIS entry,
and every further overlapping term must agree too. Low-information sequences (fewer than
3 distinct values, or arithmetic progressions) are skipped, and matches with more than
`max_hits` entries are dropped as uninformative.
"""

from __future__ import annotations

import gzip
import itertools
from pathlib import Path
from typing import Any

from overthink.conjecture.types import Candidate, Sequence

METHOD = "oeis-exact@1"


class OEISSnapshot:
    def __init__(self, path: Path):
        opener = gzip.open if str(path).endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f if ln.startswith("A")]
        self.path = Path(path)
        self.n_entries = len(lines)
        self.text = "\n".join(lines) + "\n"

    def search(self, values: list[int], min_terms: int) -> list[tuple[str, int, int]]:
        """All (A-number, term offset, number of overlapping terms) with full agreement."""
        needle = "," + ",".join(map(str, values[:min_terms])) + ","
        hits = []
        pos = self.text.find(needle)
        while pos != -1:
            line_start = self.text.rfind("\n", 0, pos) + 1
            line_end = self.text.find("\n", pos)
            line = self.text[line_start:line_end]
            anum, _, body = line.partition(" ")
            terms = [int(x) for x in body.strip(",").split(",") if x]
            offset = self.text.count(",", line_start, pos)
            overlap = terms[offset : offset + len(values)]
            if overlap == values[: len(overlap)]:
                hits.append((anum, offset, len(overlap)))
            pos = self.text.find(needle, pos + 1)
        return hits


def _low_information(values: list[int]) -> bool:
    if len(set(values)) < 3:
        return True
    d = values[1] - values[0]
    return all(b - a == d for a, b in itertools.pairwise(values))


def mine(seq: Sequence, cfg: dict[str, Any], snapshot: OEISSnapshot | None) -> list[Candidate]:
    if snapshot is None:
        return []
    min_terms = cfg.get("min_terms", 12)
    vals = seq.values
    if len(vals) < min_terms or _low_information(vals[:min_terms]):
        return []
    hits = snapshot.search(vals, min_terms)
    if not hits or len(hits) > cfg.get("max_hits", 10):
        return []
    return [
        Candidate(
            kind="oeis_match",
            sequence_id=seq.id,
            params={"anumber": anum, "oeis_offset": off, "n0": seq.start},
            statement=(
                f"s(n) for n >= {seq.start} equals {anum} from its term #{off} on "
                f"(agrees on all {overlap} overlapping terms in the snapshot)"
            ),
            evidence={
                "observed_range": [seq.start, seq.end],
                "overlap_terms": overlap,
                "n_hits": len(hits),
                "snapshot": snapshot.path.name,
                "support": overlap,
            },
            method=METHOD,
            sequence_meta=seq.meta,
        )
        for anum, off, overlap in hits
    ]
