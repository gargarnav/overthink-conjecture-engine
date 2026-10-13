"""Solver correctness: Rust implementations vs pure-Python oracles and known theorems."""

import numpy as np
import pytest

from overthink.games import chomp, subtraction, wythoff

# --- subtraction games -------------------------------------------------------


@pytest.mark.parametrize("moves", [[1], [1, 2], [1, 2, 3], [1, 3, 4], [2, 5, 7], [3, 4, 9, 11]])
def test_subtraction_rust_matches_reference(moves):
    assert subtraction.grundy(moves, 500).tolist() == subtraction.grundy_reference(moves, 500)


@pytest.mark.parametrize("k", [1, 2, 5, 10])
def test_subtraction_1_to_k_is_n_mod_k_plus_1(k):
    g = subtraction.grundy(range(1, k + 1), 1000)
    assert np.array_equal(g, np.arange(1001) % (k + 1))


def test_subtraction_134_period_7():
    # Classical example (Berlekamp-Conway-Guy): 0,1,0,1,2,3,2 repeating.
    g = subtraction.grundy([1, 3, 4], 700)
    assert np.array_equal(g, np.tile([0, 1, 0, 1, 2, 3, 2], 101)[:701])


def test_subtraction_rejects_bad_sets():
    with pytest.raises(ValueError):
        subtraction.grundy([0, 1], 10)


# --- Wythoff -----------------------------------------------------------------


def test_wythoff_rust_matches_reference():
    assert wythoff.grundy_table(40).tolist() == wythoff.grundy_table_reference(40)


def test_wythoff_zeros_match_closed_form():
    n = 1000
    g = wythoff.grundy_table(n)
    expected = np.zeros((n, n), dtype=bool)
    for a, b in wythoff.p_positions_closed_form(n):
        if b < n:
            expected[a, b] = expected[b, a] = True
    assert np.array_equal(g == 0, expected)


def test_wythoff_basic_properties():
    g = wythoff.grundy_table(200)
    assert np.array_equal(g, g.T)
    assert np.array_equal(g[0], np.arange(200))  # one heap = Nim heap


# --- Chomp -------------------------------------------------------------------


def test_chomp_options_example():
    # From (2,1): take (0,1) -> (1,1); take (1,0) -> (2,0). (1,0) needs two moves.
    assert sorted(chomp.options((2, 1))) == [(1, 1), (2, 0)]
    assert sorted(chomp.options((3, 2, 1))) == [
        (1, 1, 1),
        (2, 2, 1),
        (3, 0, 0),
        (3, 1, 1),
        (3, 2, 0),
    ]
    assert chomp.options((1, 0)) == []


@pytest.mark.parametrize("k", [2, 3, 4])
def test_chomp_rectangles_are_n_positions(k):
    # Strategy-stealing theorem: every rectangle with at least 2 squares is an N-position.
    p = chomp.p_positions_reference(k, 8)
    for n in range(1, 9):
        rect = (n,) * k
        assert rect not in p, rect


def test_chomp_two_row_closed_form():
    # Classical: 2-row P-positions are exactly (b+1, b).
    assert chomp.p_positions_reference(2, 30) == {(b + 1, b) for b in range(30)}


def _as_set(arr: np.ndarray) -> set[tuple[int, ...]]:
    return {tuple(int(x) for x in row) for row in arr}


@pytest.mark.parametrize("n", [1, 2, 5, 12, 20])
def test_chomp4_rust_matches_brute_force(n):
    assert _as_set(chomp.chomp4_p_positions(n)) == chomp.p_positions_reference(4, n)


def test_chomp4_truncated_c_is_subset():
    full = _as_set(chomp.chomp4_p_positions(20))
    part = _as_set(chomp.chomp4_p_positions(20, max_c=6))
    assert part == {p for p in full if p[2] <= 6}


def test_chomp4_restricted_to_three_rows_matches_brute_force():
    full = chomp.chomp4_p_positions(20)
    three = {(a, b, c) for a, b, c, d in _as_set(full) if d == 0}
    assert three == chomp.p_positions_reference(3, 20)


def test_chomp4_rectangles_large():
    pos = _as_set(chomp.chomp4_p_positions(150))
    for n in range(2, 151):
        assert (n, n, n, n) not in pos


def test_chomp4_at_most_one_a_per_bcd():
    arr = chomp.chomp4_p_positions(200)
    bcd = arr[:, 1:]
    assert len(np.unique(bcd, axis=0)) == len(bcd)


def test_chomp4_max_d_zero_is_three_row_chomp():
    three = {(int(a), int(b), int(c)) for a, b, c, d in chomp.chomp4_p_positions(25, max_d=0)}
    assert three == chomp.p_positions_reference(3, 25)


def test_chomp4_max_d_is_exact_subset():
    full = _as_set(chomp.chomp4_p_positions(40))
    part = _as_set(chomp.chomp4_p_positions(40, max_d=3))
    assert part == {p for p in full if p[3] <= 3}
