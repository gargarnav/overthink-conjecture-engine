# SPDX-License-Identifier: MIT
"""Check (or with --fix, add) SPDX license headers on every tracked source file.

Exempt, and kept byte-identical on purpose:
- reference/: the author's original research code, whose SHA-256 hashes are recorded;
- experiments/familyH/write_proposals.py: the exact script that produced committed
  LLM proposals (a pre-registered experiment artifact).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HEADERS = {
    ".py": "# SPDX-License-Identifier: MIT",
    ".rs": "// SPDX-License-Identifier: MIT",
    ".lean": "-- SPDX-License-Identifier: MIT",
}
EXEMPT_PREFIXES = ("reference/",)
EXEMPT_FILES = {"experiments/familyH/write_proposals.py"}


def tracked_sources() -> list[Path]:
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    files = []
    for f in out.splitlines():
        p = Path(f)
        if p.suffix in HEADERS and not f.startswith(EXEMPT_PREFIXES) and f not in EXEMPT_FILES:
            files.append(p)
    return files


def has_header(p: Path) -> bool:
    head = p.read_text().splitlines()[:3]
    return any("SPDX-License-Identifier: MIT" in line for line in head)


def add_header(p: Path) -> None:
    text = p.read_text()
    header = HEADERS[p.suffix] + "\n"
    if text.startswith("#!"):
        first, _, rest = text.partition("\n")
        p.write_text(first + "\n" + header + rest)
    else:
        p.write_text(header + text)


def main() -> int:
    fix = "--fix" in sys.argv
    missing = [p for p in tracked_sources() if not has_header(p)]
    for p in missing:
        if fix:
            add_header(p)
        print(("added header: " if fix else "missing SPDX header: ") + str(p))
    return 0 if fix or not missing else 1


if __name__ == "__main__":
    sys.exit(main())
