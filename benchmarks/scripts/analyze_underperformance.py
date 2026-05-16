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

ROOT_CAUSE_BY_METRIC = {
    "category_recall": "missed_expected_category",
    "evidence_groundedness": "lower_groundedness",
    "missing_context_recall": "missed_expected_category",
    "positive_control_recall": "missed_expected_category",
    "false_positive_count": "false_positive",
    "unexpected_missing_context_count": "extra_missing_context_noise",
    "unexpected_positive_control_count": "extra_positive_control_noise",
    "must_mention_recall": "must_mention_gap",
    "actionability": "actionability_gap",
}
FOLLOW_UP_BY_BUCKET = {
    "missed_expected_category": "scanner precision or taxonomy mapping",
    "lower_groundedness": "report template",
    "extra_missing_context_noise": "scanner precision",
    "extra_positive_control_noise": "scanner precision",
    "must_mention_gap": "mitigation/question KB",
    "actionability_gap": "mitigation/question KB",
    "false_positive": "scanner precision",
    "report_discipline_issue": "report language policy",
}


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


def _gap(repo_value: Any, direct_value: Any, direction: str) -> float:
    if not isinstance(repo_value, int | float) or not isinstance(direct_value, int | float):
        return 0.0
    if direction == "lower":
        return abs(float(repo_value) - float(direct_value))
    return abs(float(direct_value) - float(repo_value))


def _category_fields(metric: str, repo_row: dict[str, Any], direct_row: dict[str, Any]) -> dict[str, Any]:
    if metric == "category_recall":
        expected = set(repo_row.get("expected_risk_categories", []))
        repo_found = set(repo_row.get("risk_categories_found", []))
        direct_found = set(direct_row.get("risk_categories_found", []))
        return {
            "expected_categories": sorted(expected),
            "repo_found_categories": sorted(repo_found),
            "direct_found_categories": sorted(direct_found),
            "missed_by_repo": sorted(expected - repo_found),
            "missed_by_direct": sorted(expected - direct_found),
        }
    if metric == "missing_context_recall":
        expected = set(repo_row.get("expected_missing_context_categories", []))
        repo_found = set(repo_row.get("missing_context_categories_found", []))
        direct_found = set(direct_row.get("missing_context_categories_found", []))
        return {
            "expected_missing_context_categories": sorted(expected),
            "repo_missing_context_found": sorted(repo_found),
            "direct_missing_context_found": sorted(direct_found),
            "missing_context_missed_by_repo": sorted(expected - repo_found),
            "missing_context_missed_by_direct": sorted(expected - direct_found),
        }
    if metric == "positive_control_recall":
        expected = set(repo_row.get("expected_positive_controls", []))
        repo_found = set(repo_row.get("positive_controls_found", []))
        direct_found = set(direct_row.get("positive_controls_found", []))
        return {
            "expected_positive_controls": sorted(expected),
            "repo_positive_controls_found": sorted(repo_found),
            "direct_positive_controls_found": sorted(direct_found),
            "positive_controls_missed_by_repo": sorted(expected - repo_found),
            "positive_controls_missed_by_direct": sorted(expected - direct_found),
        }
    if metric == "false_positive_count":
        return {
            "repo_false_positive_categories": repo_row.get("expected_absent_false_positives", []),
            "direct_false_positive_categories": direct_row.get("expected_absent_false_positives", []),
        }
    if metric == "unexpected_missing_context_count":
        return {
            "repo_unexpected_missing": repo_row.get("unexpected_missing_context_categories", []),
            "direct_unexpected_missing": direct_row.get("unexpected_missing_context_categories", []),
        }
    if metric == "unexpected_positive_control_count":
        return {
            "repo_unexpected_positive": repo_row.get("unexpected_positive_control_categories", []),
            "direct_unexpected_positive": direct_row.get("unexpected_positive_control_categories", []),
        }
    return {}


def _bucket_for_metric(metric: str) -> str:
    return ROOT_CAUSE_BY_METRIC.get(metric, "report_discipline_issue")


def _decorate_item(
    *,
    case_id: str,
    metric: str,
    direct_system: str,
    repo_row: dict[str, Any],
    direct_row: dict[str, Any],
    direction: str,
) -> dict[str, Any]:
    bucket = _bucket_for_metric(metric)
    item = {
        "case_id": case_id,
        "metric": metric,
        "repo_ethics": repo_row.get(metric),
        direct_system: direct_row.get(metric),
        "compared_to": direct_system,
        "root_cause_bucket": bucket,
        "likely_follow_up_area": FOLLOW_UP_BY_BUCKET.get(bucket, "manual review"),
        "gap": _gap(repo_row.get(metric), direct_row.get(metric), direction),
    }
    item.update(_category_fields(metric, repo_row, direct_row))
    return item


def _count_categories(items: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {
        "missed_expected_category": {},
        "extra_missing_context_noise": {},
        "extra_positive_control_noise": {},
        "false_positive": {},
    }
    for item in items:
        for category in item.get("missed_by_repo", []):
            counts["missed_expected_category"][category] = counts["missed_expected_category"].get(category, 0) + 1
        for category in item.get("missing_context_missed_by_repo", []):
            counts["missed_expected_category"][category] = counts["missed_expected_category"].get(category, 0) + 1
        for category in item.get("positive_controls_missed_by_repo", []):
            counts["missed_expected_category"][category] = counts["missed_expected_category"].get(category, 0) + 1
        for category in item.get("repo_unexpected_missing", []):
            counts["extra_missing_context_noise"][category] = counts["extra_missing_context_noise"].get(category, 0) + 1
        for category in item.get("repo_unexpected_positive", []):
            counts["extra_positive_control_noise"][category] = counts["extra_positive_control_noise"].get(category, 0) + 1
        for category in item.get("repo_false_positive_categories", []):
            counts["false_positive"][category] = counts["false_positive"].get(category, 0) + 1
    return counts


def _improvement_themes(repo_opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    themes: list[dict[str, Any]] = []
    category_counts = _count_categories(repo_opportunities)
    for bucket, categories in category_counts.items():
        for category, count in sorted(categories.items(), key=lambda pair: (-pair[1], pair[0])):
            themes.append(
                {
                    "theme": bucket.replace("_", " "),
                    "category": category,
                    "count": count,
                    "likely_follow_up_area": FOLLOW_UP_BY_BUCKET.get(bucket, "manual review"),
                }
            )

    bucket_counts: dict[str, int] = {}
    for item in repo_opportunities:
        bucket = str(item.get("root_cause_bucket", "report_discipline_issue"))
        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
    for bucket, count in sorted(bucket_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        if bucket in {"missed_expected_category", "extra_missing_context_noise", "extra_positive_control_noise", "false_positive"}:
            continue
        themes.append(
            {
                "theme": bucket.replace("_", " "),
                "category": None,
                "count": count,
                "likely_follow_up_area": FOLLOW_UP_BY_BUCKET.get(bucket, "manual review"),
            }
        )
    return themes[:10]


def analyze(results: dict[str, Any]) -> dict[str, Any]:
    repo_rows = _rows_by_case(results, "repo_ethics")
    output: dict[str, Any] = {
        "comparisons": {},
        "root_cause_buckets": {bucket: [] for bucket in sorted(set(ROOT_CAUSE_BY_METRIC.values()) | {"report_discipline_issue"})},
        "repo_ethics_worse_by_metric": {},
        "direct_worse_by_metric": {},
        "improvement_themes": [],
        "top_repo_ethics_improvement_opportunities": [],
        "top_direct_baseline_weaknesses": [],
    }

    repo_opportunities: list[dict[str, Any]] = []
    direct_weaknesses: list[dict[str, Any]] = []
    repo_worse_by_metric: dict[str, list[dict[str, Any]]] = {metric: [] for metric, _ in METRICS}
    direct_worse_by_metric: dict[str, list[dict[str, Any]]] = {metric: [] for metric, _ in METRICS}
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
                item = _decorate_item(
                    case_id=case_id,
                    metric=metric,
                    direct_system=direct_system,
                    repo_row=repo_row,
                    direct_row=direct_row,
                    direction=direction,
                )

                if outcome == "repo_better":
                    metric_result["repo_ethics_better"].append(item)
                    weakness = {"system": direct_system, **item}
                    direct_weaknesses.append(weakness)
                    direct_worse_by_metric[metric].append(weakness)
                elif outcome == "direct_better":
                    metric_result["repo_ethics_worse"].append(item)
                    repo_opportunities.append(item)
                    repo_worse_by_metric[metric].append(item)
                    output["root_cause_buckets"].setdefault(item["root_cause_bucket"], []).append(item)
                else:
                    metric_result["tied_count"] += 1
            comparison["metrics"][metric] = metric_result
        output["comparisons"][direct_system] = comparison

    output["repo_ethics_worse_by_metric"] = {key: value for key, value in repo_worse_by_metric.items() if value}
    output["direct_worse_by_metric"] = {key: value for key, value in direct_worse_by_metric.items() if value}
    output["improvement_themes"] = _improvement_themes(repo_opportunities)
    output["top_repo_ethics_improvement_opportunities"] = sorted(repo_opportunities, key=lambda item: item.get("gap", 0), reverse=True)[:10]
    output["top_direct_baseline_weaknesses"] = sorted(direct_weaknesses, key=lambda item: item.get("gap", 0), reverse=True)[:10]
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

    lines.extend(["## Root-Cause Buckets", ""])
    lines.append("| Bucket | Cases | Likely follow-up area |")
    lines.append("|---|---:|---|")
    for bucket, items in sorted(analysis.get("root_cause_buckets", {}).items()):
        lines.append(f"| `{bucket}` | {len(items)} | {FOLLOW_UP_BY_BUCKET.get(bucket, 'manual review')} |")
    lines.append("")

    lines.extend(["## Top Improvement Themes", ""])
    themes = analysis.get("improvement_themes", [])
    if themes:
        for theme in themes:
            category = f" for `{theme['category']}`" if theme.get("category") else ""
            lines.append(
                f"- {theme['theme']}{category}: {theme['count']} occurrence(s); "
                f"follow-up area: {theme['likely_follow_up_area']}."
            )
    else:
        lines.append("- No repeated improvement themes were identified.")
    lines.append("")

    lines.extend(["## Top Repo-Ethics Improvement Opportunities", ""])
    opportunities = analysis.get("top_repo_ethics_improvement_opportunities", [])
    if opportunities:
        for item in opportunities:
            lines.append(
                f"- `{item['case_id']}` vs `{item['compared_to']}` on `{item['metric']}`: "
                f"repo_ethics={_fmt_value(item.get('repo_ethics'))}, "
                f"direct={_fmt_value(item.get(item['compared_to']))}; "
                f"bucket=`{item.get('root_cause_bucket')}`, follow-up={item.get('likely_follow_up_area')}."
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
