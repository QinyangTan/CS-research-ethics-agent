"""Write the human-readable direct Codex vs repo-ethics comparison report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
COMPARISON_METRICS: list[tuple[str, str, str]] = [
    ("category_recall", "Category Recall", "higher"),
    ("evidence_groundedness", "Evidence Groundedness", "higher"),
    ("missing_context_recall", "Missing Context Recall", "higher"),
    ("positive_control_recall", "Positive Control Recall", "higher"),
    ("false_positive_count", "False Positives", "lower"),
    ("unexpected_missing_context_count", "Extra Missing Context", "lower"),
    ("unexpected_positive_control_count", "Extra Positive Controls", "lower"),
    ("forbidden_language_violations", "Forbidden Violations", "lower"),
    ("unsupported_conclusion_count", "Overclaims", "lower"),
    ("secret_leakage_count", "Secret Leaks", "lower"),
    ("must_mention_recall", "Must Mention Recall", "higher"),
    ("must_not_mention_violations", "Must-not Violations", "lower"),
    ("actionability", "Actionability", "higher"),
]


def _metric(metrics: dict[str, Any], key: str) -> str:
    value = metrics.get(key)
    if value is None:
        return "n/a"
    if isinstance(value, int | float):
        return f"{value:.2f}"
    return str(value)


def _availability(results: dict[str, Any], system: str) -> dict[str, Any]:
    return results.get("output_availability", {}).get(system, {"available": 0, "total_cases": results.get("case_count", 0)})


def _coverage_line(results: dict[str, Any]) -> str:
    strong = _availability(results, "direct_codex_strong")
    naive = _availability(results, "direct_codex_naive")
    return (
        f"{strong.get('available', 0)}/{strong.get('total_cases', results.get('case_count', 0))} strong, "
        f"{naive.get('available', 0)}/{naive.get('total_cases', results.get('case_count', 0))} naive"
    )


def _coverage_percent(available: int, total: int) -> str:
    if total == 0:
        return "n/a"
    return f"{(available / total) * 100:.2f}%"


def _comparison_status(results: dict[str, Any]) -> str:
    strong = _availability(results, "direct_codex_strong")
    naive = _availability(results, "direct_codex_naive")
    if strong.get("available", 0) == 0 and naive.get("available", 0) == 0:
        return "Inconclusive direct comparison"
    if strong.get("available", 0) < strong.get("total_cases", 0) or naive.get("available", 0) < naive.get("total_cases", 0):
        return "Partial direct comparison"
    return "Complete direct comparison"


def _system_rows(results: dict[str, Any]) -> list[str]:
    rows = []
    for system in ["repo_ethics", "direct_codex_strong", "direct_codex_naive"]:
        metrics = results.get("systems", {}).get(system, {})
        rows.append(
            f"| `{system}` | {_metric(metrics, 'category_recall')} | {_metric(metrics, 'evidence_groundedness')} | "
            f"{_metric(metrics, 'missing_context_recall')} | {_metric(metrics, 'positive_control_recall')} | "
            f"{_metric(metrics, 'false_positive_count')} | {_metric(metrics, 'unexpected_missing_context_count')} | "
            f"{_metric(metrics, 'unexpected_positive_control_count')} | {_metric(metrics, 'forbidden_language_violations')} | "
            f"{_metric(metrics, 'unsupported_conclusion_count')} | {_metric(metrics, 'secret_leakage_count')} |"
        )
    return rows


def _availability_rows(results: dict[str, Any]) -> list[str]:
    rows = []
    total_default = int(results.get("case_count", 0))
    for system in ["repo_ethics", "direct_codex_strong", "direct_codex_naive"]:
        counts = _availability(results, system)
        available = int(counts.get("available", 0))
        total = int(counts.get("total_cases", total_default))
        rows.append(f"| `{system}` | {available} | {total} | {_coverage_percent(available, total)} |")
    return rows


def _case_highlights(results: dict[str, Any]) -> list[str]:
    rows = results.get("cases", [])
    repo_rows = [row for row in rows if row.get("system") == "repo_ethics"]
    direct_by_system = {
        system: {row["case_id"]: row for row in rows if row.get("system") == system}
        for system in ["direct_codex_strong", "direct_codex_naive"]
    }
    highlights = sorted(
        repo_rows,
        key=lambda row: (row.get("category_recall", 0), row.get("evidence_groundedness", 0), -row.get("false_positive_count", 0)),
    )[:8]
    lines: list[str] = []
    for row in highlights:
        case_id = row["case_id"]
        strong = direct_by_system["direct_codex_strong"].get(case_id)
        naive = direct_by_system["direct_codex_naive"].get(case_id)
        note = "Repo-ethics row available."
        if strong is None and naive is None:
            note = "No direct baseline output."
        lines.append(
            f"| `{case_id}` | {row.get('category_recall', 0):.2f} | "
            f"{strong.get('category_recall', 'n/a') if strong else 'n/a'} | "
            f"{naive.get('category_recall', 'n/a') if naive else 'n/a'} | {note} |"
        )
    return lines


def _rows_by_case(results: dict[str, Any], system: str) -> dict[str, dict[str, Any]]:
    return {row["case_id"]: row for row in results.get("cases", []) if row.get("system") == system}


def _compare_values(repo_value: Any, direct_value: Any, direction: str) -> str | None:
    if not isinstance(repo_value, int | float) or not isinstance(direct_value, int | float):
        return None
    if abs(float(repo_value) - float(direct_value)) < 1e-9:
        return "tie"
    if direction == "lower":
        return "repo" if repo_value < direct_value else "direct"
    return "repo" if repo_value > direct_value else "direct"


def _comparison_rows(results: dict[str, Any], direct_system: str) -> list[str]:
    repo_rows = _rows_by_case(results, "repo_ethics")
    direct_rows = _rows_by_case(results, direct_system)
    overlapping = sorted(set(repo_rows) & set(direct_rows))
    lines: list[str] = [
        "| Metric | repo_ethics higher/better | "
        f"{direct_system} higher/better | tied | overlapping cases |",
        "|---|---:|---:|---:|---:|",
    ]
    for key, label, direction in COMPARISON_METRICS:
        repo_better = 0
        direct_better = 0
        tied = 0
        comparable = 0
        for case_id in overlapping:
            outcome = _compare_values(repo_rows[case_id].get(key), direct_rows[case_id].get(key), direction)
            if outcome is None:
                continue
            comparable += 1
            if outcome == "repo":
                repo_better += 1
            elif outcome == "direct":
                direct_better += 1
            else:
                tied += 1
        lines.append(f"| {label} | {repo_better} | {direct_better} | {tied} | {comparable} |")
    return lines


def write_report(results: dict[str, Any], output_path: Path, timestamp: str) -> None:
    status = _comparison_status(results)
    total_cases = int(results.get("case_count", 0))
    direct_available = (
        int(_availability(results, "direct_codex_strong").get("available", 0))
        + int(_availability(results, "direct_codex_naive").get("available", 0))
    )
    if direct_available == 0:
        comparison_note = "Not evaluated in this run because direct-Codex outputs were not available."
        empirical_answer = (
            "Inconclusive for direct comparison.\n\n"
            f"Repo-ethics outputs were generated and scored for all {total_cases} reviewed benchmark cases. "
            "However, no direct-Codex strong or naive Markdown outputs were available, so this run does not support claims "
            "that repo-ethics is better or worse than direct Codex.\n\n"
            "A valid comparison requires collecting direct Codex outputs for the same reviewed cases and rerunning the scorer."
        )
    else:
        comparison_note = "Evaluate only overlapping cases where both systems have outputs."
        empirical_answer = (
            "Mixed or partial direct comparison. Interpret only overlapping case-level metrics and output availability."
        )

    lines = [
        "# Direct Codex vs Repo-Ethics Benchmark Report",
        "",
        f"**Current empirical status:** {status}  ",
        f"**Direct baseline coverage:** {_coverage_line(results)}",
        "",
        "## Setup",
        "",
        "- Repository: `QinyangTan/CS-research-ethics-agent`",
        f"- Benchmark run timestamp: {timestamp}",
        f"- Benchmark version: `{results.get('benchmark_version', 'unknown')}`",
        f"- Reviewed synthetic cases: {total_cases}",
        "- Systems requested: `repo_ethics`, `direct_codex_strong`, `direct_codex_naive`",
        "- Prompts:",
        "  - Strong direct baseline: `benchmarks/prompts/direct_codex_prompt.md`",
        "  - Naive direct baseline: `benchmarks/prompts/direct_codex_naive_prompt.md`",
        "- Commands run:",
        "  - `python3 -m pip install -e packages/repo-ethics-mcp`",
        "  - `pytest`",
        "  - `python3 scripts/check_no_hosted_llm_calls.py`",
        "  - `python3 benchmarks/scripts/generate_fixtures.py`",
        "  - `python3 benchmarks/scripts/run_repo_ethics_benchmark.py`",
        "  - `python3 benchmarks/scripts/score_reports.py`",
        "  - `python3 benchmarks/scripts/summarize_results.py`",
        "  - `python3 benchmarks/scripts/write_direct_comparison_report.py`",
        "",
        "## Output Availability",
        "",
        "| System | Outputs Available | Reviewed Cases | Coverage |",
        "|---|---:|---:|---:|",
        *_availability_rows(results),
        "",
        "## Empirical Answer",
        "",
        empirical_answer,
        "",
        "## What Can Be Concluded From This Run",
        "",
        "This run can evaluate repo-ethics behavior on the reviewed synthetic cases.",
        "",
        "This run cannot determine whether repo-ethics performs better or worse than direct Codex when direct-Codex baseline outputs are unavailable.",
        "",
        "The benchmark infrastructure is ready for comparison once direct outputs are collected.",
        "",
        "## Aggregate Metrics",
        "",
        "These metrics are repo-ethics-only when direct outputs are absent; they are not comparative results in that case.",
        "",
        "| System | Category Recall | Evidence Groundedness | Missing Context Recall | Positive Control Recall | False Positives | Extra Missing Context | Extra Positive Controls | Forbidden Violations | Overclaims | Secret Leaks |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        *_system_rows(results),
        "",
        "## Metric-by-Metric Interpretation",
        "",
        "- Category recall measures expected risk categories found.",
        "- Evidence groundedness measures expected repository-path citation.",
        "- Missing-context recall and positive-control recall measure expected non-risk categories found.",
        "- False positives refer to expected-absent risk categories only.",
        "- Extra missing-context and positive-control categories are diagnostic. They are not counted as risk false positives, but high values may indicate over-cautious or noisy reporting.",
        "- Forbidden-language violations, unsupported conclusions, and secret leakage are report-discipline checks.",
        "",
        "## Overlapping Case Comparison",
        "",
        "Higher is better for recall, groundedness, must-mention recall, and actionability. Lower is better for false positives, extra missing context, extra positive controls, forbidden violations, overclaims, secret leaks, and must-not violations.",
        "",
        "### repo_ethics vs direct_codex_strong",
        "",
        *_comparison_rows(results, "direct_codex_strong"),
        "",
        "### repo_ethics vs direct_codex_naive",
        "",
        *_comparison_rows(results, "direct_codex_naive"),
        "",
        "## Where Repo-Ethics Performed Better",
        "",
        comparison_note,
        "",
        "## Where Direct Codex Performed Better",
        "",
        comparison_note,
        "",
        "## Inconclusive or Mixed Results",
        "",
        "- Direct output coverage may be incomplete or absent.",
        "- The fixtures are synthetic and intentionally small.",
        "- Direct Markdown scoring is heuristic and depends on taxonomy aliases.",
        "- The benchmark does not use an LLM-as-judge.",
        "- These scores measure report behavior on controlled cases, not final ethical truth.",
        "",
        "## Case-Level Highlights",
        "",
        "| Case ID | repo_ethics recall | strong direct recall | naive direct recall | notes |",
        "|---|---:|---:|---:|---|",
        *_case_highlights(results),
        "",
        "## Conclusion",
        "",
        "This run is inconclusive for direct comparison when direct baseline outputs are missing.",
        "",
        "Further comparison requires Markdown outputs in `benchmarks/outputs/direct_codex/` and/or `benchmarks/outputs/direct_codex_naive/`, followed by a fresh scoring run.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_collection_needed(results: dict[str, Any], output_path: Path) -> None:
    total = int(results.get("case_count", 0))
    strong = _availability(results, "direct_codex_strong")
    naive = _availability(results, "direct_codex_naive")
    if strong.get("available", 0) >= total and naive.get("available", 0) >= total:
        if output_path.exists():
            output_path.unlink()
        return
    output_path.write_text(
        """# Direct Baseline Collection Needed

Direct Codex baseline outputs were not collected for all reviewed cases in this run, so direct comparison is incomplete.

A direct comparison requires Markdown outputs in:

- Strong direct baseline: `benchmarks/outputs/direct_codex/<case_id>.md`
- Naive direct baseline: `benchmarks/outputs/direct_codex_naive/<case_id>.md`

Use the reviewed cases listed in `benchmarks/cases/cs_ethics_cases.jsonl`. For each case, review the corresponding fixture under `benchmarks/fixtures/<case_id>/` using only the appropriate direct prompt. Do not use repo-ethics scanner output or MCP tools to create direct baseline outputs.

Helpful commands:

```bash
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline naive
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline strong
python3 benchmarks/scripts/score_reports.py
python3 benchmarks/scripts/summarize_results.py
```

The placeholder commands print collection instructions by default. They do not run Codex unless an explicit `--direct-codex-command` template is supplied.

No superiority claim can be made until direct outputs are collected and scored against the same reviewed cases.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Write direct Codex vs repo-ethics benchmark report.")
    parser.add_argument("--results-json", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "results.json")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "benchmarks" / "results" / "direct_comparison_report.md")
    parser.add_argument(
        "--collection-needed-output",
        type=Path,
        default=REPO_ROOT / "benchmarks" / "results" / "direct_baseline_collection_needed.md",
    )
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z").strip())
    args = parser.parse_args()
    results = json.loads(args.results_json.read_text(encoding="utf-8"))
    write_report(results, args.output, args.timestamp)
    write_collection_needed(results, args.collection_needed_output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
