//! Wythoff's game: two heaps (x, y); remove any positive number from one heap,
//! or the same positive number from both.

use crate::mex_of;

/// Grundy values G(x, y) for 0 <= x, y < n, row-major (index x * n + y).
pub fn grundy_table(n: usize) -> Vec<u32> {
    let mut g = vec![0u32; n * n];
    let mut opts = Vec::new();
    for x in 0..n {
        for y in 0..n {
            opts.clear();
            for k in 1..=x {
                opts.push(g[(x - k) * n + y]);
            }
            for k in 1..=y {
                opts.push(g[x * n + (y - k)]);
            }
            for k in 1..=x.min(y) {
                opts.push(g[(x - k) * n + (y - k)]);
            }
            g[x * n + y] = mex_of(&opts);
        }
    }
    g
}

#[cfg(test)]
mod tests {
    use super::grundy_table;

    #[test]
    fn zeros_are_beatty_pairs() {
        // P-positions are (floor(k*phi), floor(k*phi^2)) and their mirrors.
        let n = 300;
        let g = grundy_table(n);
        let phi = (1.0 + 5f64.sqrt()) / 2.0;
        let mut expected = vec![false; n * n];
        for k in 0.. {
            let a = (k as f64 * phi).floor() as usize;
            let b = a + k;
            if a >= n {
                break;
            }
            if b < n {
                expected[a * n + b] = true;
                expected[b * n + a] = true;
            }
        }
        for i in 0..n * n {
            assert_eq!(g[i] == 0, expected[i], "cell ({}, {})", i / n, i % n);
        }
    }
}
