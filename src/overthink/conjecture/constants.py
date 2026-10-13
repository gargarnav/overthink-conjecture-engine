"""A fixed library of named real constants for identifying slopes of floor-linear sequences.

The library is part of the miner configuration: adding constants after seeing data is
a form of tuning, so changes must be logged.
"""

from __future__ import annotations

from decimal import Decimal, getcontext

getcontext().prec = 60

_PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
_S2, _S3, _S5 = Decimal(2).sqrt(), Decimal(3).sqrt(), Decimal(5).sqrt()
_PHI = (1 + _S5) / 2


def _beatty_complement(a: Decimal) -> Decimal:
    return a / (a - 1)


CONSTANTS: dict[str, Decimal] = {
    "phi": _PHI,
    "phi^2": _PHI * _PHI,
    "1/phi": 1 / _PHI,
    "sqrt2": _S2,
    "2+sqrt2": _beatty_complement(_S2),
    "1+sqrt2": 1 + _S2,
    "sqrt2/2": _S2 / 2,
    "sqrt3": _S3,
    "(3+sqrt3)/2": _beatty_complement(_S3),
    "sqrt5": _S5,
    "e": Decimal(1).exp(),
    "e/(e-1)": _beatty_complement(Decimal(1).exp()),
    "pi": _PI,
    "pi/(pi-1)": _beatty_complement(_PI),
    "ln2": Decimal(2).ln(),
}
