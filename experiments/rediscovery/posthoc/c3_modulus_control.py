"""Checks of the v1 conjectures on chomp4_n1000 (a <= 500 for C3, as in the paper). Run from the repo root."""

import numpy as np
import polars as pl

N = 500
p = pl.read_parquet("data_out/chomp4_n1000/data.parquet").filter(pl.col("a") <= N)
# enumerate all triples a >= b >= c >= 0, 1 <= a <= N, and label extending ones via a sorted key
rows = []
for a in range(1, N + 1):
    b = np.repeat(np.arange(a + 1), np.arange(a + 1) + 1)
    c = np.concatenate([np.arange(bb + 1) for bb in range(a + 1)])
    rows.append(np.stack([np.full(len(b), a), b, c], 1))
T = np.concatenate(rows).astype(np.int64)
key = lambda x: (x[:, 0] * 1001 + x[:, 1]) * 1001 + x[:, 2]
ext = np.sort(key(p.select("a", "b", "c").to_numpy().astype(np.int64)))
lab = np.isin(key(T), ext).astype(np.int64)
amb, c = T[:, 0] - T[:, 1], T[:, 2]


def cmi(feature):  # I(lab; feature | c) in millibits, vectorised from cell counts
    k = c * (feature.max() + 1) + feature
    n1 = np.bincount(k, weights=lab)
    n = np.bincount(k).astype(float)
    nc = np.bincount(c).astype(float)
    n1c = np.bincount(c, weights=lab)

    def h(x, tot):
        q = np.divide(x, tot, out=np.zeros_like(x), where=tot > 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            return -(
                np.where(q > 0, q * np.log2(q), 0) + np.where(q < 1, (1 - q) * np.log2(1 - q), 0)
            )

    N_ = len(lab)
    return 1000 * ((nc * h(n1c, nc)).sum() - (n * h(n1, n)).sum()) / N_


print("I(extends ; (a-b) mod m | c), millibits, for m near 112 and 56:")
print("  " + "  ".join(f"{m}:{cmi(amb % m):.1f}" for m in [54, 55, 56, 57, 58]))
print(
    "  "
    + "  ".join(f"{m}:{cmi(amb % m):.1f}" for m in [108, 109, 110, 111, 112, 113, 114, 115, 116])
)
ranks = sorted(range(100, 125), key=lambda m: -cmi(amb % m))
print("  rank of 112 among moduli 100..124:", ranks.index(112) + 1, " top 5:", ranks[:5])
print("control, a-b cut into m contiguous intervals (no periodicity):")
for m in [56, 112, 224]:
    print(f"  m={m}: {cmi(np.minimum(amb * m // (N + 1), m - 1)):.1f}")
print("control, the exact value of a-b:", f"{cmi(amb):.1f}")
