//! Performance-critical core of the Overthink Conjecture Engine.
//!
//! Exposed to Python as `overthink._core`. Pure-Rust logic lives in plain
//! functions so it can be unit-tested with `cargo test` without Python.

use numpy::ndarray::Array2;
use numpy::{IntoPyArray, PyArray1, PyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

pub mod chomp4;
pub mod subtraction;
pub mod wythoff;

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

/// Grundy values g(0..=n_max) of the subtraction game with the given subtraction set.
#[pyfunction]
fn subtraction_grundy<'py>(
    py: Python<'py>,
    moves: Vec<u32>,
    n_max: usize,
) -> Bound<'py, PyArray1<u32>> {
    py.detach(|| subtraction::grundy(&moves, n_max))
        .into_pyarray(py)
}

/// Wythoff Grundy values G(x, y) for 0 <= x, y < n as an n x n array.
#[pyfunction]
fn wythoff_grundy<'py>(py: Python<'py>, n: usize) -> Bound<'py, PyArray2<u32>> {
    let flat = py.detach(|| wythoff::grundy_table(n));
    Array2::from_shape_vec((n, n), flat)
        .expect("table is n*n")
        .into_pyarray(py)
}

/// All P-positions (a, b, c, d) of 4-row Chomp with c <= max_c and a <= max_a,
/// returned as four uint32 arrays (a, b, c, d) ordered by (c, d, b).
#[pyfunction]
#[allow(clippy::type_complexity)]
fn chomp4_p_positions<'py>(
    py: Python<'py>,
    max_c: usize,
    max_a: usize,
) -> PyResult<(
    Bound<'py, PyArray1<u32>>,
    Bound<'py, PyArray1<u32>>,
    Bound<'py, PyArray1<u32>>,
    Bound<'py, PyArray1<u32>>,
)> {
    if max_c > max_a {
        return Err(PyValueError::new_err("max_c must not exceed max_a"));
    }
    if max_a >= u32::MAX as usize - 1 {
        return Err(PyValueError::new_err("max_a too large"));
    }
    let [a, b, c, d] = py.detach(|| chomp4::solve(max_c, max_a).positions());
    Ok((
        a.into_pyarray(py),
        b.into_pyarray(py),
        c.into_pyarray(py),
        d.into_pyarray(py),
    ))
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(mex, m)?)?;
    m.add_function(wrap_pyfunction!(core_version, m)?)?;
    m.add_function(wrap_pyfunction!(subtraction_grundy, m)?)?;
    m.add_function(wrap_pyfunction!(wythoff_grundy, m)?)?;
    m.add_function(wrap_pyfunction!(chomp4_p_positions, m)?)?;
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
