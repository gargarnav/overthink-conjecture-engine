"""The Lean exporter's selection and rendering (Lean itself is exercised in the Lean CI job)."""

from overthink.prove import lean_subtraction
from overthink.registry.store import Registry


def _propose(reg, cid, sset, period, n0, aliases=()):
    meta = {
        "dataset": "subtraction_x",
        "table": "data",
        "view": "grouped",
        "target": "grundy",
        "index": "n",
        "group": {"subtraction_set": sset},
        "transform": "raw",
    }
    sid = f"subtraction_x/data|grundy~n|subtraction_set={sset}|raw"
    reg.append(
        [
            {
                "type": "proposed",
                "conjecture_id": cid,
                "provenance": {"run_id": "r"},
                "conjecture": {
                    "id": cid,
                    "kind": "periodic",
                    "sequence_id": sid,
                    "params": {"period": period, "delta": 0, "n0": n0},
                    "sequence_meta": meta,
                },
            },
            {
                "type": "falsification",
                "conjecture_id": cid,
                "status": "survived",
                "per_sequence": [{"sequence_id": sid}]
                + [
                    {"sequence_id": f"subtraction_x/data|grundy~n|subtraction_set={a}|raw"}
                    for a in aliases
                ],
            },
        ]
    )


def test_targets_cover_aliases_and_render(tmp_path):
    reg = Registry(tmp_path / "e.jsonl")
    _propose(reg, "C-1", "1,3,4", 7, 0)
    _propose(reg, "C-2", "1,2,3", 4, 0, aliases=["1,2,3,9"])
    targets = lean_subtraction._targets(reg)
    assert [t["sets"] for t in targets] == [[(1, 3, 4)], [(1, 2, 3), (1, 2, 3, 9)]]
    text = lean_subtraction.render(targets)
    assert "theorem sub_1_2_3_9 :" in text
    assert "grundy [1, 3, 4] (n + 7) = grundy [1, 3, 4] n" in text
    assert "periodic_of_window (m := 9) (n₀ := 0)" in text
    assert "native_decide" not in text and "sorry" not in text


def test_proved_conjectures_stay_in_the_generated_file(tmp_path):
    reg = Registry(tmp_path / "e.jsonl")
    _propose(reg, "C-1", "1,3,4", 7, 0)
    reg.append([{"type": "proved", "conjecture_id": "C-1", "method": lean_subtraction.METHOD}])
    (t,) = lean_subtraction._targets(reg)
    assert t["already_proved"] and t["sets"] == [(1, 3, 4)]
