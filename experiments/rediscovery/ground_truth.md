# Ground truth for the blind rediscovery test (step 4)

Added by the author on 2026-10-13. This was after the freeze tag (`rediscovery-frozen` → `1a99e9c`, originally `3e4aead`), the raw mining output (step 2) and the falsification output (step 3) had been committed and pushed publicly to GitHub. Statements are quoted verbatim.

## Source

- **v1:** A. Garg, *Structural Conjectures for 4 × n Chomp: Unique Extension, Asymptotic Ratios, and Period-112 Geometry*, arXiv:2604.25952v1 [math.GM], 24 Apr 2026. Data: all 4,316,097 P-positions with n ≤ 500.
- **v2:** A. Garg, *Structural Results for 4 × n Chomp: Unique Extension, Bimodal Asymptotic Structure, and Period-112 Geometry*, arXiv:2604.25952v2 [math.GM], 21 May 2026. Data: all 961,619,972 P-positions with n ≤ 3000.

Both versions predate the freeze. The **primary ground truth is v1's four conjectures**: they are "the four structural conjectures" referred to when this project was set up. v2's revisions are scored separately.

## v1 (primary)

**Conjecture 1 (Unique Extension).** *For any triple (a, b, c) with a ≥ b ≥ c ≥ 0, there exists at most one non-negative integer d such that (a, b, c, d) is a P-position of 4 × n Chomp.*

**Conjecture 2 (Asymptotic Ratios).** *For P-positions (a, b, c, d) of 4 × n Chomp with a large, the row-length ratios converge to fixed constants L₁, L₂, L₃:  b/a → L₁, c/a → L₂, d/a → L₃, as a → ∞, with estimated values L₁ ≈ 0.762, L₂ ≈ 0.499, L₃ ≈ 0.224.*
(v1 §3.2 and Fig. 1: estimated from windowed medians of the ratios over P-positions with first row a.)

**Conjecture 3 (Period-112 Mask).** *The set of triples (a, b, c) that extend to 4 × n P-positions exhibits modular structure with fundamental period 112. Membership in the extending set is predicted with 79% accuracy by a logistic classifier using only c and (a − b) mod 112.*

**Conjecture 4 (Linear Cone).** *The set of extending triples (a, b, c) forms a linear cone in ℝ³ with asymptotic width  width(c) ≈ (11/8)·c + f(c mod 112), where f is a bounded periodic function with period 112.*

## v2 (revisions)

- **Lemma 1 (Unique Extension)**, proved in v2 (formerly Conjecture 1): *For any triple (a, b, c) with a ≥ b ≥ c ≥ 0, there is at most one non-negative integer d such that (a, b, c, d) is a P-position of 4 × n Chomp.* Corollary 1 extends this to k-row Chomp.
- **Conjecture 1 (HIGH family asymptotic ratios):** *There exists an infinite set S_H ⊆ ℕ of natural density approximately 0.561 such that for P-positions (a, b, c, d) with a ∈ S_H and a → ∞: b/a → L₁ᴴ ≈ 0.780, c/a → L₂ᴴ ≈ 0.519, d/a → 1/4.*
- **Conjecture 2 (LOW family asymptotic ratios):** *There exists an infinite set S_L ⊆ ℕ of natural density approximately 0.439 such that for P-positions (a, b, c, d) with a ∈ S_L and a → ∞: b/a → L₁ᴸ ≈ 0.753, c/a → L₂ᴸ ≈ 0.465, d/a → L₃ᴸ ≈ 0.183.*
  (v2 §4.1: HIGH/LOW is defined by whether the per-a median of d/a over P-positions with first row a is above 0.21.)
- **Conjectures 3 and 4:** unchanged from v1.
