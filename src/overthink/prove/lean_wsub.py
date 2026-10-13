# SPDX-License-Identifier: MIT
"""Record Lean proofs of the LLM's W(S) proposals H01–H04 (family H) in the registry.

`lean/OverthinkLean/WythoffSubtraction.lean` proves, for every position:
H01 (odd S with 1 ∈ S: G = F₁), H02 (1, 2 ∈ S, 3 ∤ s: G = (x + y) % 3), via the scaling
theorem H03 (G_{s} = F₁(⌊x/s⌋, ⌊y/s⌋)) and H04 (G_{2,4} = (⌊x/2⌋ + ⌊y/2⌋) % 3), and H08 (the
P-positions of W({a, a+1}) for every a ≥ 1, `pair_P_positions`).
"""

from __future__ import annotations

import re
import subprocess
from typing import Any

from overthink.prove.lean_subtraction import ALLOWED_AXIOMS, LEAN_DIR
from overthink.registry.store import Registry

THEOREMS = {  # LLM proposal id -> Lean theorem
    "H01": "Overthink.WSub.H01",
    "H02": "Overthink.WSub.H02",
    "H03-2": "Overthink.WSub.H03",
    "H03-3": "Overthink.WSub.H03",
    "H03-4": "Overthink.WSub.H03",
    "H03-5": "Overthink.WSub.H03",
    "H04": "Overthink.WSub.H04",
    "H08-2": "Overthink.WSub.pair_P_positions",
    "H08-3": "Overthink.WSub.pair_P_positions",
    "H08-4": "Overthink.WSub.pair_P_positions",
}
METHOD = "general: grundy_eq_of / grundy_zero_iff_of characterization, kernel-checked"


def run(registry: Registry, record: bool = True) -> dict[str, Any]:
    build = subprocess.run(
        ["lake", "build", "OverthinkLean.WythoffSubtraction"],
        cwd=LEAN_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if build.returncode != 0:
        return {"ok": False, "build_log_tail": (build.stdout + build.stderr)[-3000:]}
    names = sorted(set(THEOREMS.values()))
    src = "import OverthinkLean.WythoffSubtraction\n" + "".join(
        f"#print axioms {t}\n" for t in names
    )
    out = subprocess.run(
        ["lake", "env", "lean", "--stdin"],
        cwd=LEAN_DIR,
        input=src,
        capture_output=True,
        text=True,
        check=False,
    )
    axioms = re.findall(r"depends on axioms: \[([^\]]*)\]", out.stdout)
    if len(axioms) != len(names) or any(
        not {x.strip() for x in a.split(",")} <= ALLOWED_AXIOMS for a in axioms
    ):
        return {"ok": False, "axiom_check": out.stdout + out.stderr}
    events = []
    for cid, e in registry.state().items():
        c = e["conjecture"]
        pid = c.get("evidence", {}).get("proposal_id")
        if (
            e["status"] == "survived"
            and c["kind"].startswith("claim_")
            and c["method"].startswith("llm:")
            and pid in THEOREMS
            and c["sequence_meta"].get("dataset") == "wsub_subsets5_n1000"
        ):
            events.append(
                {
                    "type": "proved",
                    "conjecture_id": cid,
                    "method": METHOD,
                    "lean_module": "OverthinkLean.WythoffSubtraction",
                    "lean_theorems": [THEOREMS[pid]],
                    "proposal_id": pid,
                }
            )
    if record:
        registry.append(events)
    return {"ok": True, "recorded": len(events)}
