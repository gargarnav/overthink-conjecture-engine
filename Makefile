# SPDX-License-Identifier: MIT
.PHONY: setup test lint lean reproduce-demo ci-demo stats costs docs

setup:            ## install the environment (Python 3.12, Rust core)
	uv sync

test:             ## Python and Rust tests
	uv run pytest -q
	cd rust && cargo test -q

lint:
	uv run ruff check . && uv run ruff format --check . && uv run python scripts/check_spdx.py

lean:             ## build and axiom-check the Lean proofs
	cd lean && lake exe cache get && lake build && lake env lean CheckAxioms.lean

reproduce-demo:   ## regenerate the blind 4-row Chomp rediscovery and compare with committed outputs
	uv run overthink run experiments/configs/reproduce_demo.yaml

ci-demo:          ## small end-to-end pipeline (as run in CI)
	uv run overthink run experiments/configs/ci_demo.yaml

stats:
	uv run overthink stats

costs:
	uv run overthink costs
