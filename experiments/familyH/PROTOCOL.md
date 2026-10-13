# Family H: Wythoff subtraction games W(S): pre-registered protocol

**Status: binding from the `familyH-frozen` tag on.** Requested by the author on 2026-10-13: "do a new game family … [the assistant] acts as the LLM", because the project has no API access and the grant is about AI for mathematics, not only compute and Lean.

## The family

W(S), for a finite set S of positive integers: two heaps (x, y); a move removes s ∈ S tokens from one heap, or s tokens from both heaps. Equivalently, the finite two-dimensional subtraction game with move vectors (s, 0), (0, s), (s, s), s ∈ S. Data: all 31 non-empty S ⊆ {1, …, 5}, Grundy values for x, y < 1000 (`wsub_subsets5_n1000`).

**Literature (checked before any data was looked at).** Larsson, Saha & Yokoo, *Subtraction games in more than one dimension* (arXiv:2307.12458) prove that two-dimensional finite subtraction games have outcomes that are eventually periodic along rows and columns. They solve two-move games, solve some three-move instances, and conjecture regular "mosaic" structure for others. Their abstract does not discuss Grundy values or Wythoff-type rulesets. Danai, Ellis & Thanatipanonda study nim-values of two-dimensional subtraction-*transfer* games. No source was found that treats W(S) specifically. A row-periodicity proposal is therefore expected to be an instance of the Larsson–Saha–Yokoo theorem (for outcomes), and novelty can only be judged after a literature check.

## Two proposers on the same window (x, y < 100)

1. **Classical miners**, with the same settings as rediscovery run 2: `experiments/configs/mining/familyH_wsub.yaml`.
2. **LLM proposer = the AI assistant in this session** (Claude Opus 5.5 in Claude Code; no API), through the `session` provider (`src/overthink/conjecture/llm.py`).

## Rules for the LLM proposer (fixed in advance)

- Its **only data source is the packet** written by `overthink llm-packet` from the proposal window: P-patterns for x, y < 48 and Grundy values for x, y < 12 for every S, plus the classical miners' proposals and the claim language. The packet's SHA-256 is committed before proposals are written, and the session provider refuses proposals for any other packet.
- It may not run code on the dataset, or read data beyond the packet, before its proposals are committed.
- At most **40 proposals**. Every proposal must be a machine-checkable claim. Statistical claims declare their tolerance in advance. All proposals are reported, including refuted ones and claims rejected as malformed.
- **Disclosed prior exposure:**
  - two solver sanity tests: S = {1} has P-positions exactly at x, y both even; taking every move size gives Wythoff;
  - the S = {1} Grundy values G(1,0) = 1, G(1,2) = 3 (from a corrected unit test);
  - the dataset's Parquet size (1.4 MB for 31M values), which hints at regular structure;
  - the literature above.

## Order of events (separate commits)

1. Tag `familyH-frozen` (code, configs, this protocol, dataset hash `3414dbb5f3ee4b76…`).
2. `overthink mine experiments/configs/mining/familyH_wsub.yaml --runs-dir experiments/familyH/run` → commit.
3. `overthink llm-packet … --mining-run <step-2 run> --out experiments/familyH/packet.md` → commit.
4. The assistant reads the packet and writes `experiments/familyH/llm_proposals.json` → commit.
5. `overthink llm-ingest … --provider session` and `overthink falsify` for both runs → commit.
6. `experiments/familyH/REPORT.md`, followed by a literature check of the survivors, then Lean where feasible.

## What is reported (fixed in advance)

For each proposer: proposals, rejected (malformed), refuted on window data, refuted on full data, survived, untestable. Which survivors the other proposer also found, and which statement forms only the LLM produced. Usage: packet size, approximate tokens, and API cost (0).
