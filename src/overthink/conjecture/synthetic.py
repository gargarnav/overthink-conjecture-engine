# SPDX-License-Identifier: MIT
"""Synthetic sequences with planted structure, plus negative controls, for benchmarking miners.

Each generator returns a function `make(length)` so the same planted sequence can be
produced at the proposal length and at 10x for scoring. A mined candidate counts as
*correct* only if it still holds on the 10x extension.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from typing import Any

from overthink.conjecture.constants import CONSTANTS


@dataclass
class Planted:
    family: str
    make: Callable[[int], list[int]]
    length: int
    expected: dict[str, Any] = field(default_factory=dict)
    accepted_kinds: tuple[str, ...] = ()  # empty = negative control (no structure)


def _min_period(block: list[int]) -> int:
    p = len(block)
    return next(q for q in range(1, p + 1) if p % q == 0 and block == block[:q] * (p // q))


def periodic(rng: random.Random, additive: bool, long_preperiod: bool = False) -> Planted:
    while True:
        p = rng.randint(1, 20)
        t = rng.randint(100, 220) if long_preperiod else rng.randint(0, 30)
        block = [rng.randint(0, 9) for _ in range(p)]
        if _min_period(block) == p:
            break
    delta = rng.randint(1, 5) if additive else 0
    pre = [rng.randint(0, 9) for _ in range(t)]

    def make(n: int) -> list[int]:
        tail = [block[i % p] + delta * (i // p) for i in range(max(0, n - t))]
        seq = (pre + tail)[:n]
        return seq

    # Make the preperiod exact: the term just before the periodic part must break the pattern.
    if t > 0:
        full = make(t + p + 1)
        if full[t - 1 + p] - full[t - 1] == delta:
            pre[-1] = full[t - 1 + p] - delta + rng.choice([-1, 1])
    kind = "additive_periodic" if additive else "periodic"
    family = kind + ("_long_preperiod" if long_preperiod else "")
    return Planted(family, make, 300, {"period": p, "delta": delta, "n0": t}, (kind,))


def recurrence(rng: random.Random) -> Planted:
    order = rng.randint(2, 4)
    coeffs = [rng.randint(-2, 2) for _ in range(order - 1)] + [rng.choice([-2, -1, 1, 2])]
    init = [rng.randint(-5, 5) for _ in range(order)]

    def make(n: int) -> list[int]:
        s = init[:n]
        while len(s) < n:
            s.append(sum(c * s[-i] for i, c in enumerate(coeffs, start=1)))
        return s

    # Some recurrences (e.g. roots of unity) produce periodic sequences; those are acceptable.
    return Planted(
        "linear_recurrence",
        make,
        60,
        {"order": order},
        ("linear_recurrence", "periodic", "additive_periodic", "polynomial", "quasi_polynomial"),
    )


def polynomial(rng: random.Random) -> Planted:
    deg = rng.randint(2, 3)
    coeffs = [Fraction(rng.randint(-6, 6), rng.choice([1, 2])) for _ in range(deg)] + [
        Fraction(rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([1, 2]))
    ]

    def make(n: int) -> list[int]:
        # floor keeps values integral when coefficients are halves
        return [int(sum(c * k**j for j, c in enumerate(coeffs)) // 1) for k in range(n)]

    return Planted("polynomial", make, 80, {"degree": deg}, ("polynomial", "quasi_polynomial"))


def quasi_polynomial(rng: random.Random) -> Planted:
    m, deg = rng.randint(2, 3), rng.randint(1, 2)
    while True:
        polys = [[rng.randint(-5, 5) for _ in range(deg)] + [rng.randint(1, 4)] for _ in range(m)]
        if len({p[-1] for p in polys}) > 1:  # distinct leading coefficients
            break

    def make(n: int) -> list[int]:
        return [sum(c * k**j for j, c in enumerate(polys[k % m])) for k in range(n)]

    return Planted(
        "quasi_polynomial", make, 120, {"modulus": m, "degree": deg}, ("quasi_polynomial",)
    )


def beatty(rng: random.Random) -> Planted:
    named = rng.random() < 0.5
    if named:
        name = rng.choice(sorted(CONSTANTS))
        alpha = CONSTANTS[name]
    else:
        k = rng.choice([k for k in range(2, 60) if int(k**0.5) ** 2 != k])
        name, alpha = None, Decimal(k).sqrt() * Decimal(rng.randint(1, 3)) / 2
    beta = Decimal(rng.randint(0, 999)) / 1000

    def make(n: int) -> list[int]:
        return [int((alpha * k + beta) // 1) for k in range(n)]

    return Planted(
        "floor_linear", make, 200, {"alpha_name": name, "alpha": float(alpha)}, ("floor_linear",)
    )


def random_uniform(rng: random.Random) -> Planted:
    seed = rng.random()

    def make(n: int) -> list[int]:
        r = random.Random(seed)
        return [r.randint(0, 9) for _ in range(n)]

    return Planted("negative_uniform", make, 300)


def random_walk(rng: random.Random) -> Planted:
    seed = rng.random()

    def make(n: int) -> list[int]:
        r, s, x = random.Random(seed), [], 0
        for _ in range(n):
            x += r.choice([-1, 0, 1])
            s.append(x)
        return s

    return Planted("negative_random_walk", make, 300)


def noisy_periodic(rng: random.Random) -> Planted:
    """Periodic, but every term is independently corrupted with probability 1/40, so the
    pattern never settles. Any conjecture claiming eventual periodicity is false."""
    p = rng.randint(2, 12)
    block = [rng.randint(0, 9) for _ in range(p)]
    seed = rng.random()

    def make(n: int) -> list[int]:
        r = random.Random(seed)
        return [block[i % p] if r.random() > 1 / 40 else r.randint(10, 99) for i in range(n)]

    return Planted("negative_noisy_periodic", make, 300)


GENERATORS: dict[str, Callable[[random.Random], Planted]] = {
    "periodic": lambda r: periodic(r, additive=False),
    "additive_periodic": lambda r: periodic(r, additive=True),
    "periodic_long_preperiod": lambda r: periodic(r, additive=False, long_preperiod=True),
    "linear_recurrence": recurrence,
    "polynomial": polynomial,
    "quasi_polynomial": quasi_polynomial,
    "floor_linear": beatty,
    "negative_uniform": random_uniform,
    "negative_random_walk": random_walk,
    "negative_noisy_periodic": noisy_periodic,
}
