# SPDX-License-Identifier: MIT
"""Record Lean proofs of the 4-row Chomp functional dependencies in the registry.

`lean/OverthinkLean/Chomp.lean` proves, for all P-positions of 4-row Chomp, that each row
length is determined by the other three (a corollary of `eq_of_isP_of_eq_off`). This implies
the dataset-level functional-dependency conjectures mined from any set of P-positions.
"""

from __future__ import annotations

import re
import subprocess
from typing import Any

from overthink.prove.lean_subtraction import ALLOWED_AXIOMS, LEAN_DIR
from overthink.registry.store import Registry

THEOREMS = {  # target column -> Lean theorem
    "a": "Overthink.Chomp.unique_first_row",
    "b": "Overthink.Chomp.unique_second_row",
    "c": "Overthink.Chomp.unique_third_row",
    "d": "Overthink.Chomp.unique_extension",
}
METHOD = "general: one-move argument (eq_of_isP_of_eq_off), kernel-checked"


def run(registry: Registry, record: bool = True) -> dict[str, Any]:
    build = subprocess.run(
        ["lake", "build", "OverthinkLean.Chomp"],
        cwd=LEAN_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if build.returncode != 0:
        return {"ok": False, "build_log_tail": (build.stdout + build.stderr)[-3000:]}
    src = "import OverthinkLean.Chomp\n" + "".join(
        f"#print axioms {t}\n" for t in THEOREMS.values()
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
    if len(axioms) != len(THEOREMS) or any(
        not {x.strip() for x in a.split(",")} <= ALLOWED_AXIOMS for a in axioms
    ):
        return {"ok": False, "axiom_check": out.stdout + out.stderr}
    events = []
    for cid, e in registry.state().items():
        c = e["conjecture"]
        if (
            c["kind"] == "functional_dependency"
            and e["status"] != "refuted"
            and c["sequence_meta"].get("dataset", "").startswith("chomp4")
            and e["status"] != "proved"
        ):
            target = c["params"]["target"]
            if sorted(c["params"]["determinants"]) == sorted(set("abcd") - {target}):
                events.append(
                    {
                        "type": "proved",
                        "conjecture_id": cid,
                        "method": METHOD,
                        "lean_module": "OverthinkLean.Chomp",
                        "lean_theorems": [THEOREMS[target]],
                        "note": "Lean statement covers all P-positions of 4-row Chomp",
                    }
                )
    if record:
        registry.append(events)
    return {"ok": True, "recorded": len(events)}
