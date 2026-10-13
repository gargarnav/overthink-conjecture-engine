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
| W(S) Wythoff subtraction games: a function that never matches its own value on an option and reaches every smaller value on one *is* the Grundy function (`WSub.grundy_eq_of`); scaling `G_{k·S}(x,y) = G_S(⌊x/k⌋,⌊y/k⌋)` (`WSub.grundy_scale`) | `WythoffSubtraction.lean` | general |
| **LLM-proposed (family H), proved for every position:** H01 (S odd, 1 ∈ S ⇒ G = F₁, an explicit parity formula), H02 (1, 2 ∈ S, 3 ∤ s ⇒ G = (x+y) mod 3), H03 (G_{s} = F₁(⌊x/s⌋,⌊y/s⌋)), H04 (G_{2,4} = (⌊x/2⌋+⌊y/2⌋) mod 3) | `WythoffSubtraction.lean` | general |
| **W({a, a+1}) for every a ≥ 1: (x,y) is a P-position iff, with m = 2a+1, x mod m < a and y mod m < a, or (x mod m, y mod m) ∈ {(a,2a), (2a,a)}** (`WSub.pair_P_positions`; LLM proposal H08, found from a ≤ 4). Write-up: `docs/results/W_pair_theorem.md` | `WythoffSubtraction.lean` | general |
| **511 generated theorems**: for every non-empty S ⊆ {1,…,9}, the Grundy sequence is periodic with the period and preperiod proposed by the pipeline, for **all** n ≥ n₀ | `Generated/SubtractionPeriodicity.lean` | general (finite window by kernel `decide`) |

The generated file is produced by `uv run overthink prove` from the conjecture registry. It only exports conjectures that survived 10× falsification, and records `proved` events with theorem names, toolchain and Mathlib revision. A conjecture is marked proved only if every set in its scope (the set it was mined from plus its aliases) compiles. A deliberately false period (S = {1,3,4}, period 6) fails to compile: `decide` evaluates the finite window to false.

Scope notes:
- The Chomp definitions use positions `Fin k → ℕ` of row lengths. Moves and validity mirror `src/overthink/games/chomp.py`. `IsP` is *the* P-labelling, unique by `isP_unique`.
- `grundy` is defined by the mex recursion, i.e. the Sprague-Grundy function of the subtraction game. It is not separately proved equal to the Sprague-Grundy value of an abstract game object.

## License

The Lean code in this directory is MIT-licensed (see `../LICENSE`). It depends on Lean 4 and Mathlib, which are Apache-2.0; MIT and Apache-2.0 are compatible, and nothing from Mathlib is copied into this repository (it is fetched by Lake).
