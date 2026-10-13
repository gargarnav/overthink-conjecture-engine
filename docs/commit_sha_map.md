# Commit SHA map (history rewrites, 2026-10-13)

On 2026-10-13, before the repository was first published, its history was rewritten twice at the author's request, using `git filter-branch`:

1. Commit messages: an automatically added attribution trailer was removed.
2. Author and committer emails: the author's personal address was replaced with the GitHub no-reply address.

**Nothing else changed.** Each final commit has exactly the same tree (file contents) as the original, which was verified commit by commit. Author and committer dates were preserved. The annotated tag `rediscovery-frozen` was recreated on the corresponding commit (`1a99e9c`, originally `3e4aead`) with its original message and tagger date (2026-10-13 20:01:46 +0530).

Provenance recorded before the rewrites (dataset manifests, run outputs, registry events, `docs/results_log.md`) cites the **original** SHAs. Those records were not edited; use this table to translate. The tree hash proves the content is the same.

| Original SHA | Final SHA | Tree (unchanged) | Subject |
|---|---|---|---|
| `95a29e8f7fa8` | `a62e5a7b6432` | `e6ef42175445` | Rediscovery: mechanical candidate table and results-log entry for steps 1-3 |
| `320b8327c45e` | `23de9bfecc04` | `36ede7e1cfe1` | Rediscovery step 3: falsification at a <= 1000 (10x), unedited |
| `bbdd356a6cd7` | `3c9df5ff77a3` | `f64867d9e505` | Rediscovery step 2: raw mining output on 4-row Chomp (a <= 100), unedited |
| `3e4aeadd710a` | `1a99e9c8e8f3` | `a7792100e1d3` | Log Phase E, record dev conjectures in registry, finalize rediscovery protocol |
| `df862a5c7d16` | `c0c77b791da8` | `296edce83cc6` | Add falsifier and append-only conjecture registry |
| `866b6dd0b4b6` | `761d9d53cffb` | `8d3c5038a8db` | Add miner benchmark CLI, draft rediscovery pre-registration, log Phase D |
| `4f58c46ebd20` | `9e622afe8991` | `99d6580dc9c3` | Add generic dataset views and the mining run (overthink mine CONFIG) |
| `cbe08111dbef` | `c80e70133581` | `826bd937ce82` | Add classical conjecture miners, checker and synthetic benchmark |
| `d96413a86878` | `a6f0b89c705c` | `becc27b86897` | Generate and document canonical datasets (chomp4, wythoff, subtraction) |
| `1c73b5720703` | `9b7245ed9954` | `a6e330ad1cf6` | Add dataset generation: schemas, Parquet store, manifests, dataset cards |
| `3dfe59aa7708` | `1fa674a9f344` | `88ee989ecb19` | Log P-position count for n=500 (4,316,097), matching the paper's 4.3M+ figure |
| `fc2ce37bb6aa` | `bc14904ac528` | `5a425296ca6f` | Add 4-row Chomp cross-validation script and log Phase B results |
| `87e5112688c0` | `b27d19f5c9b7` | `bbcee753d147` | Add Python game wrappers, pure-Python oracles and solver tests |
| `bf3922762079` | `b079d588e487` | `615e8745b22f` | Add Rust solvers: subtraction games, Wythoff Grundy table, 4-row Chomp |
| `e1abbcb30f91` | `614f6e2252b8` | `6f3de78a7436` | Add author's reference C/C++ Chomp solvers as validation oracle |
| `ab412d811b63` | `6ca086599bda` | `86d99c1df01a` | Add CI workflow (Rust lint/tests, ruff, pytest on Linux and macOS) |
| `fe4e91ff5e90` | `67b4cc11e9fe` | `5709600f952c` | Add docs skeleton: architecture, methodology, results log, dataset/experiment/Lean/grant placeholders |
| `734c108c33a1` | `b35ffd09ec9f` | `2034b69b3340` | Add Python package, Rust core (PyO3) and CLI skeleton |
| `329f58261e11` | `c749edf9a448` | `85afaaa1d20f` | Add MIT license, citation metadata, README and gitignore |
