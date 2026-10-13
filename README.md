# Overthink Conjecture Engine

[![CI](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/ci.yml)
[![Lean](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/lean.yml/badge.svg)](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/lean.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](datasets/LICENSE)

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
| Exact solvers (subtraction, Wythoff, 4×n Chomp) | Done (Phase B): 4×n Chomp reproduces all 35,029,679 reference P-positions for n ≤ 1000 |
| Parquet datasets + schema | Done (Phase C): 3 datasets, one command each, hash-verified ([datasets/](datasets/)) |
| Classical pattern miners | Done (Phase D): 5 miners, synthetic benchmark, Wythoff's theorem recovered from data |
| Conjecture registry + falsifier | Done (Phase E): 297 dev conjectures, all survived 10× re-testing |
| LLM proposer (optional, mock by default) | Done (Phase F): claim language, window-only packets, mock/session/API providers |
| New game family | Done (Phase H): W(S) Wythoff subtraction games. Classical 597/597 and LLM 19/19 proposals survived 10×; LLM claims characterize 26/31 sets exactly ([report](experiments/familyH/REPORT.md)) |
| Blind rediscovery test on 4×n Chomp | Done: run 1 (blind) 0/4 v1 conjectures found, 69 exact statements survived at 30×; run 2 (not blind) 167/176 survived. See [experiments/rediscovery/REPORT.md](experiments/rediscovery/REPORT.md) |
| Lean 4 formalization | Done (Phase I): general theorems for k-row Chomp (incl. Unique Extension), 511 pipeline-proposed subtraction-game periodicity theorems, 7 LLM-proposed W(S) Grundy formulas, and a classification of the P-positions of W({a,a+1}) for every a ([write-up](docs/results/W_pair_theorem.md)), all kernel-checked, no `sorry`/`native_decide` ([lean/](lean/README.md)) |

## Quickstart

Requirements: [uv](https://docs.astral.sh/uv/) and a Rust toolchain (`rustup`). The Rust core is compiled automatically on first sync.

```bash
uv sync
uv run overthink info
uv run pytest
uv run overthink generate experiments/configs/datasets/*.yaml   # ~1 min
uv run overthink verify chomp4_n1000 wythoff_n1000 subtraction_subsets9_n2000
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

## Funding

No external funding at present. (The acknowledgment text for any future grant lives in
`funding.yaml` and is only rendered when `funded: true`.)

## Citation

See [CITATION.cff](CITATION.cff).
