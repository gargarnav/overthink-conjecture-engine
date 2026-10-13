# Overthink Conjecture Engine

A falsification-first discovery loop for combinatorial game theory.

1. **Compute**: exact datasets of positions and values (P/N, Grundy values) for families of impartial games.
2. **Conjecture**: mine the data for structure (periodicity, recurrences, closed forms, OEIS links) with classical methods and an optional LLM proposer.
3. **Overthink**: try hard to break every conjecture: test on instances at least 10× larger, search for counterexamples, check against known literature and OEIS, and record every failure.
4. **Prove**: formalize surviving statements in Lean 4 + Mathlib, starting with finite cases.
5. **Record**: every conjecture, with its evidence, counterexamples, proof status and full provenance, goes into an open dataset.

The project goes deep on one underexplored area (combinatorial games). It is not a general AI mathematician, and it does not try to compete with those efforts.

## Status

Early development. See [`docs/results_log.md`](docs/results_log.md) for a dated record of what has actually worked and failed. Nothing is claimed here that isn't in that log.

| Component | Status |
|---|---|
| Repository scaffold, Rust↔Python core | Done (Phase A) |
| Exact solvers (subtraction, Wythoff-type, 4×n Chomp) | TODO (Phase B) |
| Parquet datasets + schema | TODO (Phase C) |
| Classical pattern miners | TODO (Phase D) |
| Conjecture registry + falsifier | TODO (Phase E) |
| LLM proposer (optional, mock by default) | TODO (Phase F) |
| Blind rediscovery test on 4×n Chomp | TODO (Phase G) |
| Lean 4 formalization | TODO (Phase I) |

## Quickstart

Requirements: [uv](https://docs.astral.sh/uv/) and a Rust toolchain (`rustup`). The Rust core is compiled automatically on first sync.

```bash
uv sync
uv run overthink info
uv run pytest
```

## Repository layout

```
src/overthink/   Python package
  games/         game definitions + exact solvers
  data/          dataset generation, Parquet storage, schema
  conjecture/    pattern miners + LLM proposer
  falsify/       scale-up testing, counterexample search, literature/OEIS check
  prove/         Lean export + proof attempt orchestration
  registry/      conjecture registry with full provenance
rust/            performance-critical core (PyO3 extension: overthink._core)
lean/            Lean 4 + Mathlib project
datasets/        dataset cards + small samples (large data hosted separately)
experiments/     reproducible run configs, reports
docs/            architecture, methodology, results log
grant/           grant application drafts
tests/
```

## Openness

- Code: MIT ([LICENSE](LICENSE)).
- Data: open, with dataset cards, schema and reproduction commands (see [`datasets/`](datasets/)).
- Papers: arXiv preprints.

## Citation

See [CITATION.cff](CITATION.cff).
