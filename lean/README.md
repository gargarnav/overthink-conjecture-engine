# Lean 4 formalization

Lean `v4.35.0` with Mathlib `v4.35.0`. Build and check:

```bash
cd lean
lake exe cache get              # prebuilt Mathlib (~5 GB, first time only)
lake build
lake env lean CheckAxioms.lean  # must list only propext, Classical.choice, Quot.sound
```

Proof labels follow `docs/methodology.md` §3. **Nothing here uses `native_decide` or `sorry`**; CI fails if `sorryAx` or `Lean.ofReduceBool` appears in the axiom check.

| Result | File | Label |
|---|---|---|
| P-positions of a terminating game exist and are unique (`IsPLabelling.exists_of_wf`, `IsPLabelling.unique`) | `Game.lean` | general |
| k-row Chomp terminates (`Chomp.wf`) | `Chomp.lean` | general |
| **Two valid P-positions of k-row Chomp that differ in at most one row are equal** (`Chomp.eq_of_isP_of_eq_off`) | `Chomp.lean` | general |
| 4-row corollaries: each of a, b, c, d is determined by the other three. `unique_extension` is A. Garg, arXiv:2604.25952v2, Lemma 1 | `Chomp.lean` | general |
| Subtraction games: periodicity follows from a finite window of max(S) values (`periodic_of_window`); kernel-evaluable Grundy table (`grundy_eq_table`) | `Subtraction.lean` | general |
| S = {1,3,4} period 7, S = {1,2,3} period 4, S = {2,5,7} period 22, for **all** n | `Subtraction.lean` | general (finite window by kernel `decide`) |
| **511 generated theorems**: for every non-empty S ⊆ {1,…,9}, the Grundy sequence is periodic with the period and preperiod proposed by the pipeline, for **all** n ≥ n₀ | `Generated/SubtractionPeriodicity.lean` | general (finite window by kernel `decide`) |

The generated file is produced by `uv run overthink prove` from the conjecture registry. It only exports conjectures that survived 10× falsification, and records `proved` events with theorem names, toolchain and Mathlib revision. A conjecture is marked proved only if every set in its scope (the set it was mined from plus its aliases) compiles. A deliberately false period (S = {1,3,4}, period 6) fails to compile: `decide` evaluates the finite window to false.

Scope notes:
- The Chomp definitions use positions `Fin k → ℕ` of row lengths. Moves and validity mirror `src/overthink/games/chomp.py`. `IsP` is *the* P-labelling, unique by `isP_unique`.
- `grundy` is defined by the mex recursion, i.e. the Sprague-Grundy function of the subtraction game. It is not separately proved equal to the Sprague-Grundy value of an abstract game object.
