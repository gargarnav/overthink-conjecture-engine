# Rediscovery run 2 on 4×n Chomp: report

**Not blind** (see `PROTOCOL.md`). Tag `rediscovery2-frozen` → `c33c7c1`. Mining output in commit `702dc2f`, falsification output in `c1b3b05`. Proposal window a ≤ 300, falsification at a ≤ 3000 (10×), dataset `chomp4_a3000_c60`.

## Results, in the order fixed by the protocol

### 1. Functional dependencies: all 4 proposed, all 4 survived (as predicted)

| Statement | Status | Rows (window → full) |
|---|---|---|
| a is determined by (b, c, d) | survived | 172,092 → 2,010,792 |
| b is determined by (a, c, d) | survived | 172,092 → 2,010,792 |
| c is determined by (a, b, d) | survived | 172,092 → 2,010,792 |
| **d is determined by (a, b, c)** (= v1 C1 / v2 Lemma 1) | survived | 172,092 → 2,010,792 |

All four are theorems with a one-move proof (see `experiments/rediscovery/REPORT.md`, Part B). They are natural first targets for general Lean proofs.

### 2. Coverage

| | Run 1 (a ≤ 100, groups ≤ 30) | Run 2 (a ≤ 300, groups ≤ 60) |
|---|---|---|
| `a~b` sequences | 364 | 1,522 |
| `a~b` proposals | 61 | 160 (10.5%) |
| `a~b` survivors | 57 | 151 (76 with c ≤ 30, 75 with 30 < c ≤ 60) |
| `b~a` survivors | 12 | 12 |

Most (c, d) sequences still get no proposal: a − b does not settle into a period with enough repetitions inside a ≤ 300.

Periods among the run-2 `a~b` survivors (period: count): 1: 62, 2: 19, 3: 5, 4: 3, 6: 7, 8: 5, 12: 16, 16: 17, 24: 3, 32: 9, 48: 4, 64: 1.

### 3. Second-order statements: none

No second-order sequence reached the minimum length of 12 consecutive groups. The longest runs of consecutive groups that have a proposal are 6 (over c, with d = 3 fixed) and 3 (over d, with c = 4 fixed). So no statement about how the period depends on (c, d) could be proposed.

### 4. Totals: 176 proposals → 167 survived, 9 refuted, 0 untestable

Refuted (all `a~b`; counterexample index b, observed vs predicted a; then the unfalsified re-proposal from a ≤ 3000):

| (c, d) | Proposal | Counterexample | Re-proposal (unfalsified) |
|---|---|---|---|
| (27, 6) | period 1 from b ≥ 261 | b = 282: 301 vs 299 | period 192 from b ≥ 292 |
| (29, 21) | period 1 from b ≥ 132 | b = 303: 329 vs 328 | period 192 from b ≥ 497 |
| (30, 6) | period 1 from b ≥ 261 | b = 290: 311 vs 308 | period 192 from b ≥ 292 |
| (35, 5) | period 2 from b ≥ 250 | b = 285: 307 vs 305 | period 96 from b ≥ 362 |
| (43, 41) | period 1 from b ≥ 122 | b = 428: 470 vs 469 | period 192 from b ≥ 1914 |
| (43, 43) | period 1 from b ≥ 121 | b = 673: 717 vs 716 | period 192 from b ≥ 1913 |
| (48, 46) | period 1 from b ≥ 87 | b = 2181: 2229 vs 2228 | period 1 from b ≥ 2183 |
| (55, 9) | period 1 from b ≥ 199 | b = 270: 305 vs 304 | period 192 from b ≥ 569 |
| (56, 55) | period 4 from b ≥ 108 | b = 391: 447 vs 443 | period 4 from b ≥ 2348 |

The (48, 46) case held for almost 2,100 terms beyond its start before failing at b = 2181, i.e. at 7× the proposal window. This is the strongest example so far of why the 10× rule matters.

### 5. Consistency with run 1

All 57 run-1 `a~b` survivors get a run-2 proposal for the same (c, d) with the **same period and delta**, and none is contradicted.

### 6. Scores against the ground truth (non-blind)

| Ground truth | Run 2 | Note |
|---|---|---|
| v1 C1 / v2 Lemma 1 | **Found (non-blind)** | Emitted as `d ← (a, b, c)` and survived. This capability was added after reading the ground truth, so it is not a rediscovery. |
| v1 C2, C3, C4; v2 Conjectures 1–2 | Missed | Statement forms the miners cannot express (unchanged from run 1). |

## Observation from reading the output (AI-assisted, not a pipeline result)

Every period proposed in runs 1 and 2, including the re-proposals made at a ≤ 3000, is of the form **2ᵏ or 3·2ᵏ**: 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 192. No other period occurs, and in particular no factor of 7. This is a candidate conjecture about the eventual periods of a − b along b for fixed (c, d). It is relevant to the "period-8 signal of unknown origin" in v1/v2, and it also has to be checked against the known periodicity literature before any claim of novelty. It was **not** produced by the pipeline: the miners have no view across the parameters of different groups unless 12 consecutive groups all have proposals. A "parameter-set" view (the set of periods across all groups) would be the natural pipeline extension. Like everything here, it would need its own pre-registered run.

## Reproduction

```bash
git checkout rediscovery2-frozen
uv run overthink generate experiments/configs/datasets/chomp4_a3000_c60.yaml
uv run overthink mine experiments/configs/mining/rediscovery2_chomp4.yaml
uv run overthink falsify <run dir>
```
