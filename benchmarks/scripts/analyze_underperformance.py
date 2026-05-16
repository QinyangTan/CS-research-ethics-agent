"""Analyze benchmark metrics where systems underperform each other."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
METRICS: list[tuple[str, str]] = [
    ("category_recall", "higher"),
    ("evidence_groundedness", "higher"),
    ("missing_context_recall", "higher"),
    ("positive_control_recall", "higher"),
    ("false_positive_count", "lower"),
    ("unexpected_missing_context_count", "lower"),
    ("unexpected_positive_control_count", "lower"),
    ("must_mention_recall", "higher"),
    ("actionability", "higher"),
]
DIRECT_SYSTEMS = ["direct_codex_strong", "direct_codex_naive"]


def _rows_by_case(results: dict[str, Any], system: str) -> dict[str, dict[str, Any]]:
    return {row["case_id"]: row for row in results.get("cases", []) if row.get("system") == system}


def _compare(repo_value: Any, direct_value: Any, direction: str) -> str | None:
    if not isinstance(repo_value, int | float) or not isinstance(direct_value, int | float):
        return None
    if abs(float(repo_value) - float(direct_value)) < 1e-9:
        return "tie"
    if direction == "lower":
        return "repo_better" if repo_value < direct_value else "direct_better"
    return "repo_better" if repo_value > direct_value else "direct_better"


def analyze(results: dict[str, Any]) -> dict[str, Any]:
    repo_rows = _rows_by_case(results, "repo_ethics")
    output: dict[str, Any] = {"comparisons": {}, "top_repo_ethics_improvement_opportunities": [], "top_direct_baseline_weaknesses": []}

    repo_opportunities: list[dict[str, Any]] = []
    direct_weaknesses: list[dict[str, Any]] = []
    for direct_system in DIRECT_SYSTEMS:
        direct_rows = _rows_by_case(results, direct_system)
        overlap = sorted(set(repo_rows) & set(direct_rows))
        comparison: dict[str, Any] = {"overlapping_cases": len(overlap), "metrics": {}}
        for metric, direction in METRICS:
            metric_result = {"repo_ethics_worse": [], "repo_ethics_better": [], "tied_count": 0}
            for case_id in overlap:
                repo_row = repo_rows[case_id]
                direct_row = direct_rows[case_id]
                outcome = _compare(repo_row.get(metric), direct_row.get(metric), direction)
                if outcome is None:
                    continue
                item = {
                    "case_id": case_id,
                    "repo_ethics": repo_row.get(metric),
                    direct_system: direct_row.get(metric),
                }
                if metric == "category_recall":
                    expected = set(repo_row.get("expected_risk_categories", []))
                    repo_found = set(repo_row.get("risk_categories_found", []))
                    direct_found = set(direct_row.get("risk_categories_found", []))
                    item.update(
                        {
                            "expected_categories": sorted(expected),
                            "repo_found_categories": sorted(repo_found),
                            "direct_found_categories": sorted(direct_found),
                            "missed_by_repo": sorted(expected - repo_found),
                            "missed_by_direct": sorted(expected - direct_found),
                        }
                    )
                if metric == "false_positive_count":
                    item["repo_false_positive_categories"] = repo_row.get("expected_absent_false_positives", [])
                    item["direct_false_positive_categories"] = direct_row.get("expected_absent_false_positives", [])
                if metric == "unexpected_missing_context_count":
                    item["repo_unexpected_missing"] = repo_row.get("unexpected_missing_context_categories", [])
                    item["direct_unexpected_missing"] = direct_row.get("unexpected_missing_context_categories", [])
                if metric == "unexpected_positive_control_count":
                    item["repo_unexpected_positive"] = repo_row.get("unexpected_positive_control_categories", [])
                    item["direct_unexpected_positive"] = direct_row.get("unexpected_positive_control_categories", [])

                if outcome == "repo_better":
                    metric_result["repo_ethics_better"].append(item)
                    direct_weaknesses.append({"system": direct_system, "metric": metric, **item})
                elif outcome == "direct_better":
                    metric_result["repo_ethics_worse"].append(item)
                    repo_opportunities.append({"compared_to": direct_system, "metric": metric, **item})
                else:
                    metric_result["tied_count"] += 1
            comparison["metrics"][metric] = metric_result
        output["comparisons"][direct_system] = comparison

    output["top_repo_ethics_improvement_opportunities"] = repo_opportunities[:10]
    output["top_direct_baseline_weaknesses"] = direct_weaknesses[:10]
    return output


def _fmt_value(value: Any) -> str:
    if isinstance(value, int | float):
        return f"{value:.2f}"
    return str(value)


def write_markdown(analysis: dict[str, Any], path: Path) -> None:
    lines = [
        "# Benchmark Underperformance Analysis",
        "",
        "This analysis is diagnostic. It should guide general scanner/report improvements, not case-specific rules.",
        "",
        "Scores are heuristic benchmark diagnostics, not final ethical truth.",
        "",
    ]
    for direct_system, comparison in analysis.get("comparisons", {}).items():
        lines.extend([f"## repo_ethics vs {direct_system}", "", f"- Overlapping cases: {comparison.get('overlapping_cases', 0)}", ""])
        lines.append("| Metric | repo_ethics worse | repo_ethics better | tied |")
        lines.append("|---|---:|---:|---:|")
        for metric, data in comparison.get("metrics", {}).items():
            lines.append(
                f"| `{metric}` | {len(data.get('repo_ethics_worse', []))} | "
                f"{len(data.get('repo_ethics_better', []))} | {data.get('tied_count', 0)} |"
            )
        lines.append("")

    lines.extend(["## Top Repo-Ethics Improvement Opportunities", ""])
    opportunities = analysis.get("top_repo_ethics_improvement_opportunities", [])
    if opportunities:
        for item in opportunities:
            lines.append(
                f"- `{item['case_id']}` vs `{item['compared_to']}` on `{item['metric']}`: "
                f"repo_ethics={_fmt_value(item.get('repo_ethics'))}, "
                f"direct={_fmt_value(item.get(item['compared_to']))}."
            )
    else:
        lines.append("- No repo-ethics underperformance cases were identified for compared metrics.")

    lines.extend(["", "## Top Direct Baseline Weaknesses", ""])
    weaknesses = analysis.get("top_direct_baseline_weaknesses", [])
    if weaknesses:
        for item in weaknesses:
            lines.append(
                f"- `{item['case_id']}` for `{item['system']}` on `{item['metric']}`: "
                f"repo_ethics={_fmt_value(item.get('repo_ethics'))}, "
                f"direct={_fmt_value(item.get(item['system']))}."
            )
    else:
        lines.append("- No direct baseline underperformance cases were identified for compared metrics.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze repo-ethics and direct-baseline benchmark underperformance.")
    parser.add_argument("--results-json", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "results.json")
    parser.add_argument("--output-json", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "underperformance_analysis.json")
    parser.add_argument("--output-md", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "underperformance_analysis.md")
    args = parser.parse_args()

    results = json.loads(args.results_json.read_text(encoding="utf-8"))
    analysis = analyze(results)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(analysis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(analysis, args.output_md)
    print(f"Wrote {args.output_json} and {args.output_md}")


if __name__ == "__main__":
    main()
