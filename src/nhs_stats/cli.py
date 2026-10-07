"""Command line entry point."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from nhs_stats import pipeline
from nhs_stats.paths import DataPaths
from nhs_stats.quality import QualityGateError

_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _month(value: str) -> str:
    if not _MONTH.match(value):
        raise argparse.ArgumentTypeError("expected YYYY-MM")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nhs-stats", description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, help="Data root (default: $NHS_STATS_DATA_DIR or ./data)"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    fetch = commands.add_parser("fetch", help="Store a monthly A&E CSV in bronze")
    fetch.add_argument("--month", type=_month, required=True)
    fetch.add_argument(
        "--status", default="provisional", choices=["provisional", "revised", "final"]
    )
    origin = fetch.add_mutually_exclusive_group(required=True)
    origin.add_argument("--url", help="Public URL of the monthly CSV")
    origin.add_argument("--file", type=Path, help="Local CSV, for offline use")

    build = commands.add_parser("build", help="Bronze to silver, with quality gate")
    build.add_argument("--month", type=_month, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = DataPaths.from_env(args.data_dir)

    if args.command == "fetch":
        if args.url:
            stored = pipeline.ingest_url(args.url, args.month, paths, status=args.status)
        else:
            stored = pipeline.ingest_file(args.file, args.month, paths, status=args.status)
        print(f"bronze: {stored.path} ({stored.sha256[:12]})")
        return 0

    try:
        result = pipeline.build(args.month, paths)
    except QualityGateError as error:
        print(f"quality gate failed: {error}", file=sys.stderr)
        return 1
    for check in result.results:
        flag = "ok " if check.passed else check.severity
        print(f"[{flag}] {check.name}")
    print(f"silver: {result.silver_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
