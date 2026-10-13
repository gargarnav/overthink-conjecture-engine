-- SPDX-License-Identifier: MIT
import Mathlib

/-!
# Subtraction games: periodicity from a finite window

The subtraction game with subtraction set `S`: a heap of `n` tokens; a move removes `s ∈ S`
tokens (`0 < s ≤ n`). `grundy S n` is the Sprague-Grundy value, defined by the mex recursion.

`periodic_of_window` reduces a periodicity statement `g (n + p) = g n` for all `n ≥ n₀` to
`m` consecutive cases `n₀ ≤ n < n₀ + m`, where `m` bounds `S`. The finite cases are evaluated
by the kernel (`decide`) through `table`, a structurally recursive version of `grundy` proved
equal to it (`grundy_eq_table`).

Proof status:
* `periodic_of_window`, `grundy_eq_table`: proved in general (kernel-checked).
* `grundy_134_period7`, `grundy_123_period4`, `grundy_257_period22`: statements for all `n`
  (general); proved from `periodic_of_window` plus a finite base case checked by `decide`
  (kernel evaluation, no `native_decide`). Each one was proposed by the pipeline in run
  `dev_subtraction_wythoff` and survived 10x falsification (n ≤ 2000).
-/

namespace Overthink.Subtraction

/-- Minimum excludant (structural recursion, so the kernel can evaluate it). -/
def mexAux (l : List ℕ) : ℕ → ℕ → ℕ
  | n, 0 => n
  | n, fuel + 1 => if n ∈ l then mexAux l (n + 1) fuel else n

/-- The least natural number not in `l`. -/
def mex (l : List ℕ) : ℕ := mexAux l 0 (l.length + 1)

/-- Sprague-Grundy value of a heap of `n` tokens. -/
def grundy (S : List ℕ) (n : ℕ) : ℕ :=
  mex (S.filterMap fun s => if _h : 0 < s ∧ s ≤ n then some (grundy S (n - s)) else none)
termination_by n
decreasing_by omega

theorem grundy_eq (S : List ℕ) (n : ℕ) :
    grundy S n =
      mex (S.filterMap fun s => if 0 < s ∧ s ≤ n then some (grundy S (n - s)) else none) := by
  rw [grundy]
  simp only [dite_eq_ite]

/-- When every move is available, `g n` is the mex of `g (n - s)` over `s ∈ S`. -/
theorem grundy_eq_of_le {S : List ℕ} {n : ℕ} (hS : ∀ s ∈ S, 0 < s ∧ s ≤ n) :
    grundy S n = mex (S.map fun s => grundy S (n - s)) := by
  rw [grundy_eq, ← List.filterMap_eq_map]
  congr 1
  apply List.filterMap_congr
  intro s hs
  simp [hS s hs]

/-- **Periodicity from a finite window.** If every `s ∈ S` satisfies `0 < s ≤ m`, and
`g (n + p) = g n` for the `m` heaps `n₀ ≤ n < n₀ + m`, then it holds for all `n ≥ n₀`. -/
theorem periodic_of_window {S : List ℕ} {m n₀ p : ℕ} (hS : ∀ s ∈ S, 0 < s ∧ s ≤ m)
    (hbase : ∀ n, n₀ ≤ n → n < n₀ + m → grundy S (n + p) = grundy S n) :
    ∀ n, n₀ ≤ n → grundy S (n + p) = grundy S n := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro hn
    by_cases hlt : n < n₀ + m
    · exact hbase n hn hlt
    · have h1 : ∀ s ∈ S, 0 < s ∧ s ≤ n := fun s hs => ⟨(hS s hs).1, by have := (hS s hs).2; omega⟩
      have h2 : ∀ s ∈ S, 0 < s ∧ s ≤ n + p :=
        fun s hs => ⟨(hS s hs).1, by have := (h1 s hs).2; omega⟩
      rw [grundy_eq_of_le h2, grundy_eq_of_le h1]
      congr 1
      apply List.map_congr_left
      intro s hs
      have := hS s hs
      rw [show n + p - s = n - s + p by omega]
      exact ih (n - s) (by omega) (by omega)

/-! ## A kernel-evaluable table of Grundy values -/

/-- `table S n = [g (n-1), g (n-2), …, g 0]`, built by structural recursion. -/
def table (S : List ℕ) : ℕ → List ℕ
  | 0 => []
  | n + 1 =>
    let t := table S n
    mex (S.filterMap fun s => if 0 < s ∧ s ≤ n then t[s - 1]? else none) :: t

theorem table_length (S : List ℕ) (n : ℕ) : (table S n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [table, ih]

theorem table_getElem? (S : List ℕ) : ∀ n i, i < n → (table S n)[i]? = some (grundy S (n - 1 - i))
  | 0, i, h => absurd h (Nat.not_lt_zero _)
  | n + 1, 0, _ => by
    simp only [table, List.getElem?_cons_zero, Option.some.injEq, Nat.add_sub_cancel, Nat.sub_zero]
    rw [grundy_eq]
    congr 1
    apply List.filterMap_congr
    intro s _
    by_cases h : 0 < s ∧ s ≤ n
    · simp only [h, and_self, ↓reduceIte]
      rw [table_getElem? S n (s - 1) (by omega)]
      congr 2
      omega
    · simp only [h, ↓reduceIte]
  | n + 1, i + 1, h => by
    simp only [table, List.getElem?_cons_succ]
    rw [table_getElem? S n i (by omega)]
    congr 2
    omega

/-- The table agrees with the Grundy function. -/
theorem grundy_eq_table (S : List ℕ) (n : ℕ) : grundy S n = (table S (n + 1)).headD 0 := by
  have := table_getElem? S (n + 1) 0 (by omega)
  simp only [Nat.add_sub_cancel, Nat.sub_zero] at this
  cases h : table S (n + 1) with
  | nil => simp [h] at this
  | cons x xs => simp_all

/-! ## Periodicity statements proposed by the pipeline (all `n`, kernel-checked) -/

/-- S = {1, 3, 4}: Grundy values have period 7 (pipeline candidate, survived at n ≤ 2000). -/
theorem grundy_134_period7 : ∀ n, grundy [1, 3, 4] (n + 7) = grundy [1, 3, 4] n := by
  intro n
  refine periodic_of_window (m := 4) (n₀ := 0) (by decide) ?_ n (Nat.zero_le n)
  intro n _ hn
  simp only [grundy_eq_table]
  interval_cases n <;> decide

/-- S = {1, 2, 3}: Grundy values have period 4 (pipeline candidate, survived at n ≤ 2000). -/
theorem grundy_123_period4 : ∀ n, grundy [1, 2, 3] (n + 4) = grundy [1, 2, 3] n := by
  intro n
  refine periodic_of_window (m := 3) (n₀ := 0) (by decide) ?_ n (Nat.zero_le n)
  intro n _ hn
  simp only [grundy_eq_table]
  interval_cases n <;> decide

/-- S = {2, 5, 7}: Grundy values have period 22 (pipeline candidate, survived at n ≤ 2000). -/
theorem grundy_257_period22 : ∀ n, grundy [2, 5, 7] (n + 22) = grundy [2, 5, 7] n := by
  intro n
  refine periodic_of_window (m := 7) (n₀ := 0) (by decide) ?_ n (Nat.zero_le n)
  intro n _ hn
  simp only [grundy_eq_table]
  interval_cases n <;> decide

end Overthink.Subtraction
