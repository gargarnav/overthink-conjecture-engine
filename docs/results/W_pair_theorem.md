# The P-positions of W({a, a+1}) for every a

**Status:** proved for every a ≥ 1 (Lean 4, kernel-checked, standard axioms only). **Novelty:** not found in the literature we searched (below); pending review by a specialist.

## Statement

Let W({a, a+1}) be the two-heap game where a move removes a or a+1 tokens from one heap, or the same amount (a or a+1) from both heaps. Normal play. Equivalently, it is the finite two-dimensional subtraction game with the six move vectors (a,0), (0,a), (a,a), (a+1,0), (0,a+1), (a+1,a+1).

**Theorem.** Let a ≥ 1 and m = 2a + 1, and write r = x mod m, t = y mod m. Then (x, y) is a P-position if and only if

  r < a and t < a,  or  (r, t) = (a, 2a),  or  (r, t) = (2a, a).

So the P-positions are periodic with period 2a+1 in both directions. In each m × m block they form an a × a square in the corner plus two extra points. For a = 1 this is the familiar condition x + y ≡ 0 (mod 3).

Lean: `Overthink.WSub.pair_P_positions` in `lean/OverthinkLean/WythoffSubtraction.lean`:
```lean
theorem pair_P_positions {a : ℕ} (ha : 1 ≤ a) :
    ∀ x y, grundy [a, a + 1] x y = 0 ↔ PairP a x y
```

## Proof

Call B the set described in the theorem. It suffices to show (i) no move leads from B to B, and (ii) every position outside B has a move into B. Induction on x + y then shows that B is exactly the set of P-positions. (In Lean this step is `grundy_zero_iff_of`.)

**Residues under a move.** Subtracting a from a heap with residue r gives residue r − a if r ≥ a, and r + a + 1 otherwise. Subtracting a + 1 gives r − a − 1 if r ≥ a + 1, and r + a otherwise. (Lean: `sub_mod_eq`.)

**(i) No move from B to B.**
- *From (r, t) with r, t < a.* A move on the first heap sends r to [a+1, 2a] (removing a) or to [a, 2a−1] (removing a+1), and leaves t < a. The result is not in B: its first residue is ≥ a, and t is neither a nor 2a. The second heap is symmetric. A diagonal move by a sends both residues into [a+1, 2a]; a diagonal move by a+1 sends both into [a, 2a−1]. Neither lands in B, because every point of B with both residues ≥ a has one residue equal to a and the other equal to 2a.
- *From (a, 2a).* The six moves give (0, 2a), (2a, 2a), (a, a), (a, a−1), (0, a) and (2a, a−1), none of which is in B. The point (2a, a) is symmetric.

**(ii) A move into B from outside B.** Let (r, t) ∉ B.
- If r < a, then t ≥ a. If t ≤ 2a−1, remove a from the second heap (residue t − a < a). If t = 2a, remove a+1 (residue a − 1). Either move is available, since y ≥ t ≥ the amount removed.
- If t < a, this is symmetric.
- If r, t ≥ a: when both are ≥ a+1, remove a+1 from both; when both are ≤ 2a−1, remove a from both. Otherwise one residue equals a and the other equals 2a, so (r, t) ∈ B, contrary to assumption. ∎

## How it was found

1. **Proposed by the AI proposer** (proposal H08, `experiments/familyH/llm_proposals.json`, commit `f9020d9`). It was written from 48×48 P-position pictures of the 31 games W(S), S ⊆ {1,…,5}, in which only a = 1, 2, 3, 4 occur. The general form "period 2a+1, an a×a square plus (a, 2a) and (2a, a)" was stated as a conjecture for every a.
2. **Survived falsification** on all positions with x, y < 1000 for a = 2, 3, 4: 3,000,000 positions, 10× the proposal window per axis (commit `186d49f`).
3. **Proved for every a** in Lean, and cross-checked against the independent Rust solver for a = 1, …, 30 on x, y < 12(2a+1), with 0 mismatches. A deliberately wrong variant, with (a, 2a−1) in place of (a, 2a), fails to compile.

## Literature check (2026-10-13)

- Larsson, Saha & Yokoo, *Subtraction games in more than one dimension* (arXiv:2307.12458v4). They solve two-move rulesets and some three-move ones, prove row/column eventual periodicity of outcomes, and in Theorem 16 treat diagonal "twin" rulesets {(a,a), (b,b)} with optional (a,b), (b,a). Those also give patterns mod a + b, but the rulesets differ from W({a, a+1}), which has six moves including moves along the axes.
- Duchêne, Fraenkel, Gravier & Nowakowski, *Another bridge between Nim and Wythoff* (Australas. J. Combin. 44, 2009): restricted Wythoff variants with different rules.
- Bounded Wythoff (any amount up to R; possibly in Duchêne, Fraenkel, Nowakowski & Rigo, JCTA 2010) contains W({1, 2}) but not W({a, a+1}) for a ≥ 2. *Not yet read.*
- Targeted web searches found no statement of this result.

**What this result is and is not.** Once the statement is known, the proof is elementary: a residue case analysis. The contribution is (1) the statement itself, a complete classification of the P-positions for an infinite family of six-move two-dimensional subtraction games, found by an AI proposer from data covering only a ≤ 4; (2) its falsification and machine-checked proof for every a; and (3) the pipeline that produced it end to end. The outcome (P/N) classification is proved here; the Grundy values are not.
