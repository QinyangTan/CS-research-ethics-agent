"""Run the lightweight example benchmark."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "repo-ethics-mcp" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from repo_ethics.engine.report_builder import build_report  # noqa: E402
from repo_ethics.engine.scan_runner import run_scan  # noqa: E402


def main() -> int:
    cases = json.loads((ROOT / "eval" / "benchmark_cases.json").read_text(encoding="utf-8"))
    rows: list[tuple[str, int, int, int, str, str, str]] = []
    total_expected = 0
    total_found = 0
    total_false_positive = 0

    for case in cases:
        scan_result = run_scan(ROOT / case["path"])
        report = build_report(scan_result)
        risk_finding_categories = {finding.category for finding in report.findings if finding.status in {"confirmed", "potential"}}
        risk_signal_categories = {item.category for item in scan_result.evidence if item.evidence_type == "risk_signal"}
        missing_context_categories = {item.category for item in scan_result.evidence if item.evidence_type == "missing_context"}
        positive_control_categories = {item.category for item in scan_result.evidence if item.evidence_type == "positive_control"}
        risk_categories = risk_finding_categories | risk_signal_categories
        categories = risk_categories | missing_context_categories | positive_control_categories
        expected = set(case["expected_categories"])
        expected_missing = set(case.get("expected_missing_context_categories", []))
        absent = set(case["expected_absent_categories"])
        found = len(expected & risk_categories)
        false_positive = len(absent & risk_categories)
        missing_found = len(expected_missing & missing_context_categories)
        total_expected += len(expected)
        total_found += found
        total_false_positive += false_positive
        rows.append(
            (
                case["case_id"],
                found,
                len(expected),
                false_positive,
                f"{missing_found}/{len(expected_missing)}" if expected_missing else "n/a",
                ", ".join(sorted(positive_control_categories)) or "none",
                ", ".join(sorted(categories)),
            )
        )

    print("| Case | Expected Risk Recall | Missing Context Found | Expected-Absent False Positives | Positive Controls | Categories |")
    print("|---|---:|---:|---:|---|---|")
    for case_id, found, expected_count, false_positive, missing_found, positive_controls, categories in rows:
        print(f"| {case_id} | {found}/{expected_count} | {missing_found} | {false_positive} | {positive_controls} | {categories} |")

    recall = total_found / total_expected if total_expected else 1.0
    print(f"\nApproximate recall: {recall:.2%}")
    print(f"Expected-absent false positives: {total_false_positive}")
    return 0 if total_false_positive == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
