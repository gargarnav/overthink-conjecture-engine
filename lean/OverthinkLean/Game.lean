-- SPDX-License-Identifier: MIT
import Mathlib

/-!
# P-positions of a terminating game

A game is given by its move relation: `Move x y` means `y` is reachable from `x` in one move.
`IsPLabelling Move P` says that `P` marks exactly the P-positions (previous player wins):
a position is a P-position iff no move leads to a P-position.

For a terminating game (no infinite sequence of moves, i.e. `flip Move` is well-founded)
such a labelling exists and is unique, so "the P-positions" is well defined.

Proof status: all results in this file are proved in general (kernel-checked, no `decide`).
-/

namespace Overthink

variable {α : Type*}

/-- `P` marks the P-positions of `Move`: `x` is a P-position iff every move from `x` leads to
a position that is not a P-position. -/
def IsPLabelling (Move : α → α → Prop) (P : α → Prop) : Prop :=
  ∀ x, P x ↔ ∀ y, Move x y → ¬ P y

namespace IsPLabelling

variable {Move : α → α → Prop} {P Q : α → Prop}

/-- No move leads from a P-position to a P-position. -/
theorem not_move (h : IsPLabelling Move P) {x y : α} (hx : P x) (hy : P y) : ¬ Move x y :=
  fun hm => (h x).1 hx y hm hy

/-- In a terminating game there is at most one P-labelling. -/
theorem unique (hwf : WellFounded (flip Move)) (hP : IsPLabelling Move P)
    (hQ : IsPLabelling Move Q) : P = Q := by
  funext x
  apply propext
  refine hwf.induction (C := fun x => P x ↔ Q x) x ?_
  intro x ih
  rw [hP x, hQ x]
  exact forall_congr' fun y => imp_congr_right fun hm => not_congr (ih y hm)

/-- In a terminating game a P-labelling exists. -/
theorem exists_of_wf (hwf : WellFounded (flip Move)) : ∃ P, IsPLabelling Move P := by
  refine ⟨hwf.fix (C := fun _ => Prop) (fun x IH => ∀ y (h : Move x y), ¬ IH y h), fun x => ?_⟩
  rw [hwf.fix_eq]

end IsPLabelling

end Overthink
