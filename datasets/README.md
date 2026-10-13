# Datasets

Each dataset is produced by one command from a config in `experiments/configs/datasets/`. Its directory here holds a tracked **dataset card** (`README.md`), a **manifest** with provenance and hashes (`manifest.json`), and a small **sample** (`sample.parquet`). The full `data.parquet` is written to `data_out/<id>/`, which is git-ignored. *(TODO: host full files on Hugging Face Datasets, with a Zenodo DOI at release.)*

| Dataset | Family | Rows | Parquet | Card |
|---|---|---|---|---|
| `chomp4_n1000` | 4-row Chomp P-positions, a ≤ 1000 | 35,029,679 | 50 MB | [card](chomp4_n1000/README.md) |
| `wythoff_n1000` | Wythoff Grundy values, x, y < 1000 | 1,000,000 | 1.4 MB | [card](wythoff_n1000/README.md) |
| `subtraction_subsets9_n2000` | Subtraction-game Grundy values, all 511 sets S ⊆ {1..9}, n ≤ 2000 | 1,022,511 | 0.3 MB | [card](subtraction_subsets9_n2000/README.md) |

## Regenerate and verify

```bash
uv run overthink generate experiments/configs/datasets/*.yaml   # ~1 min on Apple M4
uv run overthink verify chomp4_n1000 wythoff_n1000 subtraction_subsets9_n2000
```

`verify` recomputes each dataset's `content_sha256` and compares it to the tracked manifest. That hash is taken over the canonically sorted values, so it doesn't depend on the Parquet writer or library version.

## Schema

Column definitions live in [`src/overthink/data/schema.py`](../src/overthink/data/schema.py) (schema version 1.0) and are copied into each card. Any change to a column bumps the schema version.

## License

Data: CC BY 4.0 *(proposed; TODO confirm before first public release)*. Code: MIT.
