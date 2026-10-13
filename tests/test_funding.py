# SPDX-License-Identifier: MIT
"""The funding acknowledgment is only produced when funding is actually awarded."""

from overthink import funding


def test_repository_is_not_marked_funded():
    assert funding.is_funded() is False
    assert funding.acknowledgment() is None


def test_flag_switches_acknowledgment(tmp_path):
    f = tmp_path / "funding.yaml"
    f.write_text("funded: true\nacknowledgment: >-\n  Supported by X.\n")
    assert funding.acknowledgment(f) == "Supported by X."
    f.write_text("funded: false\nacknowledgment: Supported by X.\n")
    assert funding.acknowledgment(f) is None
