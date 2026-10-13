# SPDX-License-Identifier: MIT
"""Dataset generation from a config file: Parquet + manifest + dataset card.

Layout of a generated dataset `<id>`:

    <out_dir>/<id>/data.parquet     full data (large; hosted separately, git-ignored)
    <meta_dir>/<id>/manifest.json   provenance and hashes (tracked in git)
    <meta_dir>/<id>/README.md       dataset card (tracked in git)
    <meta_dir>/<id>/sample.parquet  small sample (tracked in git)

`content_sha256` hashes the canonically sorted data column by column, so it is stable
across Parquet writers and library versions; `file_sha256` is the hash of the exact file.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
import yaml

from overthink import __version__, _core
from overthink.data.families import build
from overthink.data.schema import SCHEMA_VERSION, get_schema, validate

PARQUET_OPTS: dict[str, Any] = {"compression": "zstd", "compression_level": 9, "statistics": True}


def load_config(path: Path) -> dict[str, Any]:
    cfg = yaml.safe_load(path.read_text())
    for key in ("dataset", "family", "params"):
        if key not in cfg:
            raise ValueError(f"{path}: missing required key {key!r}")
    get_schema(cfg["family"])
    return cfg


def content_sha256(df: pl.DataFrame) -> str:
    """Hash of the data independent of file format: column name, then values as int64 LE
    (numeric) or newline-joined UTF-8 (strings), in canonical row order."""
    h = hashlib.sha256()
    for name in df.columns:
        col = df[name]
        h.update(name.encode() + b"\0")
        if col.dtype == pl.String:
            h.update("\n".join(col.to_list()).encode())
        else:
            h.update(col.cast(pl.Int64).to_numpy().astype("<i8").tobytes())
        h.update(b"\0")
    return h.hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return r.stdout.strip()


def provenance() -> dict[str, Any]:
    return {
        "git_sha": _git("rev-parse", "HEAD") or None,
        "git_dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "overthink_version": __version__,
        "rust_core_version": _core.core_version(),
        "polars_version": pl.__version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "command": " ".join(["overthink", *sys.argv[1:]]) if sys.argv else None,
    }


def generate(config_path: Path, out_dir: Path, meta_dir: Path) -> dict[str, Any]:
    """Generate one dataset from a config file. Returns the manifest."""
    cfg = load_config(config_path)
    ds_id, family, params = cfg["dataset"], cfg["family"], cfg["params"]
    schema = get_schema(family)

    t0 = time.perf_counter()
    df = build(family, params)
    seconds = time.perf_counter() - t0
    validate(df, family)

    data_dir, card_dir = out_dir / ds_id, meta_dir / ds_id
    data_dir.mkdir(parents=True, exist_ok=True)
    card_dir.mkdir(parents=True, exist_ok=True)
    data_path = data_dir / "data.parquet"
    df.write_parquet(data_path, **PARQUET_OPTS)
    sample = df.filter(schema.sample_filter)
    sample.write_parquet(card_dir / "sample.parquet", **PARQUET_OPTS)

    manifest = {
        "dataset": ds_id,
        "family": family,
        "description": cfg.get("description", ""),
        "params": params,
        "schema_version": SCHEMA_VERSION,
        "columns": {c.name: str(c.dtype) for c in schema.columns},
        "sort_order": list(schema.sort_by),
        "row_count": df.height,
        "content_sha256": content_sha256(df),
        "file_sha256": file_sha256(data_path),
        "file_bytes": data_path.stat().st_size,
        "sample_row_count": sample.height,
        "sample_content_sha256": content_sha256(sample),
        "random_seed": None,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "generation_seconds": round(seconds, 2),
        "config_path": str(config_path),
        "provenance": provenance(),
    }
    (card_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (card_dir / "README.md").write_text(render_card(manifest, cfg))
    return manifest


def load(data_dir: Path, manifest_path: Path | None = None) -> pl.DataFrame:
    """Load `data.parquet` from a dataset directory. If `manifest_path` is given, check the
    schema and content hash against it."""
    df = pl.read_parquet(data_dir / "data.parquet")
    if manifest_path is not None:
        manifest = json.loads(manifest_path.read_text())
        validate(df, manifest["family"])
        if content_sha256(df) != manifest["content_sha256"]:
            raise ValueError(f"content hash mismatch for {data_dir}")
    return df


def _human_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    raise AssertionError


def render_card(manifest: dict[str, Any], cfg: dict[str, Any]) -> str:
    schema = get_schema(manifest["family"])
    prov = manifest["provenance"]
    cols = "\n".join(f"| `{c.name}` | {c.dtype} | {c.description} |" for c in schema.columns)
    params = "\n".join(f"| `{k}` | `{v}` |" for k, v in manifest["params"].items())
    dirty = " (uncommitted changes present)" if prov["git_dirty"] else ""
    return f"""# Dataset card: `{manifest["dataset"]}`

*Auto-generated by `overthink generate`; do not edit by hand. Regenerate instead.*

{manifest["description"] or schema.title}

## Motivation

{cfg.get("motivation", "TODO: motivation not recorded in the dataset config.")}

## Game

**{schema.title}.** {schema.rules}

## Contents

{schema.contents}

| Parameter | Value |
|---|---|
{params}

| | |
|---|---|
| Rows | {manifest["row_count"]:,} |
| File size (Parquet, zstd) | {_human_bytes(manifest["file_bytes"])} |
| Sort order | {", ".join(manifest["sort_order"])} |
| Schema version | {manifest["schema_version"]} |

## Schema

| Column | Type | Meaning |
|---|---|---|
{cols}

## Integrity

- `content_sha256` (stable across Parquet writers): `{manifest["content_sha256"]}`
- `file_sha256` (this exact file): `{manifest["file_sha256"]}`
- Sample (`sample.parquet`, {schema.sample_description}): {manifest["sample_row_count"]:,} rows,
  `content_sha256` `{manifest["sample_content_sha256"]}`

## Reproduce

```bash
uv run overthink generate {manifest["config_path"]}
```

Random seeds: none. Generation is deterministic and took {manifest["generation_seconds"]} s.
Generated {manifest["generated_at"]} from git `{prov["git_sha"]}`{dirty} with overthink
{prov["overthink_version"]} (Rust core {prov["rust_core_version"]}), polars
{prov["polars_version"]}, Python {prov["python"]} on {prov["platform"]}.

## Validation

Solver correctness evidence is in `tests/test_games.py` and `docs/results_log.md`.

## Known limitations

{cfg.get("limitations", "TODO: limitations not recorded in the dataset config.")}

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (see `datasets/LICENSE`).
Code that generates it: MIT.

## Citation

Arnav Garg, *Overthink Conjecture Engine*, dataset `{manifest["dataset"]}` (schema
{manifest["schema_version"]}), https://github.com/gargarnav/overthink-conjecture-engine.
See `CITATION.cff`. Software DOI: 10.5281/zenodo.23350597 (all versions). Dataset DOI: TODO
(full data files are archived as a separate Zenodo dataset record).
{_ack_section()}"""


def _ack_section() -> str:
    from overthink.funding import acknowledgment

    ack = acknowledgment()
    return f"\n## Acknowledgment\n\n{ack}\n" if ack else ""
