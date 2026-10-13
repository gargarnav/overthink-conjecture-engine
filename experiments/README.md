# Experiments

Each experiment is reproducible from one command and one config:

```bash
uv run overthink generate experiments/configs/datasets/<name>.yaml   # datasets
# uv run overthink run experiments/configs/<name>.yaml            # pipeline runs (Phase E)
```

- `configs/`: tracked YAML configs.
- `runs/`: run outputs (git-ignored; each run records its command, config, git SHA and seed).
- `<experiment>/REPORT.md`: tracked write-ups of finished experiments, e.g. `rediscovery/REPORT.md`.
