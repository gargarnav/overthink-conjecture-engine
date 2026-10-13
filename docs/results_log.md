# Results log

Dated, append-only record of what actually worked and what failed. Newest entries at the bottom. This file is the source of truth for any number cited in papers or grant materials.

---

## 2026-10-13: Phase A, repository scaffold

**Done**
- Repository created: MIT license, CITATION.cff, README, docs skeleton.
- Python package `overthink` (Python 3.12, uv) with a Rust core `overthink._core` built via maturin/PyO3 0.29.
- Rust core currently exposes only `mex` (minimum excludant) and `core_version`, as a build/integration smoke test.
- CLI: `overthink info`, `overthink --help`.
- Tests: 9 pytest + 3 cargo tests passing locally (macOS arm64, Apple M4). Ruff, rustfmt and clippy clean.

**Not done / notes**
- No solvers, data, miners or conjectures yet. No mathematical results to report.
- Lean toolchain not yet installed (planned for Phase I).
- Repo is local only; no public GitHub remote yet.

---

## 2026-10-13: Phase B, exact solvers

**Done**
- Rust solvers (`rust/src/`): subtraction-game Grundy values, Wythoff Grundy table, and 4-row Chomp P-positions (per-(c,d)-pair algorithm, parallel over anti-diagonals, exact under truncation a ≤ max_a).
- Pure-Python definitional oracles in `src/overthink/games/` (brute-force k-row Chomp, Wythoff, subtraction games).
- Test suite: 38 pytest + 8 cargo tests passing. Checks against brute force (4-row Chomp n ≤ 20, 3-row n ≤ 20, Wythoff 40×40, eight subtraction sets to 500) and known theorems (2-row Chomp P-positions = (b+1, b); every rectangle with ≥ 2 squares is N; Wythoff P-positions = Beatty pairs, checked on 1000×1000; S = {1,2,..,k} gives n mod (k+1); S = {1,3,4} has period 7).

**4-row Chomp validation**

| Check | Independent of the fast algorithm? | n | P-positions | Result |
|---|---|---|---|---|
| Our fast solver vs Python brute force (definition) | yes | 40 | 2,770 | identical |
| Our fast solver vs author's `krow_brute.cpp` (definition) | yes | 120 | 59,501 | identical |
| Our fast solver vs author's `rows4.cpp` output (`p_positions_4xn_cpp_1000.csv`, SHA-256 `b907bd55…88f5f`) | **no**: same algorithm, independently re-implemented | 1000 | 35,029,679 | identical |

The n = 1000 run took 53 s wall time on an Apple M4 (10 cores) with about 7 GB peak RSS, including loading the CSV. Reproduce with `uv run python experiments/validate_chomp4.py`.

**P-position counts (4-row Chomp, all positions with a ≤ n)**
- n = 500: 4,316,097 (our solver and the reference CSV agree). This is the "4.3M+" figure in the author's paper, as the author confirmed on 2026-10-13.
- n = 1000: 35,029,679.

**Blind-protocol exposure disclosure (methodology §4)**
Before any miner was written, the agent building this was exposed to:
(1) comments in `reference/cpp/rows4.cpp` stating solver-level game facts (a diagonal P-position (x,x,c,d) makes every larger b in that pair N; a constant P-position makes a whole pair N);
(2) a comment in `reference/cpp/rows3_fast.cpp` mentioning a "mean eventual shift" for live rows in 3-row Chomp;
(3) three truncated lines of `reference/cpp/sealed/rows4_fast.cpp`, shown by a keyword search, indicating the author studied eventual periodicity of `delta(b) = a − b`.
The periodicity miner was planned before this exposure (Step 0 plan, same date). The sealed files have not been read. The ground-truth statements have not been seen.

---

## 2026-10-13: Phase C, datasets

**Done**
- `overthink generate CONFIG` → `data_out/<id>/data.parquet` (zstd) plus a tracked `datasets/<id>/` holding an auto-generated dataset card, `manifest.json` (params, schema version, row count, hashes, git SHA, library versions, timing) and `sample.parquet`.
- `overthink verify ID` checks a dataset's content hash against its tracked manifest.
- Schema v1.0 is defined once in `src/overthink/data/schema.py`.
- 11 new tests (49 pytest total): schema conformance, canonical sort, determinism, round-trip, tamper detection, CLI, and the chomp4 dataset vs brute force at n = 15.

**Datasets generated** (Apple M4, git `1c73b57`)

| Dataset | Rows | Parquet size | Generation time |
|---|---|---|---|
| `chomp4_n1000` | 35,029,679 | 50.1 MB (the reference CSV is 686 MB) | 51 s |
| `wythoff_n1000` | 1,000,000 | 1.4 MB | 2.9 s |
| `subtraction_subsets9_n2000` | 1,022,511 | 0.3 MB | 0.1 s |

**Reproducibility check:** regenerating `chomp4_n1000` into a separate directory gave an identical `content_sha256` and an identical `file_sha256`, so the Parquet file is byte-identical on the same machine and library versions. Cross-machine byte identity hasn't been tested; `content_sha256` is the hash meant to be portable.

**Not done**
- Full datasets are not hosted publicly yet (Hugging Face/Zenodo TODO).
- Data license CC BY 4.0 is proposed, not confirmed.
