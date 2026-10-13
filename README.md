# Overthink Conjecture Engine

[![CI](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/ci.yml)
[![Lean](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/lean.yml/badge.svg)](https://github.com/gargarnav/overthink-conjecture-engine/actions/workflows/lean.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](datasets/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23350597.svg)](https://doi.org/10.5281/zenodo.23350597)

**A falsification-first discovery loop for combinatorial game theory.** The system:

1. computes exact game data;
2. proposes conjectures with classical miners and an AI proposer;
3. tries hard to break every conjecture on at least 10× more data;
4. proves survivors in Lean 4;
5. keeps every conjecture, including the failures, in an open registry.

The project goes deep on one area, impartial games. It is not a general AI mathematician and does not try to compete with those efforts.

## Results so far

Every number below is in [`docs/results_log.md`](docs/results_log.md). Current totals are in [`docs/metrics.md`](docs/metrics.md).

- **One result that may be new**, proved for every parameter. The P-positions of the two-heap game W({a, a+1}) (remove a or a+1 from one heap or both) are periodic modulo 2a+1: an a×a square plus the points (a, 2a) and (2a, a). The AI proposer found it from cases a ≤ 4; it was falsified on 3M positions and proved in Lean for all a. The proof is elementary once the statement is known, and novelty is pending specialist review. See [write-up](docs/results/W_pair_theorem.md).
- **Falsification corrected published conjectures.** Applied to the author's own 4×n Chomp paper (arXiv:2604.25952), the same falsification-first checks showed:
  - one conjecture is false as literally stated;
  - the "period-112" signal is not supported by a modulus control;
  - the paper's v2 HIGH/LOW split is exactly "some P-position has d > 0.45a".
  
  See the [report](experiments/rediscovery/REPORT.md).
- **AI proposer vs classical miners** (pre-registered, [family H](experiments/familyH/REPORT.md)). On 31 two-dimensional subtraction games the classical miners described no game's 2D structure, while 19 AI proposals, committed before testing, characterized 26/31. All 19 survived 10× falsification; 10 are now Lean theorems.
- **Honest negative.** In a blind, pre-registered test, the classical miners rediscovered **0 of 4** of the author's published 4×n Chomp conjectures (statement forms they cannot express). [Protocol](experiments/rediscovery/PROTOCOL.md), [report](experiments/rediscovery/REPORT.md).
- **Verified computation.** The 4-row Chomp solver matches the author's independent data exactly (all 35M P-positions with a ≤ 1000, and the 48M of the 961M with a ≤ 3000 and c ≤ 300), brute force, Sun's 2004 four-row periods (10/10), and all 9 published Brouwer–Nivasch three-row periods up to r = 6541.

Most proved statements are known or elementary (see the [literature check](experiments/literature/REPORT.md)). The registry counts instances, not distinct theorems.

## Quickstart

Requirements: [uv](https://docs.astral.sh/uv/) and a Rust toolchain. Or use Docker (`docker build -t overthink .`).

```bash
uv sync                                   # Python 3.12 + compiled Rust core
make test                                 # pytest + cargo test
make reproduce-demo                       # blind Chomp run, end to end (~90 s), compared with the committed result
uv run overthink run experiments/configs/ci_demo.yaml   # small generate -> mine -> falsify
uv run overthink stats                    # project metrics
```

Lean proofs: `make lean` (downloads the Mathlib cache, about 7 GB).

## Repository layout

```
src/overthink/   games/ (solvers) · data/ (datasets) · conjecture/ (miners, AI proposer, claims)
                 falsify/ · prove/ (Lean export) · registry/ (append-only log + export)
rust/            performance-critical core (PyO3)
lean/            Lean 4 + Mathlib proofs
datasets/        dataset cards, manifests, samples, conjecture registry export
experiments/     configs, pre-registered experiments and their reports
docs/            methodology, results log, metrics, costs, grant compliance
```

## Documentation

[Methodology](docs/methodology.md) · [Architecture](docs/architecture.md) · [Results log](docs/results_log.md) · [AI usage](AI_USAGE.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md) · [Publishing datasets](datasets/PUBLISHING.md)

## Openness

Code: MIT ([LICENSE](LICENSE)). Data: CC BY 4.0 ([datasets/LICENSE](datasets/LICENSE)). Third-party licenses: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Papers will be posted on arXiv.

## Funding

No external funding at present. (The acknowledgment text for any future grant lives in `funding.yaml` and is only rendered when `funded: true`.)

## Citation

Arnav Garg, *Overthink Conjecture Engine* (ORCID [0009-0009-2362-1903](https://orcid.org/0009-0009-2362-1903)). DOI [10.5281/zenodo.23350597](https://doi.org/10.5281/zenodo.23350597) (all versions; v0.1.0: [10.5281/zenodo.23350598](https://doi.org/10.5281/zenodo.23350598)). See [CITATION.cff](CITATION.cff).
