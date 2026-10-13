# Results log

Dated, append-only record of what actually worked and what failed. Newest entries at the bottom. This file is the source of truth for any number cited in papers or grant materials.

---

## 2026-10-13: Phase A, repository scaffold

**Done**
- Repository created: MIT license, CITATION.cff, README, docs skeleton.
- Python package `overthink` (Python 3.12, uv) with a Rust core `overthink._core` built via maturin/PyO3 0.29.
- Rust core currently exposes only `mex` (minimum excludant) and `core_version`, as a build/integration smoke test.
- CLI: `overthink info`, `overthink --help`.
- Tests: 9 pytest + 3 cargo tests passing locally (macOS arm64, Apple M4). Ruff, rustfmt and clippy clean.

**Not done / notes**
- No solvers, data, miners or conjectures yet. No mathematical results to report.
- Lean toolchain not yet installed (planned for Phase I).
- Repo is local only; no public GitHub remote yet.

---

## 2026-10-13: Phase B, exact solvers

**Done**
- Rust solvers (`rust/src/`): subtraction-game Grundy values, Wythoff Grundy table, and 4-row Chomp P-positions (per-(c,d)-pair algorithm, parallel over anti-diagonals, exact under truncation a ≤ max_a).
- Pure-Python definitional oracles in `src/overthink/games/` (brute-force k-row Chomp, Wythoff, subtraction games).
- Test suite: 38 pytest + 8 cargo tests passing. Checks against brute force (4-row Chomp n ≤ 20, 3-row n ≤ 20, Wythoff 40×40, eight subtraction sets to 500) and known theorems (2-row Chomp P-positions = (b+1, b); every rectangle with ≥ 2 squares is N; Wythoff P-positions = Beatty pairs, checked on 1000×1000; S = {1,2,..,k} gives n mod (k+1); S = {1,3,4} has period 7).

**4-row Chomp validation**

| Check | Independent of the fast algorithm? | n | P-positions | Result |
|---|---|---|---|---|
| Our fast solver vs Python brute force (definition) | yes | 40 | 2,770 | identical |
| Our fast solver vs author's `krow_brute.cpp` (definition) | yes | 120 | 59,501 | identical |
| Our fast solver vs author's `rows4.cpp` output (`p_positions_4xn_cpp_1000.csv`, SHA-256 `b907bd55…88f5f`) | **no**: same algorithm, independently re-implemented | 1000 | 35,029,679 | identical |

The n = 1000 run took 53 s wall time on an Apple M4 (10 cores) with about 7 GB peak RSS, including loading the CSV. Reproduce with `uv run python experiments/validate_chomp4.py`.

**P-position counts (4-row Chomp, all positions with a ≤ n)**
- n = 500: 4,316,097 (our solver and the reference CSV agree). This is the "4.3M+" figure in the author's paper, as the author confirmed on 2026-10-13.
- n = 1000: 35,029,679.

**Blind-protocol exposure disclosure (methodology §4)**
Before any miner was written, the agent building this was exposed to:
(1) comments in `reference/cpp/rows4.cpp` stating solver-level game facts (a diagonal P-position (x,x,c,d) makes every larger b in that pair N; a constant P-position makes a whole pair N);
(2) a comment in `reference/cpp/rows3_fast.cpp` mentioning a "mean eventual shift" for live rows in 3-row Chomp;
(3) three truncated lines of `reference/cpp/sealed/rows4_fast.cpp`, shown by a keyword search, indicating the author studied eventual periodicity of `delta(b) = a − b`.
The periodicity miner was planned before this exposure (Step 0 plan, same date). The sealed files have not been read. The ground-truth statements have not been seen.

---

## 2026-10-13: Phase C, datasets

**Done**
- `overthink generate CONFIG` → `data_out/<id>/data.parquet` (zstd) plus a tracked `datasets/<id>/` holding an auto-generated dataset card, `manifest.json` (params, schema version, row count, hashes, git SHA, library versions, timing) and `sample.parquet`.
- `overthink verify ID` checks a dataset's content hash against its tracked manifest.
- Schema v1.0 is defined once in `src/overthink/data/schema.py`.
- 11 new tests (49 pytest total): schema conformance, canonical sort, determinism, round-trip, tamper detection, CLI, and the chomp4 dataset vs brute force at n = 15.

**Datasets generated** (Apple M4, git `1c73b57`)

| Dataset | Rows | Parquet size | Generation time |
|---|---|---|---|
| `chomp4_n1000` | 35,029,679 | 50.1 MB (the reference CSV is 686 MB) | 51 s |
| `wythoff_n1000` | 1,000,000 | 1.4 MB | 2.9 s |
| `subtraction_subsets9_n2000` | 1,022,511 | 0.3 MB | 0.1 s |

**Reproducibility check:** regenerating `chomp4_n1000` into a separate directory gave an identical `content_sha256` and an identical `file_sha256`, so the Parquet file is byte-identical on the same machine and library versions. Cross-machine byte identity hasn't been tested; `content_sha256` is the hash meant to be portable.

**Not done**
- Full datasets are not hosted publicly yet (Hugging Face/Zenodo TODO).
- Data license CC BY 4.0 is proposed, not confirmed.

---

## 2026-10-13: Phase D, classical miners (development on non-Chomp data only)

**Built**
- Miners (`src/overthink/conjecture/`): ultimate (additive) periodicity; polynomial and quasi-polynomial (difference tables, exact rational fits); linear recurrences (Berlekamp-Massey over Q); floor-linear/Beatty (exact feasible-slope interval, simplest rational, fixed library of 15 named constants); exact OEIS snapshot matching (implemented and unit-tested on a fake snapshot; **no real OEIS snapshot downloaded yet**).
- Selection by minimal description length per sequence; losing alternatives are kept in the evidence.
- `checks.check` tests any candidate on a longer sequence and reports the first counterexample.
- Generic views: grouped (auto-detected functional dependencies), zero-set (P-positions), enumeration (with symmetry detection), second-order (period parameters across groups).
- CLI: `overthink mine CONFIG`, `overthink benchmark`. 72 tests passing.

**Synthetic benchmark** (`uv run overthink benchmark --config experiments/configs/mining/dev_subtraction_wythoff.yaml --n 200 --seed 7`, report in `experiments/miner_benchmark/REPORT.md`). A candidate counts as correct only if it holds on a 10× extension of the planted sequence.
- Planted periodic, additive-periodic, long-preperiod periodic, linear-recurrence, polynomial, quasi-polynomial and Beatty sequences: 200/200 recovered in every family. The exact period, delta and preperiod were recovered 200/200 in all three periodic families.
- Negative controls (uniform random, random walk): 0 candidates on 400 sequences.
- Noisy periodic control (each term corrupted with probability 1/40): **111/200 sequences produce a false proposal** (a clean tail looks periodic). These are refuted by the 10× check. Requiring the periodic part to cover ≥ 50% of the data cut false proposals to 40/200, but recall on true long-preperiod sequences fell from 200/200 to 87/200. We keep the permissive setting and rely on falsification.
- Beatty sequences: 19 strong guesses for the slope (a rational or a named constant) were refuted on the 10× extension. The weak statement (some real slope works) survived in all 200 cases.

**Problems found and fixed during development**
- The periodicity miner reported spurious additive periods for Beatty sequences near continued-fraction convergents (28/40 wrong in the first run). Fixed by selecting on description length across all miners.
- A test generator bug made the uniform-random control constant; it was caught because it produced candidates.
- Logically equivalent duplicates (Y vs Y − index) inflated candidate counts by about 55%. Structural miners now run on raw sequences only.

**Development run on real non-Chomp data** (`dev_subtraction_wythoff-20261013T142154Z`, proposal windows n ≤ 199 and x, y ≤ 99; these are *unfalsified proposals*)
- Subtraction games (511 sets S ⊆ {1..9}): a periodicity candidate for the Grundy sequence of all 511 sets. Spot checks agree with textbook values: {1,2,3} period 4, {1,2} period 3, {1,3,4} period 7.
- Wythoff: from the P-positions alone the pipeline proposed a_k = ⌊kφ + β⌋, b_k = ⌊kφ² + β⌋ with β ∈ [0, 0.021) (so β = 0 is allowed), and b_k − a_k = k. That is Wythoff's theorem. Rows y = 0..6 of the Grundy table were proposed additively periodic (periods 1, 3, 3, 6, 12, 24, 12). This agrees with the published result that rows are ultimately additively periodic (Dress, Flammenkamp & Pink 1999; *citation to verify*). The specific periods haven't been checked against the literature.

**Rediscovery pre-registration drafted** (not yet frozen): `experiments/rediscovery/PROTOCOL.md` and `experiments/configs/mining/rediscovery_chomp4.yaml`. Its views, miner and second-order parameters are identical (checked with diff) to the development config. **No miner has been run on Chomp data.**

---

## 2026-10-13: Phase E, falsifier and registry

**Built**
- `overthink falsify RUN_DIR`: rebuilds the run's views on the full dataset, checks each candidate on its sequence and all aliases, and stores counterexamples (index, observed, predicted). Refuted candidates get unfalsified re-proposals from the full data. Second-order candidates are checked against parameters re-estimated on the full data.
- `registry/events.jsonl`: an append-only event log (proposed, falsification, known, proved) with provenance: run ID, config, dataset content hash, method, model (none), seed (none), git SHA. "Refuted" is permanent.
- 6 new tests (78 total), including injected false candidates (refuted at the right index, true period re-proposed), a missing sequence (untestable), registry status rules, and a toy family that exercises second-order survival and refutation.

**Problems found and fixed**
- Enumeration views were applied to Grundy-value tables, producing a tautology ("n_k = k") that survived trivially and appeared as one candidate covering all 511 subtraction sets. Enumeration is now only applied to sets of positions.
- Second-order statements were wrongly marked untestable ("no new terms"); for them, the new evidence is parameter re-estimation on 10× data.
- Two runs started in the same second collided on directory name.

**Dev data falsification** (proposal windows n ≤ 199 and x, y ≤ 99; re-tested at n ≤ 2000 and x, y ≤ 999, a scale factor of 10.05–10.09)
- All 297 proposals survived (279 subtraction, 18 Wythoff). Per sequence, the median was 1,990 checks; extension factors ranged 9.6–10.6×. This includes the Wythoff Beatty statements with φ and φ² (checked over 382 P-pairs) and all 511 subtraction-game periodicity statements.
- Stress test: no natural refutations occurred even with proposal windows of n ≤ 40 (subtraction, 50× scale, 101/101 survived) or x, y ≤ 40 (Wythoff, 25×, 7/7 survived). The miners' evidence thresholds kept them from proposing on too little data. The refutation path is verified by tests and by the synthetic benchmark (false proposals on noisy controls are refuted).
- *Interpretation:* survival at 10× is evidence, not proof. For subtraction games, ultimate periodicity is a theorem (finite subtraction sets), so these survivals mainly confirm that the miners' periods and preperiods are right on this range.

---

## 2026-10-13: Rediscovery steps 1–3 (blind run on 4-row Chomp)

- **Step 1:** tag `rediscovery-frozen` at `3e4aead`, after all pre-freeze checks passed: 78 pytest + 8 cargo tests, the rediscovery config's views, miners and second-order sections identical to the dev config (diff), and the dataset hash verified.
- **Step 2** (commit `bbdd356`): proposal window a ≤ 100 gave 388 sequences (364 in view `a~b` grouped by (c, d) ≤ 30, and 24 in `b~a`). That produced 73 candidates, all of the form "a(b + p) = a(b) + p for b ≥ n0" for a fixed (c, d). The periods proposed were 1, 2, 3, 4, 6, 8, 12 and 16. There were **no second-order sequences**: no 12 consecutive groups all had a candidate, so no statement about how p or n0 depends on (c, d) was proposed. 2.5 s.
- **Step 3** (commit `320b832`): falsification at a ≤ 1000 (scale factor 10.0, per-sequence extension 10–21×): **69 survived, 4 refuted, 0 untestable**. 18 s.
  - The 4 refuted claims were all period 1 (a = b + const from n0 on), for (c, d) = (20, 19), (21, 4), (21, 21) and (29, 21). They failed at b = 81, 106, 81 and 130 respectively. Re-proposals from the full data (unfalsified) have periods 192, 48, 192 and 1 (the last from n0 = 881).
- Candidate table: `experiments/rediscovery/survivors.md` (mechanically generated).
- **Coverage:** only 61 of the 364 `a~b` sequences produced a candidate in the window. The rest were silent: no period with enough support within a ≤ 100.
- **Ground truth is still not in the repository.** Next: the author commits `experiments/rediscovery/ground_truth.md` (step 4), then scoring (step 5).

---

## 2026-10-13: Commit history rewritten (messages and author emails only)

Before the first publication, at the author's request: an automatically added attribution trailer was removed from all 19 commit messages, and the author's personal email was replaced with the GitHub no-reply address. Every file tree is unchanged, verified commit by commit. All SHAs changed, and SHAs cited earlier in this log and in manifests, run outputs and registry events are the original ones: see `docs/commit_sha_map.md`. The tag `rediscovery-frozen` now points to `1a99e9c` (originally `3e4aead`) with its original tagger date. Full pre-rewrite backups exist as git bundles outside the repository.

---

## 2026-10-13: Rediscovery steps 4–5 (ground truth and scoring)

- **Step 4** (`8004d8d`): the author's v1 (arXiv:2604.25952v1) and v2 (v2, n ≤ 3000) conjectures, committed verbatim after steps 1–3 were public on GitHub.
- **Step 5:** `experiments/rediscovery/REPORT.md`. Scores are proposed by the AI assistant and await the author's confirmation.
  - **Pipeline vs v1: 0 found, 0 partial, 4 missed. No wrong survivors.**
  - The frozen view builder computed all four "coordinate is determined by the others" dependencies (C1 included) but never emitted them as conjectures: a design gap.
  - C2–C4 are distributional or geometric statements the miners cannot express.
  - The 69 surviving proposals (exact eventual periodicity of a − b in b for fixed (c, d)) are in neither paper version. They are probably covered by known periodicity results (Byrnes 2003, to verify); novelty is not claimed.
- **Post-hoc checks of the ground truth** (AI-assisted, not blind, not pipeline output; scripts in `experiments/rediscovery/posthoc/`):
  - The author's n ≤ 3000 data has 961,619,972 rows. An independent re-solve of all P-positions with a ≤ 3000, c ≤ 300 matches it exactly (47,986,319 positions).
  - v1 C1 = v2 Lemma 1, a theorem. The one-move proof gives uniqueness of every coordinate given the other three.
  - v1 C2 is false as stated: the family (a, a−1, 0, 0) has b/a → 1. Only the per-a medians match.
  - v1 C3 is not supported. Lag 112 ranks 190/299 in the d-sequence autocorrelation. Mod-112 information ranks 13/25 among moduli 100–124 and is beaten by plain contiguous binning of a − b (271.5 vs 110.8 millibits).
  - v2 HIGH/LOW (per-a median of d/a > 0.21) ⇔ the max d/a among P-positions at that a exceeds 0.45: 100% agreement over a ∈ [200, 3000]. Max d/a lies in [0.432, 0.446] for LOW a and [0.855, 0.907] for HIGH a. v2 Conjectures 1–2 are therefore false as literally stated; a sharper open question is proposed.

---

## 2026-10-13: Run-1 survivors at 30×; run 2 pre-registered

- Scores for run 1 confirmed by the author.
- New dataset `chomp4_a3000_c60` (this project's solver, a ≤ 3000, c ≤ 60): 2,010,792 P-positions, identical to the author's independent n ≤ 3000 data on that range. The author's n ≤ 3000 CSV: 961,619,972 rows, SHA-256 `c08553c0…b1d8c`. Our solver reproduces it exactly for c ≤ 300 (47,986,319 positions).
- `overthink falsify --dataset-map` tests a run against another dataset.
- **Run-1 candidates re-tested at a ≤ 3000 (30× the a ≤ 100 window): 69 survived, 4 refuted (the same 4).** Each survivor was checked on 2,920–2,990 relations, out to b = 2,972–3,000 (extension 30–65× per sequence).
- Functional dependencies can now be emitted as conjectures (off by default). With the new code, run 1's frozen config reproduces run 1's 73 candidates exactly. 83 tests passing.
- Run 2 pre-registered: `experiments/rediscovery2/PROTOCOL.md`, `experiments/configs/mining/rediscovery2_chomp4.yaml`. Not blind.

---

## 2026-10-13: Rediscovery run 2 (not blind): results

Tag `rediscovery2-frozen` → `c33c7c1`; output in `702dc2f` (mining) and `c1b3b05` (falsification). Report: `experiments/rediscovery2/REPORT.md`.

- 1,546 sequences, 176 proposals: **167 survived, 9 refuted** at a ≤ 3000 (10×).
- All 4 functional dependencies (including Unique Extension) proposed and survived on 2,010,792 positions, as predicted. Found only in the non-blind sense.
- `a~b` survivors: 151 (run 1: 57). All 57 run-1 survivors get the same period in run 2. Still no second-order statements (longest run of consecutive groups with a proposal: 6; 12 needed).
- One refutation came late: (c, d) = (48, 46), period 1 from b ≥ 87, failed at b = 2181 (7× the window).
- Observation (AI-assisted, not pipeline output): every period found in runs 1–2, including re-proposals, is 2ᵏ or 3·2ᵏ (1 … 192), with no factor of 7.

---

## 2026-10-13: Literature check of the Chomp survivors

Report: `experiments/literature/REPORT.md`.
- The form of every periodicity survivor is covered by Byrnes's Poset Game Periodicity Theorem (INTEGERS 2003): for fixed lower rows, a − b is eventually periodic in b, or there are finitely many P-positions. The survivors are instances with specific parameters.
- Sun's 2004 thesis, Table 2.1 (4-row periods for 25 bottom-row pairs, c ≤ 9) vs our a ≤ 3000 data: finite/infinite 25/25, periods 10/10, starts 7/10. Three starts differ ((6,3), (6,4), (6,5)), unresolved; Sun's definition of the start is not precise.
- Independent validation: with d = 0 (3-row Chomp) our solver and miner reproduce all 9 published Brouwer/Nivasch (r, start, period) entries exactly, up to r = 6541 (period 9).
- **Retracted:** the "periods are 2ᵏ or 3·2ᵏ" observation from run 2. Counterexample: (c, d) = (6541, 0), period 9.
- Registry: 23 conjectures marked `known`, i.e. exact matches with Sun's table, Brouwer, Winning Ways, and Unique Extension (author's v2 Lemma 1). No novelty is claimed for the other survivors.
- Solver: optional `max_d` bound (max_d = 0 is exactly 3-row Chomp). Existing datasets regenerate byte-identically. 85 tests passing.

---

## 2026-10-13: Phase I, Lean 4 formalization

Lean v4.35.0, Mathlib v4.35.0 (`56a0058`). Details: `lean/README.md`. **No `sorry`, no `native_decide`**: every main theorem depends only on `propext`, `Classical.choice` and `Quot.sound`, checked by `lean/CheckAxioms.lean` and enforced in the new Lean CI workflow.

- **General theorems** (kernel-checked):
  - P-positions of a terminating game exist and are unique.
  - k-row Chomp terminates.
  - **Two valid P-positions of k-row Chomp that differ in at most one row are equal.**
  - Corollary: all four 4-row functional dependencies, including Unique Extension (author's v2 Lemma 1).
  - Subtraction games: periodicity follows from a finite window of max(S) values.
- **Pipeline conjectures proved for all n:** `uv run overthink prove` exported all 139 surviving subtraction-game periodicity conjectures. Counting aliases, that is 511 Lean theorems, one for every non-empty S ⊆ {1,…,9}. Each was proved by the finite-window lemma with the window evaluated by kernel `decide`. Build and axiom check took about 80 s.
  - A deliberately false period (S = {1,3,4}, p = 6) fails to compile.
- Registry: **143 conjectures `proved`** (139 subtraction periodicity + 4 Chomp functional dependencies; Unique Extension moves from `known` to `proved`). Totals: 143 proved, 368 survived, 22 known, 13 refuted (546).
- Not done: the Chomp periodicity survivors (a − b eventually periodic for fixed (c, d)) are not formalized. Unlike subtraction games, a finite window does not obviously suffice there; Byrnes's proof would be the starting point.

---

## 2026-10-13: Phase F (LLM proposer) and Phase H (new family: W(S))

- **Phase F built:** claim language (`conjecture/claims.py`: whitelisted expressions compiled to Polars; predicate / translation / statistic); LLM interface (`conjecture/llm.py`: window-only packets with SHA-256; mock, session and anthropic-stub providers; usage recorded); the falsifier tests claims on window and full data. No API key exists, so proposals come from the `session` provider: the project's AI assistant writes them in-session from the committed packet only.
- **Family H:** W(S), two heaps, removing s ∈ S from one heap or both; all 31 S ⊆ {1..5}, x, y < 1000 (`wsub_subsets5_n1000`, 31M Grundy values). Pre-registered (tag `familyH-frozen` → `13fc528`). Literature checked first: Larsson–Saha–Yokoo (arXiv:2307.12458) is the closest framework.
- **Classical miners:** 597 proposals (row periodicity of Grundy values plus 28 second-order); **597 survived** at 10×.
- **LLM (session) proposals:** 19 claims, none malformed; **19 survived** at 10×. Each was checked on 0.5M–4M positions. Together they give exact Grundy formulas for 13 sets and exact P-set characterizations for 13 more (26/31 sets), plus a region-restricted rule for {1,3,4}. Highlights:
  - (x+y) mod 3 when 1, 2 ∈ S and 3 ∤ s;
  - an explicit Grundy formula for every all-odd S containing 1;
  - the scaling W(kS) ≅ k² × W(S);
  - W({1..k}) ↔ Wythoff modulo k+1;
  - W({a,a+1}) with period 2a+1;
  - diagonal-split periodic P-sets.
- Falsifier sanity: three mutated LLM claims were all refuted (55k–2.7M counterexamples).
- Caveats and literature: `experiments/familyH/REPORT.md`. The W({1..k}) result may already be known (bounded Wythoff; to verify). No novelty is claimed. Next: Lean proofs of H01–H04.
