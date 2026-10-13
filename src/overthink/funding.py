# SPDX-License-Identifier: MIT
"""Funding status, read from `funding.yaml` at the repository root.

While `funded` is false, `acknowledgment()` returns None and no acknowledgment is rendered
anywhere. Claiming funding that has not been awarded would be false.
"""

from __future__ import annotations

from pathlib import Path

import yaml

FUNDING_FILE = Path(__file__).resolve().parents[2] / "funding.yaml"


def is_funded(path: Path = FUNDING_FILE) -> bool:
    if not path.exists():
        return False
    return bool(yaml.safe_load(path.read_text()).get("funded", False))


def acknowledgment(path: Path = FUNDING_FILE) -> str | None:
    """The acknowledgment text if (and only if) funding has been awarded."""
    if not is_funded(path):
        return None
    return " ".join(yaml.safe_load(path.read_text())["acknowledgment"].split())
