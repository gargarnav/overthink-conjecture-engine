"""Command-line entry point: `overthink <command>`."""

from __future__ import annotations

import argparse
import platform
import sys

from overthink import __version__


def _cmd_info(_args: argparse.Namespace) -> int:
    from overthink import _core

    print(f"overthink        {__version__}")
    print(f"rust core        {_core.core_version()}")
    print(f"python           {platform.python_version()}")
    print(f"platform         {platform.platform()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="overthink",
        description="Falsification-first conjecture discovery for combinatorial games.",
    )
    parser.add_argument("--version", action="version", version=f"overthink {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_info = sub.add_parser("info", help="show versions and check the Rust core loads")
    p_info.set_defaults(func=_cmd_info)

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
