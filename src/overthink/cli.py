"""Command-line entry point: `overthink <command>`."""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

from overthink import __version__


def _cmd_info(_args: argparse.Namespace) -> int:
    from overthink import _core

    print(f"overthink        {__version__}")
    print(f"rust core        {_core.core_version()}")
    print(f"python           {platform.python_version()}")
    print(f"platform         {platform.platform()}")
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    from overthink.data.store import generate

    for config in args.configs:
        m = generate(config, out_dir=args.out, meta_dir=args.meta_dir)
        print(
            f"{m['dataset']}: {m['row_count']:,} rows, {m['file_bytes'] / 1e6:.1f} MB, "
            f"{m['generation_seconds']} s, content_sha256 {m['content_sha256'][:16]}…"
        )
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    from overthink.data.store import load

    status = 0
    for ds in args.datasets:
        try:
            df = load(args.out / ds, manifest_path=args.meta_dir / ds / "manifest.json")
            print(f"{ds}: OK ({df.height:,} rows)")
        except (FileNotFoundError, ValueError) as e:
            print(f"{ds}: FAILED: {e}")
            status = 1
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="overthink",
        description="Falsification-first conjecture discovery for combinatorial games.",
    )
    parser.add_argument("--version", action="version", version=f"overthink {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_info = sub.add_parser("info", help="show versions and check the Rust core loads")
    p_info.set_defaults(func=_cmd_info)

    p_gen = sub.add_parser("generate", help="generate datasets from YAML config files")
    p_gen.add_argument("configs", nargs="+", type=Path, metavar="CONFIG")
    p_gen.add_argument("--out", type=Path, default=Path("data_out"), help="data directory")
    p_gen.add_argument(
        "--meta-dir", type=Path, default=Path("datasets"), help="card/manifest/sample directory"
    )
    p_gen.set_defaults(func=_cmd_generate)

    p_ver = sub.add_parser("verify", help="check generated data against its manifest hash")
    p_ver.add_argument("datasets", nargs="+", metavar="DATASET_ID")
    p_ver.add_argument("--out", type=Path, default=Path("data_out"), help="data directory")
    p_ver.add_argument("--meta-dir", type=Path, default=Path("datasets"), help="manifest directory")
    p_ver.set_defaults(func=_cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
