"""Checks of the v1 conjectures on chomp4_n1000 (a <= 500 for C3, as in the paper). Run from the repo root."""

import numpy as np
import polars as pl

df = pl.read_parquet("data_out/chomp4_n1000/data.parquet")

print("== C1: max number of d per (a,b,c):", df.group_by("a", "b", "c").len()["len"].max())

print("\n== C2: ratio distribution among P-positions with first row a")
for lo, hi in [(450, 500), (950, 1000)]:
    w = df.filter((pl.col("a") >= lo) & (pl.col("a") <= hi))
    for col in "bcd":
        r = w[col] / w["a"]
        print(
            f"  a in [{lo},{hi}] {col}/a: min {r.min():.3f}  q10 {r.quantile(0.1):.3f}  median {r.median():.4f}  q90 {r.quantile(0.9):.3f}  max {r.max():.3f}"
        )
print(
    "  literal-statement check, family (a, a-1, 0, 0) is P for every a:",
    all(
        df.filter((pl.col("b") == pl.col("a") - 1) & (pl.col("c") == 0) & (pl.col("d") == 0))[
            "a"
        ].to_list()[i]
        == i + 1
        for i in range(1000)
    ),
)

print("\n== C3: extending triples (a,b,c), a <= 500")
N = 500
p = df.filter(pl.col("a") <= N)
ext = set(zip(*(p[c].to_list() for c in "abc")))
rows = []
for a in range(1, N + 1):
    b = np.repeat(np.arange(a + 1), np.arange(a + 1) + 1)
    c = np.concatenate([np.arange(bb + 1) for bb in range(a + 1)])
    rows.append(np.stack([np.full(len(b), a), b, c], 1))
T = np.concatenate(rows)
lab = np.fromiter(((int(x), int(y), int(z)) in ext for x, y, z in T), bool, len(T))
print(f"  triples {len(T):,}, extending {lab.sum():,} ({lab.mean():.1%})")


def H(pv):
    pv = pv[pv > 0]
    return -(pv * np.log2(pv)).sum()


def cond_mi(feature, cond):
    # I(label; feature | cond) in bits, from counts
    out = 0.0
    for cv in np.unique(cond):
        m = cond == cv
        w = m.mean()
        l = lab[m]
        f = feature[m]
        if l.all() or not l.any():
            continue
        hl = H(np.bincount(l.astype(int), minlength=2) / len(l))
        hlf = 0.0
        for fv in np.unique(f):
            mm = f == fv
            hlf += mm.mean() * H(np.bincount(l[mm].astype(int), minlength=2) / mm.sum())
        out += w * (hl - hlf)
    return out


amb = T[:, 0] - T[:, 1]
cc = T[:, 2]
print("  I(extends ; (a-b) mod m | c) in millibits:")
for m in [7, 8, 14, 16, 28, 32, 48, 56, 112, 224]:
    print(f"    m={m:4d}: {1000 * cond_mi(amb % m, cc):7.2f}")

print("\n== C3: autocorrelation of the lexicographic d-sequence (a <= 500)")
d = p.sort("a", "b", "c")["d"].to_numpy().astype(float)
d -= d.mean()
n = len(d)
f = np.fft.rfft(d, 2 * n)
ac = np.fft.irfft(f * np.conj(f))[:301] / ac0 if (ac0 := (d * d).sum()) else None
lags = np.arange(2, 301)
order = lags[np.argsort(-ac[2:301])]
print(
    f"  r(112) = {ac[112]:.4f}; rank of lag 112 among lags 2..300: {int(np.where(order == 112)[0][0]) + 1}"
)
print("  top 8 lags:", [(int(l), round(float(ac[l]), 4)) for l in order[:8]])
