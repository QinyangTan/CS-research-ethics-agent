"""Deterministically score repo-ethics and optional direct Codex reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_PATTERNS = [
    r"\bthis project is ethical\b",
    r"\bthis project is unethical\b",
    r"\birb approval is required\b",
    r"\bthis violates irb\b",
    r"\bthis is illegal\b",
    r"\bthis is compliant\b",
    r"\bthis is safe\b",
]
OVERCLAIM_PATTERNS = [
    r"\bclearly violates\b",
    r"\bdefinitely unethical\b",
    r"\bmust be approved by irb\b",
    r"\bno ethical issues\b",
    r"\bfully compliant\b",
    r"\bsafe to release\b",
]
ACTION_TERMS = [
    "anonymize",
    "anonymization",
    "hash",
    "remove identifiers",
    "rate limit",
    "robots.txt",
    "platform terms",
    "retention",
    "access control",
    "responsible disclosure",
    "model card",
    "data card",
    "bias evaluation",
    "deployment boundaries",
]
MISSING_CONTEXT_TERMS = ["unknown", "needs clarification", "not documented", "missing context", "may need", "unclear"]


def load_cases(cases_path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_yaml(path: Path) -> dict[str, list[str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(key): [str(item) for item in value] for key, value in data.items()}


def category_terms(aliases: dict[str, list[str]]) -> dict[str, list[str]]:
    return {category: [category, category.replace("_", " "), *terms] for category, terms in aliases.items()}


def mentioned_categories(text: str, aliases: dict[str, list[str]]) -> set[str]:
    lower = text.lower()
    found: set[str] = set()
    for category, terms in category_terms(aliases).items():
        if any(term.lower() in lower for term in terms):
            found.add(category)
    return found


def categories_from_repo_json(path: Path) -> tuple[set[str], set[str], set[str]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    risk_categories: set[str] = set()
    missing_categories: set[str] = set()
    positive_categories: set[str] = {item["category"] for item in report.get("positive_controls", [])}
    for finding in report.get("findings", []):
        evidence = finding.get("evidence", [])
        if finding.get("status") in {"confirmed", "potential"}:
            risk_categories.add(finding.get("category", ""))
        if finding.get("status") == "unknown":
            missing_categories.add(finding.get("category", ""))
        for item in evidence:
            if item.get("evidence_type") == "risk_signal":
                risk_categories.add(item.get("category", ""))
            elif item.get("evidence_type") == "missing_context":
                missing_categories.add(item.get("category", ""))
            elif item.get("evidence_type") == "positive_control":
                positive_categories.add(item.get("category", ""))
    scan_path = path.with_name(path.stem + ".scan.json")
    if scan_path.exists():
        scan_result = json.loads(scan_path.read_text(encoding="utf-8"))
        for item in scan_result.get("evidence", []):
            if item.get("evidence_type") == "risk_signal":
                risk_categories.add(item.get("category", ""))
            elif item.get("evidence_type") == "missing_context":
                missing_categories.add(item.get("category", ""))
            elif item.get("evidence_type") == "positive_control":
                positive_categories.add(item.get("category", ""))
    risk_categories.discard("")
    missing_categories.discard("")
    positive_categories.discard("")
    return risk_categories, missing_categories, positive_categories


def categories_from_markdown(path: Path, aliases: dict[str, list[str]]) -> tuple[set[str], set[str], set[str]]:
    if not path.exists():
        return set(), set(), set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    found = mentioned_categories(text, aliases)
    lower = text.lower()
    missing = set()
    positive = set()
    for category in found:
        terms = category_terms(aliases)[category]
        if any(term.lower() in lower and any(marker in lower for marker in MISSING_CONTEXT_TERMS) for term in terms):
            missing.add(category)
        if any(marker in lower for marker in ["positive controls", "documented", "rate limit", "robots.txt", "license", "data card", "model card", "responsible disclosure"]):
            positive.add(category)
    return found, missing, positive


def ratio(found: set[str], expected: set[str]) -> float:
    if not expected:
        return 1.0
    return len(found & expected) / len(expected)


def count_patterns(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.I)) for pattern in patterns)


def groundedness(text: str, expected_paths: list[str]) -> float:
    if not expected_paths:
        return 1.0
    lower = text.lower()
    return sum(1 for path in expected_paths if path.lower() in lower) / len(expected_paths)


def actionability(text: str) -> float:
    lower = text.lower()
    return min(1.0, sum(1 for term in ACTION_TERMS if term in lower) / 4)


def score_system(
    *,
    system_name: str,
    case: dict[str, Any],
    aliases: dict[str, list[str]],
    output_dir: Path,
) -> dict[str, Any] | None:
    case_id = case["case_id"]
    md_path = output_dir / f"{case_id}.md"
    json_path = output_dir / f"{case_id}.json"
    if not md_path.exists() and not json_path.exists():
        return None
    text = ""
    if md_path.exists():
        text += md_path.read_text(encoding="utf-8", errors="ignore")
    if json_path.exists():
        text += "\n" + json_path.read_text(encoding="utf-8", errors="ignore")

    if json_path.exists():
        risk_found, missing_found, positive_found = categories_from_repo_json(json_path)
    else:
        risk_found, missing_found, positive_found = categories_from_markdown(md_path, aliases)

    expected_risk = set(case.get("expected_risk_categories", []))
    expected_missing = set(case.get("expected_missing_context_categories", []))
    expected_positive = set(case.get("expected_positive_controls", []))
    expected_absent = set(case.get("expected_absent_categories", []))
    false_positive_categories = sorted((risk_found - expected_risk) & expected_absent)
    forbidden = count_patterns(text, FORBIDDEN_PATTERNS)
    overclaims = count_patterns(text, OVERCLAIM_PATTERNS)
    leaked = [value for value in case.get("secret_values_to_check", []) if value and value in text]
    missing_discipline = 1.0 if not expected_missing or any(term in text.lower() for term in MISSING_CONTEXT_TERMS) else 0.0

    return {
        "system": system_name,
        "case_id": case_id,
        "expected_risk_categories": sorted(expected_risk),
        "expected_missing_context_categories": sorted(expected_missing),
        "expected_positive_controls": sorted(expected_positive),
        "category_recall": ratio(risk_found, expected_risk),
        "missing_context_recall": ratio(missing_found, expected_missing),
        "positive_control_recall": ratio(positive_found, expected_positive),
        "expected_absent_false_positives": false_positive_categories,
        "false_positive_count": len(false_positive_categories),
        "evidence_groundedness": groundedness(text, case.get("expected_evidence_paths", [])),
        "forbidden_language_violations": forbidden,
        "unsupported_conclusion_count": overclaims,
        "secret_leakage_count": len(leaked),
        "missing_context_discipline": missing_discipline,
        "actionability": actionability(text),
        "risk_categories_found": sorted(risk_found),
        "missing_context_categories_found": sorted(missing_found),
        "positive_controls_found": sorted(positive_found),
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    numeric = [
        "category_recall",
        "missing_context_recall",
        "positive_control_recall",
        "false_positive_count",
        "evidence_groundedness",
        "forbidden_language_violations",
        "unsupported_conclusion_count",
        "secret_leakage_count",
        "missing_context_discipline",
        "actionability",
    ]
    return {key: mean(float(row[key]) for row in rows) for key in numeric} | {"case_count": len(rows)}


def write_summary(results: dict[str, Any], summary_path: Path) -> None:
    systems = results["systems"]
    rows = results.get("cases", [])
    lines = [
        "# Benchmark Summary",
        "",
        "This synthetic benchmark measures report quality and evidence grounding, not final ethical truth.",
        "",
        "| System | Cases | Category Recall | Groundedness | Missing Context | Positive Controls | False Positives | Forbidden | Overclaims | Secret Leaks |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for system, metrics in systems.items():
        lines.append(
            f"| {system} | {metrics.get('case_count', 0)} | {metrics.get('category_recall', 0):.2f} | "
            f"{metrics.get('evidence_groundedness', 0):.2f} | {metrics.get('missing_context_recall', 0):.2f} | "
            f"{metrics.get('positive_control_recall', 0):.2f} | {metrics.get('false_positive_count', 0):.2f} | "
            f"{metrics.get('forbidden_language_violations', 0):.2f} | {metrics.get('unsupported_conclusion_count', 0):.2f} | "
            f"{metrics.get('secret_leakage_count', 0):.2f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- On this benchmark, compare systems by separate metrics rather than a blended score.",
            "- Repo-ethics is expected to be strongest on deterministic evidence grounding, forbidden-language avoidance, positive-control recognition, and prompt-injection resistance.",
            "- Direct Codex outputs may be richer on unusual risks outside the scanner taxonomy when human-collected baseline reports are available.",
            "- The benchmark is synthetic and should be expanded with human-labeled real cases before drawing broad claims.",
        ]
    )

    if rows:
        lines.extend(["", "## Per-Category Recall", ""])
        categories = sorted({category for row in rows for category in row.get("expected_risk_categories", [])})
        lines.append("| Category | " + " | ".join(sorted(systems)) + " |")
        lines.append("|---|" + "|".join("---:" for _ in systems) + "|")
        for category in categories:
            values: list[str] = []
            for system in sorted(systems):
                relevant = [
                    row
                    for row in rows
                    if row["system"] == system and category in row.get("expected_risk_categories", [])
                ]
                if not relevant:
                    values.append("n/a")
                    continue
                hits = sum(1 for row in relevant if category in row.get("risk_categories_found", []))
                values.append(f"{hits}/{len(relevant)}")
            lines.append(f"| `{category}` | " + " | ".join(values) + " |")

        repo_rows = [row for row in rows if row["system"] == "repo_ethics"]
        hardest = sorted(
            repo_rows,
            key=lambda row: (row["category_recall"], row["evidence_groundedness"], -row["false_positive_count"]),
        )[:5]
        lines.extend(["", "## Hardest Repo-Ethics Cases", ""])
        if hardest:
            for row in hardest:
                lines.append(
                    f"- `{row['case_id']}`: recall {row['category_recall']:.2f}, "
                    f"groundedness {row['evidence_groundedness']:.2f}, false positives {row['false_positive_count']}."
                )
        else:
            lines.append("- No repo-ethics case outputs were available.")

        direct_rows = {row["case_id"]: row for row in rows if row["system"] == "direct_codex"}
        if direct_rows:
            lines.extend(["", "## Comparative Notes", ""])
            for repo_row in repo_rows:
                direct = direct_rows.get(repo_row["case_id"])
                if not direct:
                    continue
                if direct["category_recall"] > repo_row["category_recall"]:
                    lines.append(f"- Direct Codex did better on category recall for `{repo_row['case_id']}`.")
                elif direct["category_recall"] < repo_row["category_recall"]:
                    lines.append(f"- Repo-ethics did better on category recall for `{repo_row['case_id']}`.")
        else:
            lines.extend(["", "## Comparative Notes", "", "- No direct Codex baseline outputs were present, so comparative claims are not reported."])

        lines.extend(
            [
                "",
                "## Recommended Improvements",
                "",
                "- Review hardest cases manually before changing scanner logic.",
                "- Expand reviewed labels with real, permissioned teaching repositories.",
                "- Add aliases when direct baseline reports identify correct issues with different wording.",
                "- Keep positive-control and missing-context metrics separate from category recall.",
            ]
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score repo-ethics and optional direct Codex benchmark outputs.")
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "benchmarks" / "cases" / "cs_ethics_cases.jsonl")
    parser.add_argument("--gold-dir", type=Path, default=REPO_ROOT / "benchmarks" / "gold")
    parser.add_argument("--aliases", type=Path, default=REPO_ROOT / "benchmarks" / "category_aliases.yaml")
    parser.add_argument("--repo-output-dir", type=Path, default=REPO_ROOT / "benchmarks" / "outputs" / "repo_ethics")
    parser.add_argument("--direct-output-dir", type=Path, default=REPO_ROOT / "benchmarks" / "outputs" / "direct_codex")
    parser.add_argument("--results-dir", type=Path, default=REPO_ROOT / "benchmarks" / "results")
    parser.add_argument("--include-unreviewed", action="store_true")
    args = parser.parse_args()

    aliases = load_yaml(args.aliases)
    cases = []
    for row in load_cases(args.cases):
        gold_path = args.gold_dir / f"{row['case_id']}.json"
        if not gold_path.exists():
            continue
        gold = json.loads(gold_path.read_text(encoding="utf-8"))
        if gold.get("review_status") != "reviewed" and not args.include_unreviewed:
            continue
        cases.append(gold)

    rows: list[dict[str, Any]] = []
    for case in cases:
        repo_score = score_system(system_name="repo_ethics", case=case, aliases=aliases, output_dir=args.repo_output_dir)
        if repo_score is not None:
            rows.append(repo_score)
        direct_score = score_system(system_name="direct_codex", case=case, aliases=aliases, output_dir=args.direct_output_dir)
        if direct_score is not None:
            rows.append(direct_score)

    systems: dict[str, dict[str, Any]] = {}
    for system in sorted({row["system"] for row in rows}):
        systems[system] = aggregate([row for row in rows if row["system"] == system])

    args.results_dir.mkdir(parents=True, exist_ok=True)
    results = {"benchmark_version": "0.1.0", "case_count": len(cases), "systems": systems, "cases": rows}
    (args.results_dir / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(results, args.results_dir / "summary.md")
    print(f"Scored {len(rows)} system-case outputs. Results written to {args.results_dir}")


if __name__ == "__main__":
    main()
