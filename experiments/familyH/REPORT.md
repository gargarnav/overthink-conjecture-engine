# Family H: Wythoff subtraction games W(S): report

Pre-registered in `PROTOCOL.md` (tag `familyH-frozen` → `13fc528`). Each step is a separate commit:

| Step | Commit |
|---|---|
| Classical mining output | `354085d` |
| LLM data packet (window only) | `fee2ec7` |
| LLM proposals, committed before any test | `f9020d9` |
| Ingestion and falsification of both | `186d49f` |

W(S): two heaps; a move removes s ∈ S from one heap or s from both. Data: all 31 non-empty S ⊆ {1,…,5}. Proposal window x, y < 100; falsification on x, y < 1000 (10× per axis, 100× the positions).

## Headline

| | Classical miners | LLM proposer (session) |
|---|---|---|
| Proposals | 597 | 19 (0 rejected as malformed) |
| Survived 10× falsification | **597** | **19** |
| Refuted (window / full data) | 0 / 0 | 0 / 0 |
| Statement forms | single Grundy rows: G(x, y + p) = G(x, y) for fixed x (569); how row periods and starts vary across rows (28) | exact Grundy formulas; exact characterizations of the whole 2D P-set; families of sets; a region-restricted rule |
| Sets with a statement about their whole 2D structure | 0 of 31 | **26 of 31** (exact), 1 partial |
| Positions checked per claim at full scale | ≈ 1,000 per row | 0.5M – 4M |

The LLM proposer is the AI assistant of this project session (Claude Opus 5.5 in Claude Code, no API). It worked from the 154,094-character packet (about 38.5k input tokens) and wrote 19 claims. API cost: $0.

**Sanity checks on the falsifier** (run after the proposals were committed): three deliberately mutated LLM claims were all refuted on the full data, with 55,444, 2,664,000 and 106,840 counterexamples respectively. The mutations were: drop the (3,5) pair from H07; replace (x+y) mod 3 by (x+2y) mod 3 in H02; widen H14's region to max ≥ 1.2·min.

## The LLM's conjectures (all survived on x, y < 1000)

| ID | Statement (short) | Sets | Positions checked |
|---|---|---|---|
| H01 | S all odd with 1 ∈ S: **G = 0 if x, y even; 2 if both odd; for mixed parity 1 if the odd coordinate is larger, else 3** | {1},{1,3},{1,5},{1,3,5} | 4,000,000 |
| H02 | 1, 2 ∈ S, no element ≡ 0 mod 3: **G = (x + y) mod 3** | {1,2},{1,2,4},{1,2,5},{1,2,4,5} | 4,000,000 |
| H03 | Scaling: **G_{s}(x, y) = G_{1}(⌊x/s⌋, ⌊y/s⌋)** | {2},{3},{4},{5} | 4 × 1,000,000 |
| H04 | Scaling: G_{2,4} = (⌊x/2⌋ + ⌊y/2⌋) mod 3 | {2,4} | 1,000,000 |
| H05–H07 | **W({1..k}): (x, y) is P iff (x mod (k+1), y mod (k+1)) is a Wythoff P-position** (k = 3, 4, 5; also {1,2,3,5}) | 4 sets | 5,000,000 |
| H08 | **W({a, a+1}): period 2a+1, P-set [0,a)² ∪ {(a,2a), (2a,a)}** mod 2a+1 (a = 2, 3, 4) | {2,3},{3,4},{4,5} | 3 × 1,000,000 |
| H09 | Period-7 P-set shared by {2,3,4,5} and {2,3,5} | 2 sets | 2,000,000 |
| H10 | Period-8 P-set of {3,5} | 1 | 1,000,000 |
| H11–H13 | P-sets periodic but **split by the diagonal**: P iff (min(x,y) mod m, max(x,y) mod m) ∈ A (m = 5, 6, 8) | {1,4},{2,3,4},{3,4,5} | 3 × 1,000,000 |
| H14 | {1,3,4}, **away from the diagonal (max ≥ 2 min)**: a period-7 rule; near the diagonal different | {1,3,4} | 500,999 |

Patterns across these, stated in the rationales: interval sets {a..b} have P-period a+b, matching the 1D game {a..b}, and W(kS) is k² copies of W(S). Not covered by any LLM claim: {1,3,4,5}, {1,4,5}, {2,4,5}, {2,5}, and the near-diagonal band of {1,3,4}. Their packet grids show irregular, slice-like ("mosaic") structure.

## What each proposer contributed

- **Only the LLM:** statements about the *whole* two-dimensional P-set or Grundy function; statements about *families* of sets (H01, H02, H03, H05–H08) with a reason; a region-restricted law (H14). The classical miners cannot express these forms.
- **Only the classical miners:** row-periodicity facts for the four sets the LLM left alone; exact preperiods for each row; cross-row statements such as "the start of row periodicity moves one step per row".
- **Overlap:** wherever the LLM gives an exact formula or P-set, the miners' row statements for that set follow from it (for P-sets), or are implied directly (Grundy formulas H01–H04).

## Proof status and next steps

- H01–H04 come with proof sketches in their rationales (parity case analysis, residues mod 3, isomorphism W(kS) ≅ k² × W(S)). They are the natural Lean targets and general proofs look within reach.
- H05–H13 are exactly periodic or diagonal-split periodic P-sets. A finite-window argument like the one used for 1D subtraction games may reduce them to finite checks, but that needs a 2D version of `periodic_of_window`.
- H14 is a genuine conjecture about a region boundary. The slope 2 was a guess; it holds up to 1000, but the true boundary is unknown.

## Literature and novelty (no claims made)

- Larsson, Saha & Yokoo, *Subtraction games in more than one dimension* (arXiv:2307.12458): outcomes of 2D finite subtraction games are eventually periodic along rows and columns, and several rulesets form periodic "mosaics". The H11–H14 structures look like instances of those mosaics. W({s}) has three moves, a class their abstract says is partly solved.
- **H05–H07 may be known.** A search summary claims that a survey describes the P-positions of a "bounded Wythoff's game" as translations of Wythoff's P-positions on a bounded board. That source was not identified: Ho (arXiv:1202.3186) does not contain it. The likely source is Duchêne, Fraenkel, Nowakowski & Rigo, *Extensions and restrictions of Wythoff's game preserving its P-positions*, JCTA 117 (2010). **TODO: check before any novelty claim.**
- H01 for S = {1} (P iff both even) is an elementary, standard exercise.

## Honest caveats

- The LLM proposer is the same AI assistant that built the pipeline. The packet-only rule was self-enforced. Its evidence is the committed packet hash, the session provider's hash check, and the commit order (proposals in `f9020d9` before ingestion and falsification in `186d49f`). Exposure before proposing is disclosed in `PROTOCOL.md`.
- Training knowledge (Wythoff pairs, the king game) shaped some proposals. That is part of what an LLM proposer is, but it means "survived" must not be read as "new".
- A clean 19/19 says the proposals were well founded on this data, not that they are true for all positions. Only proofs settle that.
