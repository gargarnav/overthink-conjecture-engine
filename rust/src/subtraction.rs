//! Subtraction games: a heap of n tokens, a move removes s tokens for some s in S.

use crate::mex_of;

/// Grundy values g(0..=n_max) of the subtraction game with subtraction set `moves`.
pub fn grundy(moves: &[u32], n_max: usize) -> Vec<u32> {
    let mut g = vec![0u32; n_max + 1];
    let mut opts = Vec::with_capacity(moves.len());
    for n in 0..=n_max {
        opts.clear();
        for &s in moves {
            let s = s as usize;
            if s >= 1 && s <= n {
                opts.push(g[n - s]);
            }
        }
        g[n] = mex_of(&opts);
    }
    g
}

#[cfg(test)]
mod tests {
    use super::grundy;

    #[test]
    fn s123_is_n_mod_4() {
        let g = grundy(&[1, 2, 3], 100);
        assert!(g.iter().enumerate().all(|(n, &v)| v == (n % 4) as u32));
    }

    #[test]
    fn s134_has_period_7() {
        // Classical example: S = {1,3,4} has Grundy sequence 0,1,0,1,2,3,2 repeating.
        let pat = [0, 1, 0, 1, 2, 3, 2];
        let g = grundy(&[1, 3, 4], 200);
        assert!(g.iter().enumerate().all(|(n, &v)| v == pat[n % 7]));
    }
}
