# SPDX-License-Identifier: MIT
import subprocess
import sys

import pytest

import overthink
from overthink import _core
from overthink.cli import main


def test_versions_agree():
    assert overthink.__version__ == _core.core_version()


@pytest.mark.parametrize(
    "values, expected",
    [([], 0), ([0, 1, 3], 2), ([1, 2, 3], 0), ([2, 0, 1, 0], 3), ([0, 10**6], 1)],
)
def test_mex(values, expected):
    assert _core.mex(values) == expected


def test_mex_rejects_negative():
    with pytest.raises(OverflowError):
        _core.mex([-1])


def test_cli_info(capsys):
    assert main(["info"]) == 0
    out = capsys.readouterr().out
    assert "rust core" in out


def test_cli_entry_point_help():
    result = subprocess.run(
        [sys.executable, "-m", "overthink.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "info" in result.stdout
