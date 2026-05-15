from pathlib import Path

from repo_ethics.constants import FORBIDDEN_REPORT_PHRASES
from repo_ethics.engine.report_builder import build_report, report_to_markdown
from repo_ethics.engine.scan_runner import run_scan
from repo_ethics.schemas import EthicsReviewReport


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples"
REQUIRED_SECTIONS = [
    "# CS Research Ethics Pre-Review Report",
    "## Disclaimer",
    "## Project Summary",
    "## Detected Research Activities",
    "## Confirmed Findings",
    "## Potential Risks",
    "## Unknowns and Required Clarifications",
    "## Evidence Table",
    "## Recommended Mitigations",
    "## Advisor / IRB Discussion Questions",
    "## Safe Release Checklist",
    "## Appendix: Scanner Limitations",
]


def test_report_builder_includes_evidence_and_disclaimer() -> None:
    scan_result = run_scan(EXAMPLES / "reddit_nlp_project")
    report = build_report(scan_result)
    markdown = report_to_markdown(report)
    assert "This is a local, evidence-grounded CS research ethics pre-review" in markdown
    assert "src/scraper.py" in markdown
    assert "Possible privacy and consent risk" in markdown


def test_golden_report_sections_and_forbidden_language() -> None:
    for case in ["reddit_nlp_project", "face_recognition_attendance", "vulnerability_scanner", "harmless_sorting_visualizer"]:
        markdown = report_to_markdown(build_report(run_scan(EXAMPLES / case)))
        for section in REQUIRED_SECTIONS:
            assert section in markdown
        for phrase in FORBIDDEN_REPORT_PHRASES:
            assert phrase.lower() not in markdown.lower()


def test_harmless_sorting_visualizer_has_no_high_or_critical_findings() -> None:
    report = build_report(run_scan(EXAMPLES / "harmless_sorting_visualizer"))
    assert all(finding.severity not in {"high", "critical"} for finding in report.findings)


def test_schema_export_available() -> None:
    schema = EthicsReviewReport.model_json_schema()
    assert schema["title"] == "EthicsReviewReport"
    assert "properties" in schema

