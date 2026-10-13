"""Cross-validate the Rust 4-row Chomp solver against the author's reference C++ output.

usage: uv run python experiments/validate_chomp4.py [--n 1000] [--csv data_ref/p_positions_4xn_cpp_1000.csv]

The reference CSV has columns a,b,c,d,n with n == a. Both sets are encoded as uint64
keys, sorted, and compared exactly; any mismatches are printed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import polars as pl

from overthink.games.chomp import chomp4_p_positions


def keys(arr: np.ndarray, n: int) -> np.ndarray:
    m = np.uint64(n + 1)
    a, b, c, d = (arr[:, i].astype(np.uint64) for i in range(4))
    return np.sort(((a * m + b) * m + c) * m + d)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--csv", type=Path, default=Path("data_ref/p_positions_4xn_cpp_1000.csv"))
    args = ap.parse_args()

    t0 = time.perf_counter()
    ours = chomp4_p_positions(args.n)
    t_solve = time.perf_counter() - t0

    ref = pl.read_csv(args.csv).filter(pl.col("a") <= args.n)
    assert (ref["a"] == ref["n"]).all(), "reference: expected n == a"
    ref_arr = ref.select("a", "b", "c", "d").to_numpy().astype(np.uint32)

    k_ours, k_ref = keys(ours, args.n), keys(ref_arr, args.n)
    only_ours = np.setdiff1d(k_ours, k_ref, assume_unique=True)
    only_ref = np.setdiff1d(k_ref, k_ours, assume_unique=True)

    result = {
        "n": args.n,
        "ours_count": len(k_ours),
        "reference_count": len(k_ref),
        "only_in_ours": len(only_ours),
        "only_in_reference": len(only_ref),
        "identical": bool(np.array_equal(k_ours, k_ref)),
        "solve_seconds": round(t_solve, 2),
        "reference_sha256": sha256(args.csv),
        "git_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False
        ).stdout.strip(),
        "machine": f"{platform.machine()} {platform.platform()}",
    }
    print(json.dumps(result, indent=2))
    for name, ks in [("only_in_ours", only_ours), ("only_in_reference", only_ref)]:
        if len(ks):
            m = args.n + 1
            sample = [
                (int(k) // m**3, int(k) // m**2 % m, int(k) // m % m, int(k) % m) for k in ks[:10]
            ]
            print(name, "sample:", sample)


if __name__ == "__main__":
    main()
