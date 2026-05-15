"""Run repo-ethics on benchmark fixtures without external API calls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "packages" / "repo-ethics-mcp" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from repo_ethics.engine.report_builder import build_report, report_to_json, report_to_markdown  # noqa: E402
from repo_ethics.engine.scan_runner import run_scan  # noqa: E402


def load_cases(cases_path: Path) -> list[dict]:
    cases: list[dict] = []
    with cases_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def run_benchmark(cases_path: Path, output_dir: Path, include_unreviewed: bool = False) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for case in load_cases(cases_path):
        if case.get("review_status") != "reviewed" and not include_unreviewed:
            continue
        case_id = case["case_id"]
        fixture_path = REPO_ROOT / case["fixture_path"]
        scan_result = run_scan(fixture_path)
        report = build_report(scan_result)
        markdown = report_to_markdown(report)
        json_report = report_to_json(report)
        (output_dir / f"{case_id}.md").write_text(markdown, encoding="utf-8")
        (output_dir / f"{case_id}.json").write_text(json_report, encoding="utf-8")
        (output_dir / f"{case_id}.scan.json").write_text(
            json.dumps(scan_result.model_dump(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(case_id)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Run repo-ethics benchmark reports over reviewed fixtures.")
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "benchmarks" / "cases" / "cs_ethics_cases.jsonl")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "benchmarks" / "outputs" / "repo_ethics")
    parser.add_argument("--include-unreviewed", action="store_true")
    args = parser.parse_args()
    written = run_benchmark(args.cases, args.output_dir, include_unreviewed=args.include_unreviewed)
    print(f"Wrote {len(written)} repo-ethics benchmark reports to {args.output_dir}")


if __name__ == "__main__":
    main()
