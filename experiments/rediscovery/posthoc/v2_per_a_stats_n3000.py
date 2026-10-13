# SPDX-License-Identifier: MIT
"""Per-a statistics of d/a for a in [200, 3000] from the author's n <= 3000 data (Parquet in data_ref/)."""

import polars as pl

src = "data_ref/p_positions_4xn_cpp_3000.parquet"
parts = []
for lo in range(200, 3001, 100):
    hi = min(lo + 99, 3000)
    g = (
        pl.scan_parquet(src)
        .filter(pl.col("a").is_between(lo, hi))
        .with_columns((pl.col("d").cast(pl.Float64) / pl.col("a")).alias("r"))
        .group_by("a")
        .agg(
            pl.len().alias("n"),
            pl.col("r").median().alias("med"),
            pl.col("r").quantile(0.40).alias("q40"),
            pl.col("r").quantile(0.60).alias("q60"),
            pl.col("r").mean().alias("mean"),
            (pl.col("r") > 0.21).mean().alias("frac_above"),
            pl.col("r").min().alias("min"),
            pl.col("r").max().alias("max"),
            (pl.col("d") == 0).mean().alias("frac_d0"),
        )
        .collect()
    )
    parts.append(g)
t = pl.concat(parts).sort("a")
t.write_parquet("data_ref/v2_per_a_stats.parquet")
high = t["med"] > 0.21
print(f"a in [200,3000]: {t.height} values; HIGH (median > 0.21): {high.mean():.3%}")
print("medians in [0.194,0.235]:", t.filter(pl.col("med").is_between(0.194, 0.235)).height)
print(
    "HIGH iff more than half of the P-positions have d/a > 0.21:",
    (high == (t["frac_above"] > 0.5)).all(),
)
print(
    "frac(d/a > 0.21) per a: min {:.4f}  median {:.4f}  max {:.4f}".format(
        t["frac_above"].min(), t["frac_above"].median(), t["frac_above"].max()
    )
)
for col in ["q40", "q60", "mean"]:
    print(
        f"{col}: min {t[col].min():.4f}  max {t[col].max():.4f}; values in [0.194,0.235]: "
        f"{t.filter(pl.col(col).is_between(0.194, 0.235)).height} of {t.height}"
    )
row = t.filter(pl.col("a") == 3000).row(0, named=True)
print("a = 3000:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})
