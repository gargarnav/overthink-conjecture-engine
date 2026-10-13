"""Dataset generation: schema, determinism, manifest and round-trip."""

import json
from pathlib import Path

import polars as pl
import pytest

from overthink.cli import main
from overthink.data.families import build
from overthink.data.schema import SCHEMAS, validate
from overthink.data.store import content_sha256, generate, load
from overthink.games import chomp

CONFIGS = {
    "chomp4": {"max_a": 25},
    "wythoff": {"n": 40},
    "subtraction": {"sets": [[1, 3, 4], [2, 5]], "all_subsets_of": 3, "n_max": 80},
    "wythoff_subtraction": {"sets": [[1], [2, 3]], "n": 20},
}


def _write_config(tmp_path: Path, family: str) -> Path:
    path = tmp_path / f"{family}.yaml"
    path.write_text(
        json.dumps({"dataset": f"t_{family}", "family": family, "params": CONFIGS[family]})
    )
    return path


@pytest.mark.parametrize("family", sorted(SCHEMAS))
def test_build_matches_schema_and_is_sorted(family):
    df = build(family, CONFIGS[family])
    validate(df, family)
    assert df.equals(df.sort(SCHEMAS[family].sort_by))


def test_subtraction_sets_deduplicated():
    df = build("subtraction", CONFIGS["subtraction"])
    # {1,3,4}, {2,5} + 7 subsets of {1,2,3} = 9 sets
    assert df["subtraction_set"].n_unique() == 9
    assert df.height == 9 * 81


def test_chomp4_dataset_matches_brute_force():
    df = build("chomp4", {"max_a": 15})
    assert set(df.iter_rows()) == chomp.p_positions_reference(4, 15)


@pytest.mark.parametrize("family", sorted(SCHEMAS))
def test_generate_is_deterministic_and_round_trips(tmp_path, family):
    cfg = _write_config(tmp_path, family)
    m1 = generate(cfg, out_dir=tmp_path / "out1", meta_dir=tmp_path / "meta1")
    m2 = generate(cfg, out_dir=tmp_path / "out2", meta_dir=tmp_path / "meta2")
    assert m1["content_sha256"] == m2["content_sha256"]
    ds = f"t_{family}"
    df = load(tmp_path / "out1" / ds, manifest_path=tmp_path / "meta1" / ds / "manifest.json")
    assert df.height == m1["row_count"]
    card = (tmp_path / "meta1" / ds / "README.md").read_text()
    assert m1["content_sha256"] in card
    sample = pl.read_parquet(tmp_path / "meta1" / ds / "sample.parquet")
    assert content_sha256(sample) == m1["sample_content_sha256"]


def test_load_detects_tampering(tmp_path):
    cfg = _write_config(tmp_path, "wythoff")
    generate(cfg, out_dir=tmp_path / "out", meta_dir=tmp_path / "meta")
    data = tmp_path / "out" / "t_wythoff" / "data.parquet"
    df = pl.read_parquet(data)
    df.with_columns(
        pl.when(pl.int_range(pl.len()) == 5)
        .then(99)
        .otherwise(pl.col("grundy"))
        .cast(pl.UInt32)
        .alias("grundy")
    ).write_parquet(data)
    with pytest.raises(ValueError, match="content hash mismatch"):
        load(
            tmp_path / "out" / "t_wythoff",
            manifest_path=tmp_path / "meta" / "t_wythoff" / "manifest.json",
        )


def test_cli_generate_and_verify(tmp_path, capsys):
    cfg = _write_config(tmp_path, "chomp4")
    out, meta = str(tmp_path / "out"), str(tmp_path / "meta")
    assert main(["generate", str(cfg), "--out", out, "--meta-dir", meta]) == 0
    assert main(["verify", "t_chomp4", "--out", out, "--meta-dir", meta]) == 0
    assert "OK" in capsys.readouterr().out


def test_content_hash_ignores_file_encoding():
    df = build("wythoff", {"n": 10})
    assert content_sha256(df) == content_sha256(pl.DataFrame(df.to_dict()))
    assert content_sha256(df) != content_sha256(df.with_columns(pl.col("grundy") + 1))
