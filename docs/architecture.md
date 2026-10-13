# Architecture

```
          ┌────────────┐   Parquet    ┌──────────────┐  candidates  ┌───────────┐
config ──▶│  games/    │─────────────▶│ conjecture/  │─────────────▶│ registry/ │
 (YAML)   │  solvers   │   data/      │ miners + LLM │              │ JSONL log │
          └────────────┘              └──────────────┘              └─────┬─────┘
                ▲                                                         │
                │ larger instances                                        ▼
          ┌─────┴──────┐  counterexamples / survived              ┌───────────┐
          │ falsify/   │◀─────────────────────────────────────────│  prove/   │
          │ 10× scale, │─────────────────────────────────────────▶│ Lean 4    │
          │ OEIS check │        survivors                         │ export    │
          └────────────┘                                          └───────────┘
```

## Language split

- **Rust (`rust/`, exposed as `overthink._core`)**: hot loops only, i.e. exact solvers for large state spaces such as 4×n Chomp. Pure-Rust functions are unit-tested with `cargo test`; thin `#[pyfunction]` wrappers expose them.
- **Python (`src/overthink/`)**: orchestration, data I/O, miners, registry, LLM interface and CLI. Small games may have pure-Python reference solvers, which double as test oracles for the Rust versions.

## Modules

| Module | Responsibility | Phase |
|---|---|---|
| `games/` | Game definitions, exact solvers, known-value tests | B |
| `data/` | Dataset generation from config, Parquet schema, content hashing | C |
| `conjecture/` | Periodicity, recurrence, difference-table and floor-linear miners; OEIS snapshot matching; LLM proposer behind a provider interface (mock by default) | D, F |
| `falsify/` | Re-testing at ≥10× scale, counterexample search, literature/OEIS checks | E |
| `registry/` | Append-only conjecture records with provenance (see `methodology.md`) | E |
| `prove/` | Export survivors as Lean statements, run `lake build`, record proof method | I |

## Build

`uv sync` builds the Rust extension with maturin. `[tool.uv] cache-keys` in `pyproject.toml` makes uv rebuild whenever a `.rs` file changes.
