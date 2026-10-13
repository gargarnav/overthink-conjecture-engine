//! Exact P-positions of 4-row Chomp.
//!
//! A position is (a, b, c, d) with a >= b >= c >= d >= 0 and a >= 1 (row
//! lengths; square (0,0) in row a is poisoned and cannot be taken). A move
//! picks a square (row i, column j) other than (0,0) and removes it together
//! with everything above and to the right: r_t <- min(r_t, j) for t >= i.
//!
//! For fixed (b, c, d), moves in the long row reach every (a', b, c, d) with
//! b <= a' < a, so at most one a gives a P-position. Grouping by the pair
//! p = (c, d), the P-positions form a partial function b -> a_p(b), where
//! a_p(b) is the least a >= max(b, 1) not excluded by a P-position reachable
//! through some other move:
//!
//!   row b, col j in [c, b)  -> (a, j, c, d)          excludes a_p(j), j < b
//!   row b, col j in [0, c)  -> (a, j, j, min(d,j))   excludes a_q(j), q=(j,min(d,j))
//!   row c, col j in [0, c)  -> (a, b, j, min(d,j))   excludes a_q(b)
//!   row d, col j in [0, d)  -> (a, b, c, j)          excludes a_(c,j)(b)
//!
//! Two kinds of moves do not depend on a at all and make every position N:
//!
//!   row a, col j in [c, b), j >= 1  -> (j, j, c, d): N if a_p(j) = j for some j < b
//!   row a, col j in [1, c)          -> (j, j, j, min(d,j)): N if a_q(j) = j
//!
//! Every pair depends only on pairs with smaller c + d, so pairs on the same
//! anti-diagonal are solved in parallel.
//!
//! Truncation: with a <= max_a, a_p(b) is reported only when it is <= max_a.
//! Values above max_a never exclude anything below it, so every reported
//! P-position is exact.

use rayon::prelude::*;

pub const NONE: u32 = u32::MAX;

/// Per-pair results: `rows[pidx(c, d)][b - c]` is a_p(b) - b, or NONE.
pub struct Chomp4Table {
    pub max_c: usize,
    pub max_a: usize,
    rows: Vec<Vec<u32>>,
}

#[inline]
fn pidx(c: usize, d: usize) -> usize {
    c * (c + 1) / 2 + d
}

impl Chomp4Table {
    /// a_p(b) for pair (c, d), if it is <= max_a.
    #[inline]
    pub fn a_of(&self, c: usize, d: usize, b: usize) -> Option<usize> {
        let v = self.rows[pidx(c, d)][b - c];
        (v != NONE).then(|| b + v as usize)
    }

    /// All P-positions (a, b, c, d) with c <= max_c and a <= max_a, ordered by (c, d, b).
    pub fn positions(&self) -> [Vec<u32>; 4] {
        let mut out: [Vec<u32>; 4] = Default::default();
        for c in 0..=self.max_c {
            for d in 0..=c {
                for (i, &v) in self.rows[pidx(c, d)].iter().enumerate() {
                    if v != NONE {
                        let b = c + i;
                        out[0].push((b + v as usize) as u32);
                        out[1].push(b as u32);
                        out[2].push(c as u32);
                        out[3].push(d as u32);
                    }
                }
            }
        }
        out
    }
}

fn solve_pair(t: &Chomp4Table, c: usize, d: usize) -> Vec<u32> {
    let max_a = t.max_a;
    let len = max_a + 1 - c;
    let none = || vec![NONE; len];
    let lower = |j: usize| (j, d.min(j));

    // Constant-position kill: (j, j, j, min(d,j)) is P for some 1 <= j < c.
    if (1..c).any(|j| {
        let (qc, qd) = lower(j);
        t.a_of(qc, qd, j) == Some(j)
    }) {
        return none();
    }

    // Permanent exclusions: a_p(j) for earlier b in this pair, and F_p.
    let mut used = vec![false; max_a + 2];
    for j in 0..c {
        let (qc, qd) = lower(j);
        if let Some(a) = t.a_of(qc, qd, j) {
            used[a] = true;
        }
    }

    // Lower pairs reached by row-c and row-d moves, each with its own b offset.
    let lower_rows: Vec<(&[u32], usize)> = (0..c)
        .map(|j| {
            let (qc, qd) = lower(j);
            (t.rows[pidx(qc, qd)].as_slice(), qc)
        })
        .chain((0..d).map(|j| (t.rows[pidx(c, j)].as_slice(), c)))
        .collect();

    let mut out = Vec::with_capacity(len);
    let mut mark = vec![usize::MAX; max_a + 2];
    let mut dead = false;
    for b in c..=max_a {
        if dead {
            out.push(NONE);
            continue;
        }
        for &(row, off) in &lower_rows {
            let v = row[b - off];
            if v != NONE {
                mark[b + v as usize] = b;
            }
        }
        let mut a = b.max(1);
        while a <= max_a && (used[a] || mark[a] == b) {
            a += 1;
        }
        if a > max_a {
            out.push(NONE);
            continue;
        }
        out.push((a - b) as u32);
        used[a] = true;
        if a == b {
            dead = true;
        }
    }
    out
}

/// Solve all pairs (c, d) with d <= c <= max_c, for a <= max_a.
pub fn solve(max_c: usize, max_a: usize) -> Chomp4Table {
    assert!(max_c <= max_a, "max_c must not exceed max_a");
    let npairs = pidx(max_c, max_c) + 1;
    let mut t = Chomp4Table {
        max_c,
        max_a,
        rows: vec![Vec::new(); npairs],
    };
    for s in 0..=2 * max_c {
        let todo: Vec<(usize, usize)> = (0..=s / 2)
            .map(|d| (s - d, d))
            .filter(|&(c, d)| c <= max_c && d <= c)
            .collect();
        let solved: Vec<Vec<u32>> = todo
            .par_iter()
            .map(|&(c, d)| solve_pair(&t, c, d))
            .collect();
        for ((c, d), row) in todo.into_iter().zip(solved) {
            t.rows[pidx(c, d)] = row;
        }
    }
    t
}

#[cfg(test)]
mod tests {
    use super::solve;

    #[test]
    fn single_square_is_p() {
        let t = solve(0, 5);
        assert_eq!(t.a_of(0, 0, 0), Some(1));
    }

    #[test]
    fn two_row_p_positions_are_b_plus_one() {
        // Classical: with c = d = 0, the P-positions are exactly (b+1, b).
        let t = solve(0, 200);
        for b in 0..200 {
            assert_eq!(t.a_of(0, 0, b), Some(b + 1));
        }
    }
}
