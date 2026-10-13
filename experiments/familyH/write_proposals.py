"""Formats the assistant's family-H proposals as JSON. Touches no data: expressions are only
syntax-checked against the column names."""
import json, sys
from datetime import UTC, datetime
from overthink.conjecture.claims import compile_expr

COLS = ["subtraction_set", "x", "y", "grundy"]

def f1(a, b):
    return (f"(0 if ({a} % 2 == 0 and {b} % 2 == 0) else (2 if ({a} % 2 == 1 and {b} % 2 == 1) "
            f"else (1 if (({a} % 2 == 1 and {a} > {b}) or ({b} % 2 == 1 and {b} > {a})) else 3)))")

def pairs(m, table, u="x", v="y"):
    return " or ".join(f"({u} % {m} == {a} and {v} % {m} == {b})"
                       for a, bs in table.items() for b in bs)

def p_claim(rule, sets=None, group=None, where=None):
    c = {"kind": "predicate", "table": "data", "assert": f"(grundy == 0) == ({rule})"}
    if group: c["group"] = {"subtraction_set": group}
    w = []
    if sets: w.append("subtraction_set in (" + ", ".join(repr(s) for s in sets) + ")")
    if where: w.append(where)
    if w: c["where"] = " and ".join(w)
    return c

MM = ("min(x, y)", "max(x, y)")
props = []
def add(pid, statement, rationale, claim):
    props.append({"id": pid, "statement": statement, "rationale": rationale, "claim": claim})

add("H01", "For every S consisting of odd numbers with 1 in S (here {1}, {1,3}, {1,5}, {1,3,5}), "
    "the Grundy value is G(x,y) = 0 if x,y both even; 2 if both odd; for mixed parity 1 if the "
    "odd coordinate is the larger one, else 3.",
    "Identical 12x12 tables for all four sets; a parity case analysis of the mex recursion "
    "suggests odd moves of any size never add a missing or equal value.",
    {"kind": "predicate", "table": "data", "where": "subtraction_set in ('1', '1,3', '1,5', '1,3,5')",
     "assert": f"grundy == {f1('x', 'y')}"})
add("H02", "If 1 and 2 are in S and no element of S is divisible by 3 (here {1,2}, {1,2,4}, "
    "{1,2,5}, {1,2,4,5}), then G(x,y) = (x + y) mod 3.",
    "Each move lowers x+y by s or 2s, never 0 mod 3; s=1 and s=2 supply both smaller residues.",
    {"kind": "predicate", "table": "data",
     "where": "subtraction_set in ('1,2', '1,2,4', '1,2,5', '1,2,4,5')",
     "assert": "grundy == (x + y) % 3"})
for s in (2, 3, 4, 5):
    add(f"H03-{s}", f"Scaling: for S = {{{s}}}, G(x,y) = G_{{1}}(floor(x/{s}), floor(y/{s})) "
        "with G_{1} the formula of H01.",
        "Moves by multiples of s preserve x mod s and y mod s, so W({s}) is s^2 disjoint copies "
        "of W({1}).",
        {"kind": "predicate", "table": "data", "group": {"subtraction_set": str(s)},
         "assert": f"grundy == {f1(f'(x // {s})', f'(y // {s})')}"})
add("H04", "Scaling: for S = {2,4}, G(x,y) = (floor(x/2) + floor(y/2)) mod 3.",
    "W(2S) is isomorphic to four copies of W(S); combine with H02 for S = {1,2}.",
    {"kind": "predicate", "table": "data", "group": {"subtraction_set": "2,4"},
     "assert": "grundy == (x // 2 + y // 2) % 3"})
wy = {3: {0: [0], 1: [2], 2: [1]}, 4: {0: [0], 1: [2], 2: [1]},
      5: {0: [0], 1: [2], 2: [1], 3: [5], 5: [3]}}
add("H05", "For S = {1,2,3} and S = {1,2,3,5}: (x,y) is a P-position iff (x mod 4, y mod 4) is "
    "one of (0,0), (1,2), (2,1), i.e. a Wythoff P-position with both coordinates < 4.",
    "Period-4 lattice in both grids; the pairs are Wythoff pairs truncated to [0,4).",
    p_claim(pairs(4, wy[3]), sets=["1,2,3", "1,2,3,5"]))
add("H06", "For S = {1,2,3,4}: (x,y) is a P-position iff (x mod 5, y mod 5) is a Wythoff "
    "P-position with both coordinates < 5: (0,0), (1,2), (2,1).",
    "Period-5 lattice; same Wythoff-truncation pattern as H05.",
    p_claim(pairs(5, wy[4]), group="1,2,3,4"))
add("H07", "For S = {1,2,3,4,5}: (x,y) is a P-position iff (x mod 6, y mod 6) is a Wythoff "
    "P-position with both coordinates < 6: (0,0), (1,2), (2,1), (3,5), (5,3). Conjecturally "
    "W({1..k}) reduces to Wythoff modulo k+1 for every k.",
    "Period-6 lattice; the new pair (3,5) is exactly the next Wythoff pair.",
    p_claim(pairs(6, wy[5]), group="1,2,3,4,5"))
for a, s in ((2, "2,3"), (3, "3,4"), (4, "4,5")):
    m = 2 * a + 1
    rule = (f"(x % {m} < {a} and y % {m} < {a}) or (x % {m} == {a} and y % {m} == {2*a}) "
            f"or (x % {m} == {2*a} and y % {m} == {a})")
    add(f"H08-{a}", f"For S = {{{a},{a+1}}}: (x,y) is a P-position iff with m = {m}: "
        f"x mod m < {a} and y mod m < {a}, or (x mod m, y mod m) is ({a},{2*a}) or ({2*a},{a}). "
        "Conjecturally this holds for every pair {a, a+1} (a = 1 gives (x+y) mod 3 = 0).",
        "Same block-plus-two-points shape for a = 1, 2, 3, 4 with period 2a+1.",
        p_claim(rule, group=s))
a7 = {0: [0, 1], 1: [0, 1], 2: [4, 5], 3: [5, 6], 4: [2], 5: [2, 3], 6: [3]}
add("H09", "For S = {2,3,4,5} and S = {2,3,5}: the P-positions are exactly the (x,y) with "
    "(x mod 7, y mod 7) in {0,1}x{0,1} or in {(2,4),(2,5),(3,5),(3,6),(4,2),(5,2),(5,3),(6,3)}.",
    "Identical period-7 P-patterns for both sets in the whole 48x48 grid.",
    p_claim(pairs(7, a7), sets=["2,3,4,5", "2,3,5"]))
a8 = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [6, 7], 4: [6, 7], 6: [3, 4], 7: [3, 4]}
add("H10", "For S = {3,5}: (x,y) is a P-position iff (x mod 8, y mod 8) is in {0,1,2}^2, "
    "{3,4}x{6,7} or {6,7}x{3,4}.",
    "Period-8 symmetric pattern throughout the grid.",
    p_claim(pairs(8, a8), group="3,5"))
d5 = {0: [0, 2], 1: [4], 2: [2], 3: [1, 4], 4: [3]}
add("H11", "For S = {1,4}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff "
    "(u mod 5, v mod 5) is in {(0,0),(0,2),(1,4),(2,2),(3,1),(3,4),(4,3)}. The pattern is "
    "periodic with period 5 on each side of the diagonal but not symmetric across it.",
    "Rows above the diagonal follow a period-5 rule in (x mod 5, y mod 5); below, its mirror.",
    p_claim(pairs(5, d5, *MM), group="1,4"))
d6 = {0: [0, 1], 1: [0, 1], 2: [4, 5], 3: [5], 4: [2], 5: [3]}
add("H12", "For S = {2,3,4}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff "
    "(u mod 6, v mod 6) is in {0,1}x{0,1} or {(2,4),(2,5),(3,5),(4,2),(5,3)}.",
    "Period 6 = 2+4 split by the diagonal; checked row by row against the grid.",
    p_claim(pairs(6, d6, *MM), group="2,3,4"))
d8 = {0: [0, 1, 2], 1: [0, 1, 2], 2: [0, 1, 2], 3: [6, 7], 4: [7], 6: [3], 7: [4]}
add("H13", "For S = {3,4,5}: with u = min(x,y), v = max(x,y), (x,y) is a P-position iff "
    "(u mod 8, v mod 8) is in {0,1,2}^2 or {(3,6),(3,7),(4,7),(6,3),(7,4)}.",
    "Period 8 = 3+5 split by the diagonal (interval sets {a..b} seem to have period a+b).",
    p_claim(pairs(8, d8, *MM), group="3,4,5"))
f7 = {0: [0, 2], 1: [4, 6], 2: [1, 3], 3: [6], 4: [1, 3], 5: [5, 0], 6: [4]}
add("H14", "For S = {1,3,4}, away from the diagonal (max(x,y) >= 2 min(x,y)): (x,y) is a "
    "P-position iff (u mod 7, v mod 7) is in {(0,0),(0,2),(1,4),(1,6),(2,1),(2,3),(3,6),(4,1),"
    "(4,3),(5,5),(5,0),(6,4)} with u = min, v = max. Near the diagonal the pattern is different.",
    "Far rows repeat with period 7 in both coordinates; irregular band near the diagonal widens "
    "with x, so the boundary max >= 2 min is a guess and the riskiest claim here.",
    p_claim(pairs(7, f7, *MM), group="1,3,4", where="max(x, y) >= 2 * min(x, y)"))

for p in props:
    c = p["claim"]
    for key in ("where", "assert"):
        if c.get(key):
            compile_expr(c[key], COLS)
doc = {"provider": "session", "model": "claude-opus-5-5",
       "packet_sha256": sys.argv[1],
       "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
       "note": ("Written by the AI assistant (Claude Opus 5.5, Claude Code session) acting as the "
                "LLM proposer, from experiments/familyH/packet.md only; no code was run on the "
                "dataset; expressions were only syntax-checked. Interactive session, no API call."),
       "proposals": props}
json.dump(doc, open(sys.argv[2], "w"), indent=2)
print(len(props), "proposals written")
