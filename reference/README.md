# Reference implementations

The author's original C/C++ research code, written before this project for the 4×n Chomp paper. It's kept here as an **independent oracle**: the project's own solvers are re-implementations in Rust/Python and are validated against this code's output.

| File | What it is |
|---|---|
| `cpp/krow_brute.cpp` | Brute-force P/N solver for k-row Chomp |
| `cpp/rows4.cpp` | Fast per-(c,d)-pair solver for 4×n Chomp |
| `cpp/rows3_fast.cpp` | Fast solver for 3×n Chomp |
| `cpp/sealed/` | Analysis code that encodes structural hypotheses. **Sealed under the blind rediscovery protocol** (`docs/methodology.md` §4): not read or used by the pipeline until the `rediscovery-frozen` tag exists. |

Reference dataset: `p_positions_4xn_cpp_1000.csv`, i.e. all P-positions (a,b,c,d) of 4-row Chomp with a ≤ 1000, produced by the author's C++ solver. It has 35,029,679 rows and SHA-256 `b907bd55a891a60c5141498e9b44af75a19517aec2185a18c6de8cb7aa188f5f`. It's too large for git: put it at `data_ref/p_positions_4xn_cpp_1000.csv` locally. *(TODO: host alongside the project datasets.)*

Conventions used in this code and the project: row lengths a ≥ b ≥ c ≥ d ≥ 0 with a ≥ 1. Square (0,0) is the poison and can't be taken, so the single-square position (1,0,0,0) is terminal and therefore a P-position.

Second reference dataset (author's v2 solver): `p_positions_4xn_cpp_3000.csv`, i.e. all P-positions with a ≤ 3000. It has 961,619,972 rows (22,521,795,640 bytes) and SHA-256 `c08553c0ec9bf60c43ed1b0fe43467968aed79465fc9e69d750bdef8baeb1d8c`. It's too large for git; available from the author. This project's solver reproduces it exactly for c ≤ 300: 47,986,319 positions (see `docs/results_log.md`).
