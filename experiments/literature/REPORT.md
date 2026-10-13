# Literature check: 4-row Chomp survivors (2026-10-13)

Checks the surviving conjectures from rediscovery runs 1 and 2 against published work before any claim of novelty. Scripts in this directory reproduce every comparison.

## Sources found

1. **S. Byrnes, "Poset game periodicity", *INTEGERS* 3 (2003), #G3.** Poset Game Periodicity Theorem (statement as quoted in Fenner & Rogers' survey, arXiv:1505.07416, Thm 3.3). Along two chains C, D with a fixed finite part A, positions with any fixed Grundy value are either finitely many or eventually periodic: g(A_{m,n}) = k iff g(A_{m+p,n+p}) = k for large n. For Chomp: fix all rows except the top two.
2. **X. Sun, *Computer-Assisted and Computer-Generated Research in Combinatorial Games and Pattern-Avoidance*, PhD thesis, Temple University, May 2004.** Sun's periodicity conjecture (proved by Byrnes). Theorem 2.1 is computer-proved eventual periodicity for k = 4 with the bottom two rows summing to ≤ 9, except one case. Table 2.1, "Periodic Properties of Some Four-rowed P-positions", lists the period and start for 25 bottom-row pairs.
3. **A. E. Brouwer, "The game of Chomp"** (web page, with corrections by G. Nivasch). Table of (r, start, period) for 3-rowed Chomp up to r = 10,000, plus explicit P-positions for small r.
4. D. Zeilberger, "Three-rowed Chomp" (2001) and "Chomp, Recurrences, and Chaos(?)". Ultimately-periodic data for 3-rowed Chomp; credits Sun's conjecture and Byrnes's proof.

## Findings

**1. The form of every survivor is a theorem (Byrnes 2003).** All 69 (run 1) and 151 + 12 (run 2) periodicity survivors say "for fixed (c, d), a(b + p) = a(b) + p for all b ≥ n0". Byrnes's theorem guarantees that, for each (c, d), either there are finitely many P-positions or such p and n0 exist. The survivors are therefore **instances with specific parameters**, not new kinds of statement. Our "finite" pairs (dead groups) are the theorem's first case.

**2. Sun's 4-row table (2004) agrees with our data** (`sun2004_table21.py`, data a ≤ 3000):
- Finitely vs infinitely many P-positions: **25/25 agree.** All 15 blank entries are pairs with only 3–6 P-positions in total.
- Periods: **10/10 agree.**
- Starts: **7/10 agree.** They differ for (c, d) = (6, 3): ours 4, Sun 11; (6, 4): ours 3, Sun 8; and (6, 5): ours 13, Sun 14, all in x₃ = b − c. Our starts are the minimal b from which the relation holds through a ≤ 3000. Sun does not define S precisely enough to tell whether this is a definitional difference or an error. Unresolved.

**3. Independent validation against published 3-row data** (`brouwer_3row.py`, output in `brouwer_3row_output.txt`). With d = 0 (exactly 3-rowed Chomp), this project's solver and periodicity miner reproduce **all 9 published (r, start, period) entries exactly**: r = 120, 400, 402, 422, 585, 890, 892, 2027 and 6541, with periods 2, 2, 4, 2, 4, 4, 4, 3 and 9. The largest computation covered c ≤ 6541, a ≤ 13,910: 28.8M P-positions in 416 s.

**4. Retraction: the "periods are 2ᵏ or 3·2ᵏ" observation is false.** It came from reading run-2 output (c ≤ 60). (c, d) = (6541, 0) has period 9, as published by Brouwer/Nivasch and reproduced here. The observation only held on the small range examined.

**5. Registry updates** (`mark_known.py`): 23 conjectures marked `known`:
- 8 groups match Sun's Table 2.1 exactly (period and start) in each of runs 1 and 2;
- 3 groups match classical or published 3-row/2-row results ((0,0): Winning Ways; (2,0) and (5,0): Brouwer);
- Unique Extension (d ← (a, b, c)), source A. Garg, arXiv:2604.25952v2, Lemma 1.

The other survivors remain `survived`. Their form is known (Byrnes), and their specific (period, start) values for 10 ≤ c ≤ 60 do not appear in the sources found. Sun's complete list ("the website specified above") was not accessible, so **no novelty is claimed** for them. At most they are an extended, verified table of parameters.

**6. The functional dependencies a ← (b, c, d), b ← (a, c, d), c ← (a, b, d)** follow from the same one-move argument as Unique Extension. No citation was found; they are the first targets for Lean proofs.

## Consequences for arXiv:2604.25952 (for the author)

- v1/v2 state that "the 4 × n case has received no systematic computational treatment". Sun (2002, *Improvements on Chomp*, INTEGERS; and 2004 thesis) computed four-rowed P-positions and their periodic properties (Table 2.1), and Byrnes (2003) proved eventual periodicity for fixed lower rows. A v3 should cite Sun 2002/2004 and Byrnes 2003 and soften that sentence.
- v1 Conjecture 3's "period-7 signal inherited from the 3 × n sub-game": the published 3-row periods up to r = 10,000 are 1, 2, 3, 4 and 9, and no period 7 is reported.

## Sources

- [Byrnes, Poset game periodicity (INTEGERS 3, G3)](https://emis.univie.ac.at/journals/INTEGERS/papers/dg3/dg3.pdf), statement as quoted in [Fenner & Rogers, arXiv:1505.07416](https://arxiv.org/pdf/1505.07416)
- [Sun, PhD thesis (Temple University, 2004)](https://cst.temple.edu/sites/cst/files/theses9/xysun.pdf)
- [Brouwer, The game of Chomp](https://aeb.win.tue.nl/games/chomp.html)
- [Zeilberger, Chomp, Recurrences, and Chaos(?)](https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/byrnes.html)
