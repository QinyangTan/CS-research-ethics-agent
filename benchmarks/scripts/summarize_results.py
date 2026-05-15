"""Regenerate a Markdown benchmark summary from results.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from score_reports import write_summary


REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Write benchmark summary.md from results.json.")
    parser.add_argument("--results-json", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "results.json")
    parser.add_argument("--summary", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "summary.md")
    args = parser.parse_args()
    results = json.loads(args.results_json.read_text(encoding="utf-8"))
    write_summary(results, args.summary)
    print(f"Wrote {args.summary}")


if __name__ == "__main__":
    main()
