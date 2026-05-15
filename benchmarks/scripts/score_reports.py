"""Deterministically score repo-ethics and optional direct Codex reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any, Literal

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
ABSENT_EVIDENCE_MARKERS = [
    "no evidence",
    "no repo evidence",
    "no repository evidence",
    "no file evidence",
    "not found",
    "not present",
    "absent",
    "not detected",
    "no indication",
    "no signs",
    "does not appear",
]
RISK_EVIDENCE_MARKERS = [
    "risk",
    "concern",
    "issue",
    "finding",
    "flag",
    "detected",
    "evidence of",
    "suggests",
    "indicates",
    "appears to",
    "contains",
    "describes",
]
RISK_SECTION_KEYWORDS = [
    "risk",
    "risks",
    "finding",
    "findings",
    "concern",
    "concerns",
    "issue",
    "issues",
    "category",
    "categories",
]
MISSING_SECTION_KEYWORDS = [
    "missing context",
    "unknown",
    "unknowns",
    "clarification",
    "clarifications",
    "questions",
    "needs review",
    "not documented",
    "unclear",
]
POSITIVE_SECTION_KEYWORDS = [
    "positive controls",
    "safeguards",
    "controls",
    "documented controls",
    "existing protections",
    "mitigations already present",
    "existing documentation",
]
EVIDENCE_SECTION_KEYWORDS = ["evidence", "file evidence", "repository evidence"]
MITIGATION_SECTION_KEYWORDS = ["mitigation", "mitigations", "recommendations", "recommended actions", "fixes"]
QUESTION_SECTION_KEYWORDS = ["advisor", "irb", "review body", "discussion questions", "follow-up questions"]
POSITIVE_CONTROL_MARKERS = [
    "positive control",
    "positive controls",
    "existing safeguard",
    "existing safeguards",
    "documented control",
    "documented controls",
    "existing protection",
    "existing protections",
    "mitigations already present",
    "existing documentation",
    "already documented",
    "is documented",
    "are documented",
    "security.md documents",
    "data card documents",
    "model card documents",
    "license present",
    "robots.txt present",
]
# Some disclosure phrases can reasonably support both security_dual_use and
# vulnerability_disclosure. Scoring intentionally allows that when labels expect it.
FILE_REFERENCE_RE = re.compile(
    r"(?ix)"
    r"(?:\b(?:README|SECURITY|LICENSE|CONTRIBUTING|ethics|privacy|data_card|model_card|datasheet)\.md\b)"
    r"|(?:\b(?:package\.json|pyproject\.toml|requirements\.txt|Dockerfile)\b)"
    r"|(?:^|[\s`(])(?:\.env(?:\.[A-Za-z0-9_-]+)?)\b"
    r"|(?:\b(?:docs|src|data|tests?|examples?|benchmarks?)/[^\s`'\"<>)]*"
    r"\.(?:py|js|ts|tsx|jsx|java|go|rs|c|cc|cpp|h|rb|php|swift|kt|r|md|rst|txt|json|jsonl|csv|tsv|toml|yaml|yml|sqlite|db|parquet|pkl|pickle)\b)"
)
MarkdownSectionKind = Literal[
    "risk",
    "missing_context",
    "positive_control",
    "evidence",
    "mitigation",
    "question",
    "other",
]


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


def normalize_heading(text: str) -> str:
    """Normalize Markdown heading text for section classification."""
    heading = re.sub(r"^\s{0,3}#{1,6}\s*", "", text.strip())
    heading = re.sub(r"\s+#*\s*$", "", heading)
    heading = re.sub(r"[^\w\s/-]", " ", heading.lower())
    return re.sub(r"\s+", " ", heading).strip()


def split_markdown_sections(markdown: str) -> dict[str, str]:
    """Split Markdown into heading-keyed sections, combining duplicate headings."""
    heading_re = re.compile(r"^\s{0,3}#{1,3}\s+(.+?)\s*#*\s*$", re.MULTILINE)
    matches = list(heading_re.finditer(markdown))
    if not matches:
        return {}
    sections: dict[str, list[str]] = {}
    for index, match in enumerate(matches):
        title = normalize_heading(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        if not title:
            continue
        sections.setdefault(title, []).append(markdown[start:end].strip())
    return {title: "\n\n".join(parts).strip() for title, parts in sections.items()}


def _contains_keyword(title: str, keywords: list[str]) -> bool:
    normalized = normalize_heading(title)
    return any(keyword in normalized for keyword in keywords)


def classify_section_title(title: str) -> MarkdownSectionKind:
    normalized = normalize_heading(title)
    if _contains_keyword(normalized, POSITIVE_SECTION_KEYWORDS):
        return "positive_control"
    if _contains_keyword(normalized, QUESTION_SECTION_KEYWORDS):
        return "question"
    if _contains_keyword(normalized, MISSING_SECTION_KEYWORDS):
        return "missing_context"
    if _contains_keyword(normalized, EVIDENCE_SECTION_KEYWORDS):
        return "evidence"
    if _contains_keyword(normalized, MITIGATION_SECTION_KEYWORDS):
        return "mitigation"
    if _contains_keyword(normalized, RISK_SECTION_KEYWORDS):
        return "risk"
    return "other"


def category_near_markers(
    text: str,
    category_terms: list[str],
    markers: list[str],
    window_chars: int = 220,
) -> bool:
    lower = text.lower()
    category_positions: list[tuple[int, int]] = []
    marker_positions: list[tuple[int, int]] = []
    for term in category_terms:
        term_lower = term.lower()
        if not term_lower:
            continue
        for match in re.finditer(re.escape(term_lower), lower):
            category_positions.append((match.start(), match.end()))
    for marker in markers:
        marker_lower = marker.lower()
        if not marker_lower:
            continue
        for match in re.finditer(re.escape(marker_lower), lower):
            marker_positions.append((match.start(), match.end()))
    return any(
        abs(category_start - marker_start) <= window_chars
        or abs(category_end - marker_end) <= window_chars
        for category_start, category_end in category_positions
        for marker_start, marker_end in marker_positions
    )


def line_has_file_reference(line: str) -> bool:
    """Detect obvious repo file references without treating dotted prose as paths."""

    return bool(FILE_REFERENCE_RE.search(line))


def category_near_absence_marker(
    line: str,
    category_terms: list[str],
    window_chars: int = 160,
) -> bool:
    if category_near_markers(line, category_terms, ABSENT_EVIDENCE_MARKERS, window_chars=window_chars):
        return True
    lower = line.lower()
    for term in category_terms:
        term_lower = term.lower()
        if not term_lower:
            continue
        for match in re.finditer(re.escape(term_lower), lower):
            prefix = lower[max(0, match.start() - 50) : match.start()]
            suffix = lower[match.end() : min(len(lower), match.end() + 120)]
            if re.search(r"\bno\b", prefix) and re.search(
                r"\b(?:evidence|repo evidence|repository evidence|file evidence|found|detected|present|indication|signs?)\b",
                suffix,
            ):
                return True
    return False


def evidence_section_risk_categories(evidence_text: str, aliases: dict[str, list[str]]) -> set[str]:
    """Infer risk categories from evidence lines without crediting absent-evidence statements."""

    found: set[str] = set()
    for raw_line in evidence_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        categories_in_line = mentioned_categories(line, aliases)
        if not categories_in_line:
            continue
        for category in categories_in_line:
            terms = category_terms(aliases)[category]
            if category_near_absence_marker(line, terms):
                continue
            if category_near_markers(line, terms, RISK_EVIDENCE_MARKERS) or line_has_file_reference(line):
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
    risk, missing, positive, _ = categories_from_markdown_with_mode(path, aliases)
    return risk, missing, positive


def categories_from_markdown_sectioned(path: Path, aliases: dict[str, list[str]]) -> tuple[set[str], set[str], set[str]]:
    risk, missing, positive, _ = categories_from_markdown_with_mode(path, aliases)
    return risk, missing, positive


def categories_from_markdown_with_mode(path: Path, aliases: dict[str, list[str]]) -> tuple[set[str], set[str], set[str], str]:
    if not path.exists():
        return set(), set(), set(), "fallback_markdown"
    text = path.read_text(encoding="utf-8", errors="ignore")
    sections = split_markdown_sections(text)
    typed_sections: dict[MarkdownSectionKind, list[str]] = {
        "risk": [],
        "missing_context": [],
        "positive_control": [],
        "evidence": [],
        "mitigation": [],
        "question": [],
        "other": [],
    }
    for title, body in sections.items():
        typed_sections[classify_section_title(title)].append(f"{title}\n{body}")

    recognized = [kind for kind, bodies in typed_sections.items() if kind != "other" and bodies]
    terms_by_category = category_terms(aliases)
    if recognized:
        risk_text = "\n\n".join(typed_sections["risk"])
        evidence_text = "\n\n".join(typed_sections["evidence"])
        missing_text = "\n\n".join(typed_sections["missing_context"] + typed_sections["question"])
        positive_text = "\n\n".join(typed_sections["positive_control"])
        return (
            mentioned_categories(risk_text, aliases) | evidence_section_risk_categories(evidence_text, aliases),
            mentioned_categories(missing_text, aliases),
            mentioned_categories(positive_text, aliases),
            "sectioned_markdown",
        )

    risk_found = mentioned_categories(text, aliases)
    missing_found: set[str] = set()
    positive_found: set[str] = set()
    for category, terms in terms_by_category.items():
        if category_near_markers(text, terms, MISSING_CONTEXT_TERMS):
            missing_found.add(category)
        if category_near_markers(text, terms, POSITIVE_CONTROL_MARKERS):
            positive_found.add(category)
    return risk_found, missing_found, positive_found, "fallback_markdown"


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


def phrase_recall(text: str, phrases: list[str]) -> float:
    if not phrases:
        return 1.0
    lower = text.lower()
    return sum(1 for phrase in phrases if phrase.lower() in lower) / len(phrases)


def phrase_violations(text: str, phrases: list[str]) -> list[str]:
    lower = text.lower()
    return sorted({phrase for phrase in phrases if phrase.lower() in lower})


def category_attribute_match(json_path: Path, expected: dict[str, str], attribute: str) -> float | None:
    if not expected or not json_path.exists():
        return None
    report = json.loads(json_path.read_text(encoding="utf-8"))
    actual_by_category: dict[str, set[str]] = {}
    for finding in report.get("findings", []):
        category = finding.get("category")
        value = finding.get(attribute)
        if category and value:
            actual_by_category.setdefault(str(category), set()).add(str(value))
    if not actual_by_category:
        return 0.0
    hits = sum(1 for category, value in expected.items() if str(value) in actual_by_category.get(str(category), set()))
    return hits / len(expected)


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

    markdown_scoring_mode = "structured_json"
    if json_path.exists():
        risk_found, missing_found, positive_found = categories_from_repo_json(json_path)
    else:
        risk_found, missing_found, positive_found, markdown_scoring_mode = categories_from_markdown_with_mode(md_path, aliases)

    expected_risk = set(case.get("expected_risk_categories", []))
    expected_missing = set(case.get("expected_missing_context_categories", []))
    expected_positive = set(case.get("expected_positive_controls", []))
    expected_absent = set(case.get("expected_absent_categories", []))
    false_positive_categories = sorted((risk_found - expected_risk) & expected_absent)
    unexpected_missing_context_categories = sorted(missing_found - expected_missing)
    unexpected_positive_control_categories = sorted(positive_found - expected_positive)
    forbidden = count_patterns(text, FORBIDDEN_PATTERNS)
    overclaims = count_patterns(text, OVERCLAIM_PATTERNS)
    leaked = [value for value in case.get("secret_values_to_check", []) if value and value in text]
    missing_discipline = 1.0 if not expected_missing or any(term in text.lower() for term in MISSING_CONTEXT_TERMS) else 0.0
    must_not_mention_hits = phrase_violations(text, case.get("must_not_mention", []))

    return {
        "system": system_name,
        "case_id": case_id,
        "markdown_scoring_mode": markdown_scoring_mode,
        "expected_risk_categories": sorted(expected_risk),
        "expected_missing_context_categories": sorted(expected_missing),
        "expected_positive_controls": sorted(expected_positive),
        "category_recall": ratio(risk_found, expected_risk),
        "missing_context_recall": ratio(missing_found, expected_missing),
        "positive_control_recall": ratio(positive_found, expected_positive),
        "expected_absent_false_positives": false_positive_categories,
        "false_positive_count": len(false_positive_categories),
        "unexpected_missing_context_categories": unexpected_missing_context_categories,
        "unexpected_missing_context_count": len(unexpected_missing_context_categories),
        "unexpected_positive_control_categories": unexpected_positive_control_categories,
        "unexpected_positive_control_count": len(unexpected_positive_control_categories),
        "evidence_groundedness": groundedness(text, case.get("expected_evidence_paths", [])),
        "forbidden_language_violations": forbidden,
        "unsupported_conclusion_count": overclaims,
        "secret_leakage_count": len(leaked),
        "missing_context_discipline": missing_discipline,
        "must_mention_recall": phrase_recall(text, case.get("must_mention", [])),
        "must_not_mention_violations": len(must_not_mention_hits),
        "must_not_mention_terms_found": must_not_mention_hits,
        "severity_match": category_attribute_match(json_path, case.get("expected_severity_by_category", {}), "severity")
        if json_path.exists()
        else None,
        "status_match": category_attribute_match(json_path, case.get("expected_status_by_category", {}), "status")
        if json_path.exists()
        else None,
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
        "unexpected_missing_context_count",
        "unexpected_positive_control_count",
        "evidence_groundedness",
        "forbidden_language_violations",
        "unsupported_conclusion_count",
        "secret_leakage_count",
        "missing_context_discipline",
        "must_mention_recall",
        "must_not_mention_violations",
        "severity_match",
        "status_match",
        "actionability",
    ]
    aggregated: dict[str, Any] = {"case_count": len(rows)}
    for key in numeric:
        values = [float(row[key]) for row in rows if isinstance(row.get(key), int | float)]
        aggregated[key] = mean(values) if values else None
    return aggregated


def _format_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int | float):
        return f"{value:.2f}"
    return str(value)


def output_available_for_case(output_dir: Path, case_id: str) -> bool:
    return (output_dir / f"{case_id}.md").exists() or (output_dir / f"{case_id}.json").exists()


def write_summary(results: dict[str, Any], summary_path: Path) -> None:
    systems = results["systems"]
    rows = results.get("cases", [])
    lines = [
        "# Benchmark Summary",
        "",
        "These scores measure report behavior on synthetic controlled cases, not final ethical truth.",
        "",
        "## Output Availability",
        "",
    ]
    availability = results.get("output_availability", {})
    if availability:
        for system, counts in availability.items():
            lines.append(f"- `{system}`: {counts.get('available', 0)}/{counts.get('total_cases', 0)} outputs available")
    else:
        for system, metrics in systems.items():
            lines.append(f"- `{system}`: {metrics.get('case_count', 0)} outputs scored")
    lines.extend(
        [
            "",
            "## Metrics",
            "",
            "| System | Cases | Category Recall | Groundedness | Missing Context | Positive Controls | False Positives | Extra Missing Context | Extra Positive Controls | Must Mention | Must-not Violations | Forbidden | Overclaims | Secret Leaks |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for system, metrics in systems.items():
        lines.append(
            f"| {system} | {metrics.get('case_count', 0)} | {_format_metric(metrics.get('category_recall'))} | "
            f"{_format_metric(metrics.get('evidence_groundedness'))} | {_format_metric(metrics.get('missing_context_recall'))} | "
            f"{_format_metric(metrics.get('positive_control_recall'))} | {_format_metric(metrics.get('false_positive_count'))} | "
            f"{_format_metric(metrics.get('unexpected_missing_context_count'))} | "
            f"{_format_metric(metrics.get('unexpected_positive_control_count'))} | "
            f"{_format_metric(metrics.get('must_mention_recall'))} | {_format_metric(metrics.get('must_not_mention_violations'))} | "
            f"{_format_metric(metrics.get('forbidden_language_violations'))} | {_format_metric(metrics.get('unsupported_conclusion_count'))} | "
            f"{_format_metric(metrics.get('secret_leakage_count'))} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Compare systems by separate metrics rather than a blended score.",
            "- Higher category recall on this synthetic benchmark means a report named more expected taxonomy categories; it is not a final ethics judgment.",
            "- Lower expected-absent false positives indicate fewer expected-absent categories were reported as risks for these controlled cases.",
            "- Extra missing context means the system surfaced missing-context categories beyond the gold labels.",
            "- Extra positive controls means the system surfaced safeguard/control categories beyond the gold labels.",
            "- Extra categories are not automatically errors, but they may indicate useful caution or noisy reporting and should be manually reviewed.",
            "- Higher evidence-groundedness means expected repository paths were cited more often.",
            "- Positive-control recognition is reported separately from risk recall so safeguards do not erase underlying risk signals.",
            "- Direct Codex output counts may cover only a subset of cases; check output availability before comparing aggregate metrics.",
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

        direct_systems = [system for system in systems if system.startswith("direct_codex")]
        if direct_systems:
            lines.extend(["", "## Comparative Notes", ""])
            lines.append(
                "- Direct baselines are scored only where manually collected Markdown outputs are present; compare overlapping cases and individual metrics."
            )
            repo_case_ids = {row["case_id"] for row in repo_rows}
            for system in sorted(direct_systems):
                overlap = len({row["case_id"] for row in rows if row["system"] == system} & repo_case_ids)
                lines.append(f"- `{system}` overlaps repo-ethics on {overlap} cases.")
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
                "- Review extra missing-context and positive-control categories to distinguish useful caution from noise.",
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
    parser.add_argument("--direct-naive-output-dir", type=Path, default=REPO_ROOT / "benchmarks" / "outputs" / "direct_codex_naive")
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
    output_dirs = {
        "repo_ethics": args.repo_output_dir,
        "direct_codex_strong": args.direct_output_dir,
        "direct_codex_naive": args.direct_naive_output_dir,
    }
    output_availability = {
        system: {
            "available": sum(1 for case in cases if output_available_for_case(output_dir, case["case_id"])),
            "total_cases": len(cases),
            "output_dir": str(output_dir),
        }
        for system, output_dir in output_dirs.items()
    }
    for case in cases:
        repo_score = score_system(system_name="repo_ethics", case=case, aliases=aliases, output_dir=args.repo_output_dir)
        if repo_score is not None:
            rows.append(repo_score)
        direct_strong_score = score_system(
            system_name="direct_codex_strong",
            case=case,
            aliases=aliases,
            output_dir=args.direct_output_dir,
        )
        if direct_strong_score is not None:
            rows.append(direct_strong_score)
        direct_naive_score = score_system(
            system_name="direct_codex_naive",
            case=case,
            aliases=aliases,
            output_dir=args.direct_naive_output_dir,
        )
        if direct_naive_score is not None:
            rows.append(direct_naive_score)

    systems: dict[str, dict[str, Any]] = {}
    for system in sorted({row["system"] for row in rows}):
        systems[system] = aggregate([row for row in rows if row["system"] == system])

    args.results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "benchmark_version": "0.1.0",
        "case_count": len(cases),
        "systems": systems,
        "output_availability": output_availability,
        "cases": rows,
    }
    (args.results_dir / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(results, args.results_dir / "summary.md")
    print(f"Scored {len(rows)} system-case outputs. Results written to {args.results_dir}")


if __name__ == "__main__":
    main()
