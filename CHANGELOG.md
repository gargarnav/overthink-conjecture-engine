# Changelog

All notable changes to this project. Dates are UTC. Results are recorded in detail in `docs/results_log.md`.

## [0.1.0]: 2026-10-14

### Added
- Exact solvers (Rust core): subtraction games, Wythoff, 4-row Chomp (validated against the author's independent data, brute force, and published 3-row tables), Wythoff subtraction games W(S).
- Datasets with cards, manifests and content hashes (Parquet; CC BY 4.0).
- Classical miners (periodicity, polynomial/quasi-polynomial, linear recurrence, floor-linear, OEIS matching), generic views, falsifier (≥10×), append-only conjecture registry and its open export.
- LLM proposer interface (mock / interactive session / API stub) with a checkable claim language.
- Lean 4 + Mathlib formalization: k-row Chomp one-row theorem; subtraction-game finite-window periodicity (511 generated theorems); Grundy formulas for W(S) families; P-positions of W({a, a+1}) for every a.
- Pre-registered experiments: blind 4-row Chomp rediscovery (run 1, run 2) and family H (classical vs LLM proposer).
- Reproducibility: `overthink run`, `make reproduce-demo`, Dockerfile; CI with tests, types, coverage, SPDX, secrets scan, Lean axiom check.
