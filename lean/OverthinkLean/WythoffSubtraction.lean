import Mathlib

/-!
# Wythoff subtraction games W(S)

Two heaps `(x, y)` and a list `S` of move sizes. A move removes `s ∈ S` tokens from one heap,
or `s` tokens from both heaps. `grundy S x y` is the Sprague–Grundy value, defined by the mex
recursion over `opts S x y`.

Results (all proved for every position; kernel-checked, no `decide` on infinite statements):

* `grundy_eq_of`: a function that never takes its own value on an option and reaches every
  smaller value on some option *is* the Grundy function.
* `grundy_mod_three` (LLM proposal H02): if `1, 2 ∈ S` and no `s ∈ S` is divisible by 3, then
  `G(x, y) = (x + y) % 3`.
* `grundy_odd` (LLM proposal H01): if `1 ∈ S` and every `s ∈ S` is odd, then `G = F₁`, where
  `F₁ x y` is 0 if `x, y` are even, 2 if both are odd, and for mixed parity 1 if the odd
  coordinate is the larger one, else 3.
* `grundy_scale`: `G_{k·S}(x, y) = G_S(⌊x/k⌋, ⌊y/k⌋)`, hence the scaled formulas (LLM proposals
  H03, H04).
-/

namespace Overthink.WSub

/-- The positions reachable from `(x, y)` in one move. -/
def opts (S : List ℕ) (x y : ℕ) : List (ℕ × ℕ) :=
  S.flatMap fun s =>
    (if 0 < s ∧ s ≤ x then [(x - s, y)] else []) ++
    (if 0 < s ∧ s ≤ y then [(x, y - s)] else []) ++
    (if 0 < s ∧ s ≤ x ∧ s ≤ y then [(x - s, y - s)] else [])

theorem mem_opts {S : List ℕ} {x y : ℕ} {q : ℕ × ℕ} :
    q ∈ opts S x y ↔ ∃ s ∈ S, 0 < s ∧
      ((s ≤ x ∧ q = (x - s, y)) ∨ (s ≤ y ∧ q = (x, y - s)) ∨
        (s ≤ x ∧ s ≤ y ∧ q = (x - s, y - s))) := by
  simp only [opts, List.mem_flatMap, List.mem_append]
  constructor
  · rintro ⟨s, hs, h⟩
    refine ⟨s, hs, ?_⟩
    split_ifs at h <;> simp_all
    tauto
  · rintro ⟨s, hs, hpos, h⟩
    refine ⟨s, hs, ?_⟩
    rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩ <;> simp_all

theorem sum_lt_of_mem_opts {S : List ℕ} {x y : ℕ} {q : ℕ × ℕ} (h : q ∈ opts S x y) :
    q.1 + q.2 < x + y := by
  obtain ⟨s, -, hs, h⟩ := mem_opts.1 h
  rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩ <;> simp <;> omega

theorem exists_not_mem (l : List ℕ) : ∃ n, n ∉ l := by
  obtain ⟨n, hn⟩ := Infinite.exists_notMem_finset l.toFinset
  exact ⟨n, by simpa using hn⟩

/-- Minimum excludant. -/
noncomputable def mex (l : List ℕ) : ℕ := Nat.find (exists_not_mem l)

theorem mex_not_mem (l : List ℕ) : mex l ∉ l := Nat.find_spec (exists_not_mem l)

theorem mem_of_lt_mex {l : List ℕ} {u : ℕ} (h : u < mex l) : u ∈ l := by
  by_contra hu
  exact Nat.find_min (exists_not_mem l) h hu

theorem mex_eq {l : List ℕ} {v : ℕ} (h1 : v ∉ l) (h2 : ∀ u < v, u ∈ l) : mex l = v := by
  rcases lt_trichotomy (mex l) v with h | h | h
  · exact absurd (h2 _ h) (mex_not_mem l)
  · exact h
  · exact absurd (mem_of_lt_mex h) h1

/-- Sprague–Grundy value of `(x, y)` in W(S). -/
noncomputable def grundy (S : List ℕ) (x y : ℕ) : ℕ :=
  mex ((opts S x y).attach.map fun q => grundy S q.1.1 q.1.2)
termination_by x + y
decreasing_by exact sum_lt_of_mem_opts q.2

theorem grundy_eq (S : List ℕ) (x y : ℕ) :
    grundy S x y = mex ((opts S x y).map fun q => grundy S q.1 q.2) := by
  rw [grundy]
  congr 1
  conv_rhs => rw [← List.attach_map_subtype_val (opts S x y), List.map_map]
  rfl

theorem grundy_ne_of_mem_opts {S : List ℕ} {x y : ℕ} {q : ℕ × ℕ} (h : q ∈ opts S x y) :
    grundy S q.1 q.2 ≠ grundy S x y := by
  intro heq
  apply mex_not_mem ((opts S x y).map fun q => grundy S q.1 q.2)
  rw [← grundy_eq, ← heq]
  exact List.mem_map.2 ⟨q, h, rfl⟩

theorem exists_opt_of_lt_grundy {S : List ℕ} {x y v : ℕ} (h : v < grundy S x y) :
    ∃ q ∈ opts S x y, grundy S q.1 q.2 = v := by
  rw [grundy_eq] at h
  exact List.mem_map.1 (mem_of_lt_mex h)

/-- **Characterization.** If `f` differs from its value on every option, and every smaller
value is attained on some option, then `f` is the Grundy function. -/
theorem grundy_eq_of {S : List ℕ} (f : ℕ → ℕ → ℕ)
    (hne : ∀ x y q, q ∈ opts S x y → f q.1 q.2 ≠ f x y)
    (hcov : ∀ x y v, v < f x y → ∃ q ∈ opts S x y, f q.1 q.2 = v) :
    ∀ x y, grundy S x y = f x y := by
  suffices ∀ n x y, x + y = n → grundy S x y = f x y from fun x y => this _ x y rfl
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro x y hn
    have hmap : (opts S x y).map (fun q => grundy S q.1 q.2) = (opts S x y).map
        (fun q => f q.1 q.2) := by
      apply List.map_congr_left
      intro q hq
      exact ih _ (hn ▸ sum_lt_of_mem_opts hq) q.1 q.2 rfl
    rw [grundy_eq, hmap]
    apply mex_eq
    · intro hmem
      obtain ⟨q, hq, hfq⟩ := List.mem_map.1 hmem
      exact hne x y q hq hfq
    · intro u hu
      obtain ⟨q, hq, hfq⟩ := hcov x y u hu
      exact List.mem_map.2 ⟨q, hq, hfq⟩

/-! ## H02: `(x + y) % 3` -/

/-- **H02.** If `1 ∈ S`, `2 ∈ S` and no element of `S` is divisible by 3 (or zero), then the
Grundy value of `(x, y)` is `(x + y) % 3`. -/
theorem grundy_mod_three {S : List ℕ} (h1 : 1 ∈ S) (h2 : 2 ∈ S)
    (hS : ∀ s ∈ S, s % 3 ≠ 0) : ∀ x y, grundy S x y = (x + y) % 3 := by
  apply grundy_eq_of
  · intro x y q hq
    obtain ⟨s, hs, hpos, h⟩ := mem_opts.1 hq
    have := hS s hs
    rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩ <;> simp only <;> omega
  · intro x y v hv
    have m1x : 1 ≤ x → (x - 1, y) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨1, h1, by omega, Or.inl ⟨h, rfl⟩⟩
    have m1y : 1 ≤ y → (x, y - 1) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨1, h1, by omega, Or.inr (Or.inl ⟨h, rfl⟩)⟩
    have m2x : 2 ≤ x → (x - 2, y) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨2, h2, by omega, Or.inl ⟨h, rfl⟩⟩
    have m2y : 2 ≤ y → (x, y - 2) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨2, h2, by omega, Or.inr (Or.inl ⟨h, rfl⟩)⟩
    have m11 : 1 ≤ x → 1 ≤ y → (x - 1, y - 1) ∈ opts S x y :=
      fun hx hy => mem_opts.2 ⟨1, h1, by omega, Or.inr (Or.inr ⟨hx, hy, rfl⟩)⟩
    -- v < (x + y) % 3, so (x + y) % 3 ≥ 1 and some heap is nonempty
    have hv' : v + 1 = (x + y) % 3 ∨ v + 2 = (x + y) % 3 := by omega
    rcases hv' with hv' | hv'
    · -- remove 1 token from a nonempty heap
      by_cases hx : 1 ≤ x
      · exact ⟨_, m1x hx, by simp only; omega⟩
      · exact ⟨_, m1y (by omega), by simp only; omega⟩
    · -- (x + y) % 3 = 2 and v = 0: remove 2 in total
      by_cases hx : 2 ≤ x
      · exact ⟨_, m2x hx, by simp only; omega⟩
      · by_cases hy : 2 ≤ y
        · exact ⟨_, m2y hy, by simp only; omega⟩
        · exact ⟨_, m11 (by omega) (by omega), by simp only; omega⟩

/-! ## H01: all-odd move sets containing 1 -/

/-- The Grundy function of W({1}) (and of every W(S) with `S` odd and `1 ∈ S`). -/
def F₁ (x y : ℕ) : ℕ :=
  if x % 2 = 0 ∧ y % 2 = 0 then 0
  else if x % 2 = 1 ∧ y % 2 = 1 then 2
  else if (x % 2 = 1 ∧ y < x) ∨ (y % 2 = 1 ∧ x < y) then 1
  else 3

/-- **H01.** If `1 ∈ S` and every `s ∈ S` is odd, the Grundy value of `(x, y)` is `F₁ x y`. -/
theorem grundy_odd {S : List ℕ} (h1 : 1 ∈ S) (hS : ∀ s ∈ S, s % 2 = 1) :
    ∀ x y, grundy S x y = F₁ x y := by
  apply grundy_eq_of
  · intro x y q hq
    obtain ⟨s, hs, hpos, h⟩ := mem_opts.1 hq
    have := hS s hs
    rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩ <;> simp only [F₁] <;>
      split_ifs <;> omega
  · intro x y v hv
    have m1x : 1 ≤ x → (x - 1, y) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨1, h1, by omega, Or.inl ⟨h, rfl⟩⟩
    have m1y : 1 ≤ y → (x, y - 1) ∈ opts S x y :=
      fun h => mem_opts.2 ⟨1, h1, by omega, Or.inr (Or.inl ⟨h, rfl⟩)⟩
    have m11 : 1 ≤ x → 1 ≤ y → (x - 1, y - 1) ∈ opts S x y :=
      fun hx hy => mem_opts.2 ⟨1, h1, by omega, Or.inr (Or.inr ⟨hx, hy, rfl⟩)⟩
    -- the three candidate options and their values, in every parity/order case
    unfold F₁ at hv
    split_ifs at hv with ha hb hc
    · omega
    · -- both odd, value 2: need 0 (diagonal) and 1
      have : v = 0 ∨ v = 1 := by omega
      rcases this with rfl | rfl
      · exact ⟨_, m11 (by omega) (by omega), by simp only [F₁]; split_ifs <;> omega⟩
      · by_cases hxy : y < x
        · exact ⟨_, m1y (by omega), by simp only [F₁]; split_ifs <;> omega⟩
        · exact ⟨_, m1x (by omega), by simp only [F₁]; split_ifs <;> omega⟩
    · -- mixed parity, odd coordinate larger, value 1: need 0
      have : v = 0 := by omega
      subst this
      rcases hc with ⟨hx, -⟩ | ⟨hy, -⟩
      · exact ⟨_, m1x (by omega), by simp only [F₁]; split_ifs <;> omega⟩
      · exact ⟨_, m1y (by omega), by simp only [F₁]; split_ifs <;> omega⟩
    · -- mixed parity, odd coordinate smaller, value 3: need 0, 1, 2
      have : v = 0 ∨ v = 1 ∨ v = 2 := by omega
      by_cases hx : x % 2 = 1
      · -- x odd, y even, x < y
        rcases this with rfl | rfl | rfl
        · exact ⟨_, m1x (by omega), by simp only [F₁]; split_ifs <;> omega⟩
        · exact ⟨_, m11 (by omega) (by omega), by simp only [F₁]; split_ifs <;> omega⟩
        · exact ⟨_, m1y (by omega), by simp only [F₁]; split_ifs <;> omega⟩
      · -- x even, y odd, y < x
        rcases this with rfl | rfl | rfl
        · exact ⟨_, m1y (by omega), by simp only [F₁]; split_ifs <;> omega⟩
        · exact ⟨_, m11 (by omega) (by omega), by simp only [F₁]; split_ifs <;> omega⟩
        · exact ⟨_, m1x (by omega), by simp only [F₁]; split_ifs <;> omega⟩

/-! ## H03, H04: scaling -/

/-- **Scaling.** Multiplying every move size by `k > 0` turns W(S) into `k²` interleaved copies
of itself: `G_{k·S}(x, y) = G_S(⌊x/k⌋, ⌊y/k⌋)`. -/
theorem grundy_scale {S : List ℕ} {k : ℕ} (hk : 0 < k) :
    ∀ x y, grundy (S.map (k * ·)) x y = grundy S (x / k) (y / k) := by
  apply grundy_eq_of (fun x y => grundy S (x / k) (y / k))
  · intro x y q hq
    obtain ⟨t, ht, hpos, h⟩ := mem_opts.1 hq
    obtain ⟨s, hs, rfl⟩ := List.mem_map.1 ht
    have hs0 : 0 < s := by
      rcases Nat.eq_zero_or_pos s with h0 | h0
      · simp [h0] at hpos
      · exact h0
    have key : ∀ z, k * s ≤ z → (z - k * s) / k = z / k - s ∧ s ≤ z / k := fun z hz =>
      ⟨by rw [Nat.sub_mul_div z k s], (Nat.le_div_iff_mul_le hk).2 (by linarith)⟩
    rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩
    · obtain ⟨e, le⟩ := key x h1
      simp only [e]
      exact grundy_ne_of_mem_opts (mem_opts.2 ⟨s, hs, hs0, Or.inl ⟨le, rfl⟩⟩)
    · obtain ⟨e, le⟩ := key y h1
      simp only [e]
      exact grundy_ne_of_mem_opts (mem_opts.2 ⟨s, hs, hs0, Or.inr (Or.inl ⟨le, rfl⟩)⟩)
    · obtain ⟨e1, le1⟩ := key x h1
      obtain ⟨e2, le2⟩ := key y h2
      simp only [e1, e2]
      exact grundy_ne_of_mem_opts (mem_opts.2 ⟨s, hs, hs0, Or.inr (Or.inr ⟨le1, le2, rfl⟩)⟩)
  · intro x y v hv
    obtain ⟨q, hq, hgq⟩ := exists_opt_of_lt_grundy hv
    obtain ⟨s, hs, hs0, h⟩ := mem_opts.1 hq
    have hks : 0 < k * s := Nat.mul_pos hk hs0
    have hmem : k * s ∈ S.map (k * ·) := List.mem_map.2 ⟨s, hs, rfl⟩
    have lift : ∀ z, s ≤ z / k → k * s ≤ z ∧ (z - k * s) / k = z / k - s := fun z hz =>
      have h' : k * s ≤ z := le_trans (Nat.mul_le_mul_left k hz) (Nat.mul_div_le z k)
      ⟨h', by rw [Nat.sub_mul_div z k s]⟩
    rcases h with ⟨h1, rfl⟩ | ⟨h1, rfl⟩ | ⟨h1, h2, rfl⟩
    · obtain ⟨le, e⟩ := lift x h1
      exact ⟨(x - k * s, y), mem_opts.2 ⟨_, hmem, hks, Or.inl ⟨le, rfl⟩⟩, by simp only [e]; exact hgq⟩
    · obtain ⟨le, e⟩ := lift y h1
      exact ⟨(x, y - k * s), mem_opts.2 ⟨_, hmem, hks, Or.inr (Or.inl ⟨le, rfl⟩)⟩,
        by simp only [e]; exact hgq⟩
    · obtain ⟨le1, e1⟩ := lift x h1
      obtain ⟨le2, e2⟩ := lift y h2
      exact ⟨(x - k * s, y - k * s), mem_opts.2 ⟨_, hmem, hks, Or.inr (Or.inr ⟨le1, le2, rfl⟩)⟩,
        by simp only [e1, e2]; exact hgq⟩

/-! ## The statements proposed by the LLM, for the sets in the dataset -/

/-- H01 for `{1}`, `{1,3}`, `{1,5}`, `{1,3,5}`. -/
theorem H01 : ∀ S ∈ [[1], [1, 3], [1, 5], [1, 3, 5]], ∀ x y, grundy S x y = F₁ x y := by
  intro S hS
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hS
  rcases hS with rfl | rfl | rfl | rfl <;> exact grundy_odd (by decide) (by decide)

/-- H02 for `{1,2}`, `{1,2,4}`, `{1,2,5}`, `{1,2,4,5}`. -/
theorem H02 : ∀ S ∈ [[1, 2], [1, 2, 4], [1, 2, 5], [1, 2, 4, 5]],
    ∀ x y, grundy S x y = (x + y) % 3 := by
  intro S hS
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hS
  rcases hS with rfl | rfl | rfl | rfl <;> exact grundy_mod_three (by decide) (by decide) (by decide)

/-- H03: `G_{s}(x, y) = F₁(⌊x/s⌋, ⌊y/s⌋)` for every `s > 0` (the dataset has `s = 2, 3, 4, 5`). -/
theorem H03 {s : ℕ} (hs : 0 < s) (x y : ℕ) : grundy [s] x y = F₁ (x / s) (y / s) := by
  have := grundy_scale (S := [1]) hs x y
  simp only [List.map_cons, List.map_nil, mul_one] at this
  rw [this, grundy_odd (by decide) (by decide)]

/-- H04: `G_{2,4}(x, y) = (⌊x/2⌋ + ⌊y/2⌋) % 3`. -/
theorem H04 (x y : ℕ) : grundy [2, 4] x y = (x / 2 + y / 2) % 3 := by
  have := grundy_scale (S := [1, 2]) (k := 2) (by decide) x y
  simp only [List.map_cons, List.map_nil] at this
  rw [this, grundy_mod_three (by decide) (by decide) (by decide)]

end Overthink.WSub
