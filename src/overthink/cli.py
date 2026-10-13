"""Command-line entry point: `overthink <command>`."""

from __future__ import annotations

import argparse
import json
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


def _cmd_mine(args: argparse.Namespace) -> int:
    from overthink.conjecture.run import run_mining

    run_dir = run_mining(args.config, runs_dir=args.runs_dir, data_dir=args.data_dir)
    info = json.loads((run_dir / "run.json").read_text())
    for d in info["datasets"]:
        print(
            f"{d['id']}: {d['sequences']} sequences (+{d['second_order_sequences']} "
            f"second-order), {d['candidates']} candidates, {d['seconds']} s"
        )
    print(f"by kind: {info['counts_by_kind']}")
    print(f"run written to {run_dir}")
    return 0


def _cmd_benchmark(args: argparse.Namespace) -> int:
    import yaml

    from overthink.conjecture.benchmark import run_benchmark

    cfg = yaml.safe_load(args.config.read_text()) if args.config else {}
    miners = cfg.get("miners", {})
    report = run_benchmark(miners, n_per_family=args.n, seed=args.seed)
    cols = ["n", "recovered", "exact", "wrong", "other_true", "silent", "candidates"]
    lines = [
        f"# Miner benchmark (n={args.n} per family, seed={args.seed}, scale 10x)",
        "",
        f"Config: `{args.config}`" if args.config else "Config: defaults",
        "",
        "| Family | " + " | ".join(cols) + " |",
        "|---|" + "---|" * len(cols),
    ]
    for fam, st in report.items():
        lines.append(f"| {fam} | " + " | ".join(str(st.get(c, 0)) for c in cols) + " |")
    text = "\n".join(lines) + "\n"
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
        args.out.with_suffix(".json").write_text(json.dumps(report, indent=2, default=str))
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

    p_mine = sub.add_parser("mine", help="run the classical miners from a YAML config")
    p_mine.add_argument("config", type=Path)
    p_mine.add_argument("--runs-dir", type=Path, default=Path("experiments/runs"))
    p_mine.add_argument("--data-dir", type=Path, default=Path("data_out"))
    p_mine.set_defaults(func=_cmd_mine)

    p_bench = sub.add_parser("benchmark", help="benchmark miners on planted synthetic data")
    p_bench.add_argument("--config", type=Path, help="mining config (uses its 'miners')")
    p_bench.add_argument("--n", type=int, default=200, help="sequences per family")
    p_bench.add_argument("--seed", type=int, default=7)
    p_bench.add_argument("--out", type=Path, help="write markdown (+ .json) report here")
    p_bench.set_defaults(func=_cmd_benchmark)

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
