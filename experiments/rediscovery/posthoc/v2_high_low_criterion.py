"""HIGH/LOW (per-a median of d/a > 0.21) vs. the largest d/a among P-positions with first row a.

Needs data_ref/v2_per_a_stats.parquet (from v2_per_a_stats_n3000.py) and
data_ref/p_positions_4xn_cpp_3000.parquet (the author's n <= 3000 data converted to Parquet).
"""
import numpy as np
import polars as pl

t = pl.read_parquet("data_ref/v2_per_a_stats.parquet").with_columns((pl.col("med") > 0.21).alias("high"))
for thr in [0.45, 0.5, 0.6]:
    print(f"HIGH vs (max d/a > {thr}): agreement {(t['high'] == (t['max'] > thr)).mean():.2%}")
print(t.group_by("high").agg(pl.col("max").min(), pl.col("max").max().alias("max_hi"),
                             pl.col("n").median().alias("median count")).sort("high"))
src = "data_ref/p_positions_4xn_cpp_3000.parquet"
edges = np.round(np.arange(0.0, 0.46, 0.025), 3)
for a in [2999, 3000]:
    d = pl.scan_parquet(src).filter(pl.col("a") == a).select("d").collect()["d"].to_numpy() / a
    h, _ = np.histogram(d, bins=edges)
    print(f"a={a}: n={len(d):,} median {np.median(d):.4f} share d/a>0.45: {(d > 0.45).mean():.1%}")
    print("   " + " ".join(f"{lo:.3f}:{x / len(d):5.1%}" for lo, x in zip(edges[:-1], h)))
