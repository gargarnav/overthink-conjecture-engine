# SPDX-License-Identifier: MIT
"""Classical miners: exact recovery on known sequences, checker behaviour, selection rules."""

import math
from fractions import Fraction

import pytest

from overthink.conjecture import floorlinear, periodic, polynomial, recurrence
from overthink.conjecture.benchmark import run_benchmark
from overthink.conjecture.checks import check
from overthink.conjecture.mine import mine_sequence
from overthink.conjecture.oeis import OEISSnapshot
from overthink.conjecture.oeis import mine as oeis_mine
from overthink.conjecture.types import Sequence


def seq(values, start=0):
    return Sequence("test", list(values), start)


def phi_floor(k):
    return (k + math.isqrt(5 * k * k)) // 2  # floor(k * phi), exact


# --- periodicity -------------------------------------------------------------


def test_periodic_with_preperiod():
    vals = [7, 7, 7] + [0, 1, 0, 1, 2, 3, 2] * 20
    (c,) = periodic.mine(seq(vals, start=5), {})
    assert c.kind == "periodic"
    assert c.params == {"period": 7, "delta": 0, "n0": 8}


def test_additive_periodic():
    vals = [n + (n % 3 == 0) for n in range(100)]
    (c,) = periodic.mine(seq(vals), {})
    assert (c.kind, c.params["period"], c.params["delta"], c.params["n0"]) == (
        "additive_periodic",
        3,
        3,
        0,
    )


def test_periodic_respects_min_support():
    assert periodic.mine(seq([1, 2] * 5), {"min_support": 20}) == []


# --- recurrences ---------------------------------------------------------------


def test_berlekamp_massey_fibonacci_and_powers():
    fib = [0, 1]
    while len(fib) < 40:
        fib.append(fib[-1] + fib[-2])
    assert recurrence.berlekamp_massey(fib, 10) == [1, 1]
    assert recurrence.berlekamp_massey([3 * 2**n for n in range(30)], 10) == [2]
    tribonacci = [0, 0, 1]
    while len(tribonacci) < 50:
        tribonacci.append(sum(tribonacci[-3:]))
    assert recurrence.berlekamp_massey(tribonacci, 10) == [1, 1, 1]


def test_berlekamp_massey_respects_max_order():
    assert recurrence.berlekamp_massey([n * n % 97 for n in range(200)], 5) is None


def test_recurrence_candidate_checks_out():
    pell = [0, 1]
    while len(pell) < 60:
        pell.append(2 * pell[-1] + pell[-2])
    (c,) = recurrence.mine(seq(pell[:40]), {})
    assert c.params["coefficients"] == ["2", "1"]
    assert check(c.kind, c.params, seq(pell))["status"] == "holds"


# --- polynomials ----------------------------------------------------------------


def test_fit_polynomial_exact():
    pts = [(n, n * (n + 1) // 2) for n in range(3)]
    assert polynomial.fit_polynomial(pts) == [0, Fraction(1, 2), Fraction(1, 2)]


def test_polynomial_triangular_numbers():
    (c,) = polynomial.mine(seq([n * (n + 1) // 2 for n in range(60)]), {})
    assert c.kind == "polynomial"
    assert c.params["polynomials"] == {"0": ["0", "1/2", "1/2"]}


def test_quasi_polynomial_floor_half_square():
    (c,) = polynomial.mine(seq([n * n // 2 for n in range(80)]), {})
    assert c.kind == "quasi_polynomial" and c.params["modulus"] == 2
    assert check(c.kind, c.params, seq([n * n // 2 for n in range(800)]))["status"] == "holds"


# --- floor-linear -----------------------------------------------------------------


def test_simplest_between():
    assert floorlinear.simplest_between(Fraction(1, 3), Fraction(1, 2)) == Fraction(2, 5)
    assert floorlinear.simplest_between(Fraction(3, 2), Fraction(5, 2)) == 2
    assert floorlinear.simplest_between(Fraction(0), None) == 1
    assert floorlinear.simplest_between(Fraction(2), Fraction(3)) == Fraction(5, 2)


def test_wythoff_beatty_identified_as_phi():
    a = [phi_floor(k) for k in range(300)]
    cands = floorlinear.mine(seq(a), {})
    names = {c.params["alpha_name"] for c in cands}
    assert "phi" in names
    assert None in names  # the weak statement is always present
    long = seq([phi_floor(k) for k in range(5000)])
    for c in cands:
        if c.params["alpha_name"] == "phi":
            assert check(c.kind, c.params, long)["status"] == "holds"


def test_floor_linear_interval_contains_alpha():
    lo, hi = floorlinear.alpha_interval([phi_floor(k) for k in range(500)])
    assert lo < (1 + 5**0.5) / 2 < hi


# --- checker ----------------------------------------------------------------------


def test_check_reports_first_counterexample():
    vals = [0, 1] * 50 + [5] + [0, 1] * 10
    res = check("periodic", {"period": 2, "delta": 0, "n0": 0}, seq(vals, start=10))
    assert res["status"] == "violated"
    assert res["first_counterexample"] == 110


# --- selection and benchmark ---------------------------------------------------------


def test_mdl_prefers_beatty_over_spurious_period():
    # sqrt(51) is close to 50/7: an additive period of 7 holds on a long stretch.
    from decimal import Decimal

    alpha = Decimal(51).sqrt()
    vals = [int(alpha * k // 1) for k in range(200)]
    kinds = {c.kind for c in mine_sequence(seq(vals), {})}
    assert kinds == {"floor_linear"}


def test_benchmark_small():
    r = run_benchmark({}, n_per_family=15, seed=123)
    for fam in [
        "periodic",
        "additive_periodic",
        "periodic_long_preperiod",
        "linear_recurrence",
        "polynomial",
        "quasi_polynomial",
        "floor_linear",
    ]:
        assert r[fam]["recovered"] == r[fam]["n"], fam
    assert r["negative_uniform"]["candidates"] == 0
    assert r["negative_random_walk"]["candidates"] == 0


# --- OEIS ---------------------------------------------------------------------------


@pytest.fixture
def snapshot(tmp_path):
    fib = [0, 1]
    while len(fib) < 30:
        fib.append(fib[-1] + fib[-2])
    lines = [
        "# fake snapshot for tests",
        "A000045 ," + ",".join(map(str, fib)) + ",",
        "A000004 ," + ",".join(["0"] * 30) + ",",
        "A999999 ,7,7," + ",".join(map(str, fib[5:])) + ",",
    ]
    p = tmp_path / "stripped"
    p.write_text("\n".join(lines) + "\n")
    return OEISSnapshot(p)


def test_oeis_exact_match_with_offset(snapshot):
    fib = [0, 1]
    while len(fib) < 30:
        fib.append(fib[-1] + fib[-2])
    cands = oeis_mine(seq(fib[5:25]), {"min_terms": 8}, snapshot)
    found = {(c.params["anumber"], c.params["oeis_offset"]) for c in cands}
    assert found == {("A000045", 5), ("A999999", 2)}


def test_oeis_skips_low_information(snapshot):
    assert oeis_mine(seq([0] * 20), {"min_terms": 8}, snapshot) == []
