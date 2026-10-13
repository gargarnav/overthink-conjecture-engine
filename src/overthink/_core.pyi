# SPDX-License-Identifier: MIT
"""Type stubs for the compiled Rust core (rust/src/lib.rs)."""

import numpy as np
import numpy.typing as npt

def mex(values: list[int]) -> int:
    """Smallest non-negative integer not in `values`."""

def core_version() -> str:
    """Version of the compiled Rust core."""

def subtraction_grundy(moves: list[int], n_max: int) -> npt.NDArray[np.uint32]: ...
def wythoff_grundy(n: int) -> npt.NDArray[np.uint32]: ...
def wythoff_subtraction_grundy(moves: list[int], n: int) -> npt.NDArray[np.uint32]: ...
def chomp4_p_positions(
    max_c: int, max_a: int, max_d: int | None = None
) -> tuple[
    npt.NDArray[np.uint32], npt.NDArray[np.uint32], npt.NDArray[np.uint32], npt.NDArray[np.uint32]
]: ...
