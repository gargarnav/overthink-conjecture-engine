import OverthinkLean
/-! Run `lake env lean CheckAxioms.lean`. Every theorem below must depend only on
`propext`, `Classical.choice` and `Quot.sound`: no `sorryAx`, and no `Lean.ofReduceBool`
(which `native_decide` would introduce). -/
#print axioms Overthink.IsPLabelling.unique
#print axioms Overthink.IsPLabelling.exists_of_wf
#print axioms Overthink.Chomp.wf
#print axioms Overthink.Chomp.eq_of_isP_of_eq_off
#print axioms Overthink.Chomp.unique_extension
#print axioms Overthink.Chomp.unique_third_row
#print axioms Overthink.Chomp.unique_second_row
#print axioms Overthink.Chomp.unique_first_row
#print axioms Overthink.Subtraction.periodic_of_window
#print axioms Overthink.Subtraction.grundy_eq_table
#print axioms Overthink.Subtraction.grundy_134_period7
#print axioms Overthink.Subtraction.grundy_123_period4
#print axioms Overthink.Subtraction.grundy_257_period22
#print axioms Overthink.WSub.grundy_eq_of
#print axioms Overthink.WSub.grundy_mod_three
#print axioms Overthink.WSub.grundy_odd
#print axioms Overthink.WSub.grundy_scale
#print axioms Overthink.WSub.H01
#print axioms Overthink.WSub.H02
#print axioms Overthink.WSub.H03
#print axioms Overthink.WSub.H04
