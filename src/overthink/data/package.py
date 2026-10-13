# SPDX-License-Identifier: MIT
"""Package a dataset for publication (Zenodo / Hugging Face): data, card, manifest, sample,
license and SHA-256 checksums, verified against the committed manifest first."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from overthink.data.store import load


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def package(
    dataset: str,
    version: str,
    data_dir: Path = Path("data_out"),
    meta_dir: Path = Path("datasets"),
    out_dir: Path = Path("dist/datasets"),
) -> Path:
    manifest_path = meta_dir / dataset / "manifest.json"
    load(data_dir / dataset, manifest_path=manifest_path)  # raises on a content-hash mismatch
    dest = out_dir / f"{dataset}-v{version}"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    files = {
        "data.parquet": data_dir / dataset / "data.parquet",
        "README.md": meta_dir / dataset / "README.md",
        "manifest.json": manifest_path,
        "sample.parquet": meta_dir / dataset / "sample.parquet",
        "LICENSE": meta_dir / "LICENSE",
    }
    for name, src in files.items():
        shutil.copyfile(src, dest / name)
    sums = "".join(f"{_sha256(dest / n)}  {n}\n" for n in sorted(files))
    (dest / "SHA256SUMS").write_text(sums)
    (dest / "RELEASE.json").write_text(
        json.dumps(
            {
                "dataset": dataset,
                "version": version,
                "content_sha256": json.loads(manifest_path.read_text())["content_sha256"],
                "files": sorted([*files, "SHA256SUMS"]),
            },
            indent=2,
        )
        + "\n"
    )
    archive = out_dir / f"{dataset}-v{version}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dest.iterdir()):
            z.write(f, f"{dest.name}/{f.name}")
    return archive
