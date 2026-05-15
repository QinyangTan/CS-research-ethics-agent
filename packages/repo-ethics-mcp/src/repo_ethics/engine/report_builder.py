"""Build JSON and Markdown ethics review reports."""

from __future__ import annotations

import json
from pathlib import Path

from repo_ethics.constants import DISCLAIMER, FORBIDDEN_REPORT_PHRASES, SAFE_RELEASE_CHECKLIST
from repo_ethics.engine.risk_mapper import map_risks
from repo_ethics.schemas import EthicsReviewReport, EvidenceItem, RiskFinding, ScanResult


def build_report(scan_result: ScanResult, include_low_confidence: bool = True) -> EthicsReviewReport:
    evidence = scan_result.evidence
    if not include_low_confidence:
        evidence = [item for item in evidence if item.confidence != "low"]
    findings = map_risks(scan_result.project_profile, evidence)
    positive_controls = [item for item in evidence if item.evidence_type == "positive_control"]
    global_missing_context = [
        "Project purpose, population, data provenance, consent/notice process, and intended release/deployment should be clarified when not documented."
    ]
    if not findings:
        global_missing_context.append(
            "The scanner found limited concrete ethics-risk evidence. A reviewer should still confirm the project description and data sources."
        )
    return EthicsReviewReport(
        project_profile=scan_result.project_profile,
        findings=findings,
        positive_controls=positive_controls,
        global_missing_context=global_missing_context,
        safe_release_checklist=SAFE_RELEASE_CHECKLIST,
        disclaimer=DISCLAIMER,
    )


def report_to_json(report: EthicsReviewReport) -> str:
    return json.dumps(report.model_dump(), indent=2, sort_keys=True)


def _fmt_evidence_ref(item: EvidenceItem) -> str:
    if item.line_start and item.line_end:
        if item.line_start == item.line_end:
            return f"{item.file_path}:{item.line_start}"
        return f"{item.file_path}:{item.line_start}-{item.line_end}"
    return item.file_path


def _finding_block(finding: RiskFinding) -> str:
    lines = [
        f"### {finding.title}",
        f"- Risk ID: `{finding.risk_id}`",
        f"- Category: `{finding.category}`",
        f"- Status: `{finding.status}`",
        f"- Severity: `{finding.severity}`",
        f"- Confidence: `{finding.confidence}`",
        f"- Why it matters: {finding.why_it_matters}",
    ]
    if finding.evidence:
        refs = ", ".join(_fmt_evidence_ref(item) for item in finding.evidence[:8])
        lines.append(f"- Evidence: {refs}")
    if finding.missing_context:
        lines.append("- Missing context: " + "; ".join(finding.missing_context))
    return "\n".join(lines)


def _findings_by_status(findings: list[RiskFinding], status: str) -> list[RiskFinding]:
    return [finding for finding in findings if finding.status == status]


def _section_for_findings(title: str, findings: list[RiskFinding]) -> str:
    if not findings:
        return f"## {title}\n\nNo findings in this section based on available repository evidence."
    return f"## {title}\n\n" + "\n\n".join(_finding_block(finding) for finding in findings)


def _evidence_table(findings: list[RiskFinding]) -> str:
    rows: list[str] = ["| Finding | Evidence Type | Category | Evidence | Reason | Snippet |", "|---|---|---|---|---|---|"]
    for finding in findings:
        for item in finding.evidence:
            snippet = (item.snippet or "").replace("\n", " ").replace("|", "\\|")
            reason = item.reason.replace("|", "\\|")
            rows.append(
                f"| {finding.risk_id} | `{item.evidence_type}` | `{item.category}` | `{_fmt_evidence_ref(item)}` | {reason} | {snippet} |"
            )
    if len(rows) == 2:
        rows.append("| None | none | none | none | No evidence rows were generated. | |")
    return "\n".join(rows)


def _positive_controls_section(positive_controls: list[EvidenceItem]) -> str:
    if not positive_controls:
        return "## Positive Controls Detected\n\nNo positive controls were detected from repository evidence."
    lines = ["## Positive Controls Detected", ""]
    for item in positive_controls:
        lines.append(f"- `{_fmt_evidence_ref(item)}`: `{item.category}` - {item.reason}")
    return "\n".join(lines)


def _unique_ordered(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def report_to_markdown(report: EthicsReviewReport) -> str:
    profile = report.project_profile
    confirmed = _findings_by_status(report.findings, "confirmed")
    potential = _findings_by_status(report.findings, "potential")
    unknown = _findings_by_status(report.findings, "unknown")

    mitigations = _unique_ordered(
        [mitigation for finding in report.findings for mitigation in finding.recommended_mitigations]
    )
    questions = _unique_ordered(
        [question for finding in report.findings for question in finding.advisor_or_irb_questions]
        + report.global_missing_context
    )

    lines = [
        "# CS Research Ethics Pre-Review Report",
        "",
        "## Disclaimer",
        "",
        report.disclaimer,
        "",
        "## Project Summary",
        "",
        f"- Project: `{profile.project_name}`",
        f"- Root path: `{profile.root_path}`",
        f"- Languages: {', '.join(profile.languages) if profile.languages else 'Not detected'}",
        f"- Important files: {', '.join(profile.important_files[:20]) if profile.important_files else 'Not detected'}",
        f"- Possible human data: {profile.possible_human_data}",
        f"- Possible security-sensitive or dual-use material: {profile.possible_security_sensitive or profile.possible_dual_use}",
        "",
        "## Detected Research Activities",
        "",
        "- Activities: " + (", ".join(profile.detected_research_activities) if profile.detected_research_activities else "Not detected from repository text"),
        "- Data sources: " + (", ".join(profile.detected_data_sources) if profile.detected_data_sources else "Not detected from repository text"),
        "",
        _section_for_findings("Confirmed Findings", confirmed),
        "",
        _section_for_findings("Potential Risks", potential),
        "",
        _section_for_findings("Unknowns and Required Clarifications", unknown),
        "",
        "## Evidence Table",
        "",
        _evidence_table(report.findings),
        "",
        _positive_controls_section(report.positive_controls),
        "",
        "## Recommended Mitigations",
        "",
        "\n".join(f"- {item}" for item in mitigations) if mitigations else "- No specific mitigations were generated from scanner evidence.",
        "",
        "## Advisor / IRB Discussion Questions",
        "",
        "\n".join(f"- {item}" for item in questions),
        "",
        "## Safe Release Checklist",
        "",
        "\n".join(f"- [ ] {item}" for item in report.safe_release_checklist),
        "",
        "## Appendix: Scanner Limitations",
        "",
        "- Static scanning can miss risks that depend on project intent, population, deployment setting, or data provenance.",
        "- Pattern matching can produce false positives and false negatives.",
        "- Repository text is treated as untrusted evidence, including README files and comments.",
        "- This report should support, not replace, advisor or appropriate review-body discussion.",
    ]
    markdown = "\n".join(lines).strip() + "\n"
    for phrase in FORBIDDEN_REPORT_PHRASES:
        if phrase.lower() in markdown.lower():
            raise ValueError(f"Forbidden report phrase generated: {phrase}")
    return markdown


def write_report(path: str | Path, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")
