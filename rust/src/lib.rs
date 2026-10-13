//! Performance-critical core of the Overthink Conjecture Engine.
//!
//! Exposed to Python as `overthink._core`. Pure-Rust logic lives in plain
//! functions so it can be unit-tested with `cargo test` without Python.

use pyo3::prelude::*;

/// Minimum excludant: the smallest non-negative integer not in `values`.
///
/// This is the core operation of Sprague-Grundy theory: the Grundy value of a
/// position is the mex of the Grundy values of its options.
pub fn mex_of(values: &[u32]) -> u32 {
    // The mex of k values is at most k, so only values < k+1 matter.
    let k = values.len();
    let mut seen = vec![false; k + 1];
    for &v in values {
        if (v as usize) <= k {
            seen[v as usize] = true;
        }
    }
    seen.iter().position(|&s| !s).unwrap() as u32
}

/// Minimum excludant of a list of non-negative integers.
#[pyfunction]
fn mex(values: Vec<u32>) -> u32 {
    mex_of(&values)
}

/// Version of the compiled Rust core.
#[pyfunction]
fn core_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mex, m)?)?;
    m.add_function(wrap_pyfunction!(core_version, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::mex_of;

    #[test]
    fn mex_empty_is_zero() {
        assert_eq!(mex_of(&[]), 0);
    }

    #[test]
    fn mex_fills_first_gap() {
        assert_eq!(mex_of(&[0, 1, 3]), 2);
        assert_eq!(mex_of(&[1, 2, 3]), 0);
        assert_eq!(mex_of(&[2, 0, 1, 0]), 3);
    }

    #[test]
    fn mex_ignores_large_values() {
        assert_eq!(mex_of(&[0, 1_000_000]), 1);
    }
}
