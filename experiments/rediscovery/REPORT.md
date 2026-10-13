# Blind rediscovery of 4×n Chomp structure: report (step 5)

**Status: scores below are PROPOSED by the AI assistant and await confirmation by the author** (`PROTOCOL.md`: scoring is done by the author). Inputs: raw output of steps 2–3 (`run/`), candidate table (`survivors.md`), ground truth (`ground_truth.md`).

## Summary

The frozen classical pipeline **did not rediscover any of the four v1 conjectures as stated (0 found, 0 partial, 4 missed)**. Of its 73 proposals, 69 survived 10× falsification. They are exact eventual-periodicity statements that appear in neither version of the paper. None contradicts the ground truth.

Separately, applying the same falsification-first checks by hand to the ground truth (Part B, **not** pipeline output) gave these findings:
- **v1 Conjecture 1** is a theorem with a one-move proof, which v2 already gives.
- **v1 Conjecture 2** is false as literally stated.
- **v1 Conjecture 3's period-112 signal** is not supported by a modulus control.
- **v2's HIGH/LOW split** coincides exactly with a sharper, per-position criterion.

## Part A: protocol scoring (frozen pipeline vs. ground truth)

### v1 conjectures (primary)

| Ground truth | Proposed score | Justification |
|---|---|---|
| C1 Unique Extension | **Missed** | No candidate states it. The frozen view builder *did* compute it: `functional_targets` finds that each of a, b, c, d is determined by the other three, both in the a ≤ 100 window and on all 35,029,679 positions. But it only used this internally to build sequences and never emitted it as a conjecture. That is a design gap in the pipeline (see "Lessons"). |
| C2 Asymptotic Ratios | **Missed** | A statement about limits of ratio statistics over sets of positions; the miners have no such statement form (limitation stated in advance in `PROTOCOL.md`). |
| C3 Period-112 Mask | **Missed** | No statement about period 112 or about extending triples. Related but different: the miners found exact periods of a − b along b for fixed (c, d), with periods 1, 2, 3, 4, 6, 8, 12 and 16 (and re-proposed 48 and 192 after refutations). There is no factor of 7 anywhere. These are not consequences of C3, so they don't count as partial. |
| C4 Linear Cone | **Missed** | Geometric/statistical statement form not expressible by the miners. |

**Wrong** (survivors contradicting the ground truth): none. C3 and C4 are statistical, and C1 is consistent with all survivors.

### v2 statements (secondary)

| Ground truth | Proposed score | Justification |
|---|---|---|
| Lemma 1 (Unique Extension, proved) | **Missed** | As C1 above. |
| Conjecture 1 (HIGH family) | **Missed** | Statement form not expressible. |
| Conjecture 2 (LOW family) | **Missed** | Statement form not expressible. |
| Conjectures 3, 4 | **Missed** | As v1. |

### What the pipeline did produce

- 73 proposals → **69 survived** (extension 10–21× per sequence), **4 refuted**, 0 untestable. Every proposal has the form "a(b + p) = a(b) + p for all b ≥ n0", for fixed (c, d) (or the same with a and b swapped), i.e. a − b is eventually periodic in b. The full table is in `survivors.md`.
- The 4 refuted proposals (period 1 for (c, d) = (20,19), (21,4), (21,21), (29,21)) failed at b = 81–130. The full-data re-proposals had periods 192, 48, 192 and 1. This is the falsification loop working as designed.
- Coverage: only 61 of 364 (c, d) sequences produced a proposal within a ≤ 100. No second-order (cross-group) statements were produced.
- **Novelty is not claimed.** Eventual periodicity of P-positions along a row with the other rows fixed is the kind of statement covered by known periodicity results for Chomp-like poset games. Candidate reference: S. Byrnes, "Poset game periodicity", *Integers* 3 (2003), #G3 (*to verify*; the author's reference solver is named after this approach). These survivors should be checked against that literature and marked `known` where it applies.

### Lessons for the pipeline (recorded before any change)

1. Functional dependencies found in the data are conjectures in their own right and should be emitted as candidates (with the one-move argument as an obvious proof target for Lean).
2. The miners only express exact single-sequence laws. Distributional statements (limits of medians, bimodality, densities) need a separate, explicitly statistical proposer with its own falsification rules.
3. With a window of a ≤ 100, most (c, d) sequences are too short. A larger proposal window (with a correspondingly larger falsification set, now available at n ≤ 3000) is the obvious next run. It must be a new, separately pre-registered run.

## Part B: post-hoc falsification of the ground truth (AI-assisted, not pipeline output)

These checks were written by the AI assistant *after* reading the ground truth, so they are not blind and not part of the protocol score. Scripts are in `posthoc/`. They use `chomp4_n1000` and the author's n ≤ 3000 data. Data provenance:
- 961,619,972 rows, the count v2 reports.
- An independent re-solve of every P-position with a ≤ 3000 and c ≤ 300 with this project's solver matched exactly: 47,986,319 positions.

**v1 C1 / v2 Lemma 1: a theorem, and it holds for every coordinate.** v2's proof (one move in the bottom row) applies to every row:
- a is unique given (b, c, d): move to (a′, b, c, d) for b ≤ a′ < a.
- b is unique given (a, c, d): row-2 move to (a, b′, c, d), c ≤ b′ < b.
- c is unique given (a, b, d): row-3 move to (a, b, c′, d), d ≤ c′ < c.
- d is unique given (a, b, c): row-4 move.

This matches the data, where all four functional dependencies hold. The result is a natural first target for a *general* Lean proof.

**v1 C2: false as literally stated; only the medians behave as described.**
- (a, a−1, 0, 0) is a P-position for every a (2-row Chomp), so b/a → 1 and c/a = d/a = 0 along it.
- Among P-positions with a ∈ [950, 1000], b/a ranges over [0.436, 1.000] and d/a over [0.000, 0.896].
- The per-a *medians* are close to the stated constants: b/a 0.769, c/a 0.499, d/a 0.220 at a ∈ [950, 1000].

**v1 C3 (period 112): not supported.**
- *Autocorrelation:* recomputing it for the lexicographic d-sequence (n ≤ 500, mean removed) puts lag 112 at **rank 190 of 299** lags in 2..300 (r = 0.213). The autocorrelation decays smoothly from r = 0.868 at lag 2, with no peak at 112. v1/v2 Figure 2 also shows no visible spike at 112.
- *Modulus control:* conditional mutual information I(extends; (a − b) mod m | c), over all 21,084,250 triples with a ≤ 500 (4,316,097 extending):
  - It rises almost monotonically with m: 7 → 2.0, 56 → 41.3, 112 → 110.8, 224 → 248.4 millibits.
  - Among moduli 100–124, 112 ranks **13th of 25**; the top five are 124, 123, 122, 121 and 120.
  - Cutting a − b into 112 *contiguous* intervals (no periodicity) gives 271.5 millibits, against 110.8 for mod 112.

  So the apparent advantage of mod 112 over mod 56 comes from finer resolution of a − b, i.e. from the cone geometry, not from periodicity. The χ² comparison in the paper has the same issue, since χ² also grows with the number of bins.

**v2 HIGH/LOW: equivalent to a sharper per-position criterion.** For a ∈ [200, 3000] (2,801 values):
- HIGH (per-a median of d/a > 0.21) holds for 56.19%, reproducing v2.
- Two per-a medians fall inside v2's stated gap [0.194, 0.235]: a = 307 (0.2345) and a = 345 (0.1942). They sit at its edges and probably reflect a different median convention for even counts.
- **HIGH ⇔ the largest d/a among the P-positions with first row a exceeds 0.45, with 100% agreement.** At LOW a the maximum is in [0.432, 0.446]; at HIGH a it is in [0.855, 0.907]. No a falls between.
- The within-a distribution of d/a has no gap. HIGH values of a carry an *extra population* of P-positions with large d. At a = 2999 that is 244,505 of 1,075,299 positions with d > 0.45a; at a = 3000 there are none, out of 816,614.
- So v2 Conjectures 1–2 are false as literally stated: HIGH a's contain P-positions with d/a anywhere from 0 to about 0.9. The "families" are values of a, not two trajectories of positions.
- Proposed sharper open question: **characterize the a for which some P-position has d > 0.45a**, and explain the gap in max d/a between 0.446 and 0.855. Having a P-position with b = a does not explain it (agreement 56%).

**Other notes for the author**
- v2 Remark 2 / Open Question 1 asks whether an extension always exists for large a. About 79.5% of triples with a ≤ 500 do not extend. For a 3-row P-position (a, b, c), the extension (a, b, c, 0) is immediate, since an empty fourth row is the 3-row game. The question needs a sharper formulation.
- v2 §7.2: "every (k−1)-tuple extends to exactly one k-tuple" would not make k × n Chomp determined by 2 × n Chomp. Knowing which d is the extension still requires solving the game.
- The v2 Figure 1 caption gives the colours the other way round from the legend.

## Data and reproduction

```bash
uv run overthink mine experiments/configs/mining/rediscovery_chomp4.yaml   # step 2 (from tag rediscovery-frozen)
uv run overthink falsify <run dir>                                          # step 3
uv run python -I experiments/rediscovery/posthoc/v1_checks_n1000.py       # Part B
uv run python -I experiments/rediscovery/posthoc/c3_modulus_control.py
uv run python -I experiments/rediscovery/posthoc/v2_per_a_stats_n3000.py  # needs n <= 3000 data in data_ref/
uv run python -I experiments/rediscovery/posthoc/v2_high_low_criterion.py
```
