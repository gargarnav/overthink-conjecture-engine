"""Type stubs for the compiled Rust core (rust/src/lib.rs)."""

def mex(values: list[int]) -> int:
    """Smallest non-negative integer not in `values`."""

def core_version() -> str:
    """Version of the compiled Rust core."""

def chomp4_p_positions(max_c: int, max_a: int, max_d: int | None = None) -> tuple: ...
def wythoff_subtraction_grundy(moves: list[int], n: int): ...
