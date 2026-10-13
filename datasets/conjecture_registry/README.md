# Dataset card: `conjecture_registry`

Every conjecture the Overthink pipeline has proposed, one row per conjecture, **including refuted ones**: failures are data. Generated from the append-only event log `registry/events.jsonl` by:

```bash
uv run overthink registry export
```

## Motivation

A benchmark of machine-proposed conjectures with explicit evidence and verification status. For each statement it records how it was proposed, on what data, how hard it was tested, whether it broke, and whether it was proved in Lean.

## Schema (`conjectures.parquet`, `conjectures.jsonl`)

| Column | Meaning |
|---|---|
| `id` | stable hash of (kind, sequence, parameters) |
| `statement` | natural-language statement |
| `statement_machine` | JSON: kind, sequence or table, parameters; checkable by `overthink.conjecture.checks` / `claims` |
| `game_family`, `dataset` | game family and dataset it was proposed from |
| `proposal_window` | JSON: data range used to propose it |
| `proposer`, `method` | `classical` (miner name@version) or `llm` (provider) |
| `falsification_datasets`, `falsification_checks` | datasets it was tested on, and number of individual checks |
| `counterexamples` | JSON list (index or row, observed vs predicted) |
| `proof_status` | `open`, `refuted`, `verified-finite` (survived a finite test; evidence, not proof), `proved-lean` |
| `lean_files`, `lean_theorems` | where the Lean proof is |
| `literature` | published source, when the statement is known |
| `proposed_at`, `last_event_at`, `proposal_run` | timestamps and run id |

## Reading the counts honestly

Many rows are instances of the same theorem. For example, 139 subtraction-game periodicity rows are all proved by one finite-window lemma. Most statements are known or elementary. See `docs/results/` and the dataset's own `literature` column. LLM model identifiers are kept in `registry/events.jsonl`; the export uses neutral provider labels.

## Known limitations

Proposal windows are small by design. `verified-finite` only means the statement survived the stated test.

## License and citation

CC BY 4.0 (`datasets/LICENSE`). Cite via `CITATION.cff`. DOI: TODO (first Zenodo release).
