import Mathlib
import OverthinkLean.Game

/-!
# Chomp with `k` rows

A position is given by its row lengths `r : Fin k → ℕ`. Row `0` contains the poisoned square
`(0, 0)`. A move picks a square `(i, j)` of the position other than the poisoned one and
removes it together with every square `(i', j')` with `i' ≥ i` and `j' ≥ j`; that is, every
row `t ≥ i` is cut to length at most `j`. The player who cannot move loses, so the position
consisting of the poisoned square alone is a P-position.

Main result (`eq_of_isP_of_eq_off`): two valid P-positions that differ in at most one row are
equal. For 4-row Chomp this gives four functional dependencies, among them Unique Extension
(`unique_extension`, A. Garg, arXiv:2604.25952v2, Lemma 1): for each `(a, b, c)` there is at
most one `d` such that `(a, b, c, d)` is a P-position.

Proof status: everything in this file is proved in general (kernel-checked, no `decide`).
-/

namespace Overthink.Chomp

open Finset

/-- Row lengths of a position of `k`-row Chomp; row `0` holds the poisoned square. -/
abbrev Pos (k : ℕ) := Fin k → ℕ

variable {k : ℕ}

/-- A valid position: row lengths are non-increasing and the poisoned square is present. -/
def Valid (r : Pos k) : Prop := Antitone r ∧ ∀ h : 0 < k, 1 ≤ r ⟨0, h⟩

/-- Taking square `(i, j)`: every row `t ≥ i` is cut to length at most `j`. -/
def chomp (r : Pos k) (i : Fin k) (j : ℕ) : Pos k :=
  fun t => if i ≤ t then min (r t) j else r t

/-- One move: take a square `(i, j)` of `r` (so `j < r i`) other than the poisoned square. -/
def Move (r s : Pos k) : Prop :=
  ∃ i : Fin k, ∃ j, j < r i ∧ ¬ (i.val = 0 ∧ j = 0) ∧ s = chomp r i j

/-- Every move removes at least one square. -/
theorem sum_lt_of_move {r s : Pos k} (h : Move r s) : ∑ t, s t < ∑ t, r t := by
  obtain ⟨i, j, hj, -, rfl⟩ := h
  apply Finset.sum_lt_sum
  · intro t _
    unfold chomp
    split_ifs
    · exact min_le_left _ _
    · exact le_rfl
  · exact ⟨i, Finset.mem_univ _, by simp [chomp, hj]⟩

/-- Chomp terminates. -/
theorem wf : WellFounded (flip (@Move k)) :=
  Subrelation.wf (fun {_ _} h => sum_lt_of_move h) (measure fun r : Pos k => ∑ t, r t).wf

/-- The P-positions of `k`-row Chomp (exist and are unique, since Chomp terminates). -/
def IsP : Pos k → Prop := Classical.choose (IsPLabelling.exists_of_wf (wf (k := k)))

theorem isP_spec : IsPLabelling Move (IsP (k := k)) :=
  Classical.choose_spec (IsPLabelling.exists_of_wf (wf (k := k)))

/-- Any labelling satisfying the P-position recursion is `IsP`. -/
theorem isP_unique {P : Pos k → Prop} (hP : IsPLabelling Move P) : P = IsP :=
  IsPLabelling.unique wf hP isP_spec

/-- If two valid positions differ only in row `i`, the longer one can move to the shorter one
by taking square `(i, r i)`. -/
theorem move_of_eq_off {r s : Pos k} (hr : Valid r) (i : Fin k)
    (hoff : ∀ t, t ≠ i → r t = s t) (hlt : r i < s i) : Move s r := by
  refine ⟨i, r i, hlt, ?_, ?_⟩
  · rintro ⟨h0, hz⟩
    have hk : 0 < k := i.pos
    have h1 := hr.2 hk
    have hi : i = ⟨0, hk⟩ := Fin.ext h0
    rw [hi] at hz
    omega
  · funext t
    unfold chomp
    split_ifs with hit
    · rcases eq_or_lt_of_le hit with rfl | hit'
      · exact (min_eq_right hlt.le).symm
      · rw [← hoff t (ne_of_gt hit')]
        exact (min_eq_left (hr.1 hit)).symm
    · exact hoff t (by rintro rfl; exact hit le_rfl)

/-- **Two valid P-positions of `k`-row Chomp that differ in at most one row are equal.** -/
theorem eq_of_isP_of_eq_off {r s : Pos k} (hr : Valid r) (hs : Valid s) (i : Fin k)
    (hoff : ∀ t, t ≠ i → r t = s t) (hPr : IsP r) (hPs : IsP s) : r = s := by
  rcases lt_trichotomy (r i) (s i) with h | h | h
  · exact absurd (move_of_eq_off hr i hoff h) (isP_spec.not_move hPs hPr)
  · funext t
    by_cases ht : t = i
    · subst ht; exact h
    · exact hoff t ht
  · exact absurd (move_of_eq_off hs i (fun t ht => (hoff t ht).symm) h)
      (isP_spec.not_move hPr hPs)

/-! ## 4-row Chomp: each row length is determined by the other three -/

/-- **Unique Extension** (A. Garg, arXiv:2604.25952v2, Lemma 1): for each `(a, b, c)` there is
at most one `d` such that `(a, b, c, d)` is a P-position of 4-row Chomp. -/
theorem unique_extension {a b c d d' : ℕ} (h : Valid ![a, b, c, d]) (h' : Valid ![a, b, c, d'])
    (hP : IsP ![a, b, c, d]) (hP' : IsP ![a, b, c, d']) : d = d' := by
  have := eq_of_isP_of_eq_off h h' 3 (by intro t ht; fin_cases t <;> simp_all) hP hP'
  simpa using congrFun this 3

/-- For each `(a, b, d)` there is at most one `c` such that `(a, b, c, d)` is a P-position. -/
theorem unique_third_row {a b c c' d : ℕ} (h : Valid ![a, b, c, d]) (h' : Valid ![a, b, c', d])
    (hP : IsP ![a, b, c, d]) (hP' : IsP ![a, b, c', d]) : c = c' := by
  have := eq_of_isP_of_eq_off h h' 2 (by intro t ht; fin_cases t <;> simp_all) hP hP'
  simpa using congrFun this 2

/-- For each `(a, c, d)` there is at most one `b` such that `(a, b, c, d)` is a P-position. -/
theorem unique_second_row {a b b' c d : ℕ} (h : Valid ![a, b, c, d]) (h' : Valid ![a, b', c, d])
    (hP : IsP ![a, b, c, d]) (hP' : IsP ![a, b', c, d]) : b = b' := by
  have := eq_of_isP_of_eq_off h h' 1 (by intro t ht; fin_cases t <;> simp_all) hP hP'
  simpa using congrFun this 1

/-- For each `(b, c, d)` there is at most one `a` such that `(a, b, c, d)` is a P-position. -/
theorem unique_first_row {a a' b c d : ℕ} (h : Valid ![a, b, c, d]) (h' : Valid ![a', b, c, d])
    (hP : IsP ![a, b, c, d]) (hP' : IsP ![a', b, c, d]) : a = a' := by
  have := eq_of_isP_of_eq_off h h' 0 (by intro t ht; fin_cases t <;> simp_all) hP hP'
  simpa using congrFun this 0

end Overthink.Chomp
