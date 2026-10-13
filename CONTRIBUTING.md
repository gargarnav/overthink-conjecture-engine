# Contributing

Contributions are welcome: new game families and solvers, miners, falsification checks, Lean proofs, and literature pointers (especially "this is already known, see …").

## Ground rules

1. **No unverified claims.** A conjecture is reported as surviving only after it has been tested on at least 10× more data than it was proposed from, and as proved only when a Lean proof compiles with standard axioms (no `sorry`, no `native_decide`).
2. **Refutations are kept.** Never delete registry events; the registry (`registry/events.jsonl`) is append-only.
3. **Pre-registered experiments are frozen.** Do not edit files under a pre-registered experiment after its tag (e.g. `rediscovery-frozen`, `familyH-frozen`). Fixes go into a new, separately tagged run.
4. **Reproducible from one command.** New experiments get a config under `experiments/configs/` and run with `overthink run`.

## Development

```bash
uv sync                      # Python 3.12 + Rust core
make test lint               # pytest, cargo test, ruff, SPDX headers
uv run mypy                  # type check
make lean                    # Lean build + axiom check (downloads Mathlib cache, ~7 GB)
make reproduce-demo          # headline result, end to end
```

Every source file starts with an SPDX header (`# SPDX-License-Identifier: MIT`). Code is MIT; data is CC BY 4.0. By contributing you agree your contribution is licensed under these terms.

## Pull requests

Keep them small and focused. Include tests, and update `docs/results_log.md` if your change produces or changes a result. Use the PR template checklist.
