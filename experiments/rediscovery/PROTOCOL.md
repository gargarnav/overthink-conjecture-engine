# Blind rediscovery of 4×n Chomp structure: pre-registered protocol

**Status: binding from the `rediscovery-frozen` tag on.** Approved by the author on 2026-10-13: falsifier built before freezing, proposal window a ≤ 100, no OEIS lookup.

## Question

Without access to the author's conjectures, does the classical pipeline independently propose the structural conjectures about 4×n Chomp P-positions from the author's paper? And are its proposals true when tested on 10× more data?

## What is frozen at the tag

1. The code in `src/overthink/` (views, miners, selection rules, checker, falsifier, registry).
2. The run config `experiments/configs/mining/rediscovery_chomp4.yaml`. Its `views`, `miners` and `second_order` sections are identical to the development config `dev_subtraction_wythoff.yaml`, which was developed on synthetic data, subtraction games and Wythoff's game only.
3. The dataset `chomp4_n1000`, identified by `content_sha256 a3fd877c39bb5b9ec1ea4519e157b1c84574f82e09ff5d08db4aeab4935166eb`.
4. This protocol, including the scoring rules below.

## Order of events (each step is a separate git commit)

1. **Tag** `rediscovery-frozen`.
2. **Mine:** run `uv run overthink mine experiments/configs/mining/rediscovery_chomp4.yaml` (proposal window a ≤ 100). Commit the raw output (`candidates.jsonl`, `sequences.jsonl`, `run.json`, `summary.md`) to `experiments/rediscovery/run/` unedited.
3. **Falsify:** run `uv run overthink falsify <run dir>` (frozen code in `src/overthink/falsify/falsifier.py`). It rebuilds the same views on the full dataset (a ≤ 1000) and applies the rule in `docs/methodology.md` §1:
   - A candidate is tested on its sequence and all aliases.
   - It is *refuted* if it fails on any of them, and *survives* if it holds on all of them (first-order sequences must have new terms).
   - Second-order statements are checked against parameters re-estimated by the same miners on the full data.
   - Anything else is *untestable*.

   Commit the output unedited.
4. **Ground truth:** only now does the author commit `experiments/rediscovery/ground_truth.md`, containing the paper's structural conjectures verbatim, with the citation.
5. **Score:** write `REPORT.md`.

No code or config change between steps 1 and 3 is allowed. If a bug is found, it is fixed in a new commit, the whole run is repeated from step 1 under a new tag (`rediscovery-frozen-v2`), and both runs are reported.

## Scoring (step 5)

Each ground-truth statement G is scored as one of:

- **Found:** a surviving candidate, or a set of surviving candidates of one family (e.g. one per group), states G or something logically equivalent to G over G's whole scope.
- **Partial:** surviving candidates state G for part of its scope (e.g. some groups but not all), state a weaker consequence of G, or state G's form with different parameters that coincide with G only on the observed range.
- **Missed:** nothing in the output corresponds to G.

Separately, the report lists:

- **Wrong:** candidates that contradict G, and surviving candidates later shown false by any further check.
- **Refuted proposals:** count, with examples. These are expected by design and are not errors of the system, but they are reported.
- **Other survivors:** surviving candidates that don't correspond to any G. These are candidates for new observations, to be checked by the author against the paper and the literature before any claim of novelty.

Scoring is done by the author, and each decision has a one-line justification quoting the matching candidate IDs. Where scoring needs judgement (equivalence, scope), the reasoning is written out. Proposed scores by the AI assistant are labelled as such.

## Known limitations, stated in advance

- The person who built the miners saw some solver-level facts and a hint about the kind of structure studied (see the `docs/results_log.md` Phase B entry, "Blind-protocol exposure disclosure"). The periodicity miner was planned before that exposure.
- The miners only express four families of statements (eventual additive periodicity, quasi-polynomials, linear recurrences, floor-linear) about single sequences, plus the same applied to period parameters across groups. Any ground-truth statement of another form can only be **missed** or **partial**. That is a limitation of the miners, not evidence against the statement.
- Proposals use a ≤ 100 only. Structure that appears only at larger a cannot be found.
- No LLM is used in this run. A separate LLM run, if any, is reported separately because of possible training-data contamination.
- No OEIS snapshot is used in this run.
