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
    "## Positive Controls Detected",
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
    assert "Evidence Type" in markdown
    assert "## Positive Controls Detected" in markdown


def test_golden_report_sections_and_forbidden_language() -> None:
    for case in ["reddit_nlp_project", "face_recognition_attendance", "vulnerability_scanner", "harmless_sorting_visualizer", "negated_docs_project"]:
        markdown = report_to_markdown(build_report(run_scan(EXAMPLES / case)))
        for section in REQUIRED_SECTIONS:
            assert section in markdown
        for phrase in FORBIDDEN_REPORT_PHRASES:
            assert phrase.lower() not in markdown.lower()


def test_harmless_sorting_visualizer_has_no_high_or_critical_findings() -> None:
    report = build_report(run_scan(EXAMPLES / "harmless_sorting_visualizer"))
    assert all(finding.severity not in {"high", "critical"} for finding in report.findings)
    broad_missing = " ".join(
        item.reason for finding in report.findings for item in finding.evidence if item.evidence_type == "missing_context"
    )
    assert "responsible disclosure" not in broad_missing.lower()
    assert "platform terms" not in broad_missing.lower()


def test_example_reports_have_case_specific_grounding() -> None:
    cases = {
        "reddit_nlp_project": [
            "web_scraping_platform_governance",
            "privacy_identifiability",
            "dataset_release_reidentification",
            "platform terms",
            "data retention",
        ],
        "vulnerability_scanner": ["security_dual_use", "responsible disclosure", "authorization"],
        "face_recognition_attendance": ["biometrics", "attendance", "consent", "data retention", "data access"],
    }
    for case, phrases in cases.items():
        markdown = report_to_markdown(build_report(run_scan(EXAMPLES / case)))
        lower = markdown.lower()
        for phrase in phrases:
            assert phrase.lower() in lower


def test_negated_docs_project_report_does_not_overread_negated_claims() -> None:
    markdown = report_to_markdown(build_report(run_scan(EXAMPLES / "negated_docs_project")))
    lower = markdown.lower()
    assert "username" not in lower
    assert "public dataset release risk" not in lower
    assert "platform terms" in lower
    assert "timestamp" in lower


def test_schema_export_available() -> None:
    schema = EthicsReviewReport.model_json_schema()
    assert schema["title"] == "EthicsReviewReport"
    assert "properties" in schema
    assert "positive_controls" in schema["properties"]


def test_report_does_not_include_full_secrets(tmp_path: Path) -> None:
    secret = "sk-" + "b" * 28
    (tmp_path / "config.py").write_text(f"API_KEY = '{secret}'\n", encoding="utf-8")
    markdown = report_to_markdown(build_report(run_scan(tmp_path)))
    assert secret not in markdown
    assert "[REDACTED_SECRET_LIKE_VALUE]" in markdown


def test_standalone_dataset_missing_context_appears_in_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Dataset release policy is not documented.", encoding="utf-8")
    report = build_report(run_scan(tmp_path))
    markdown = report_to_markdown(report)
    assert "dataset_release_reidentification" in markdown
    assert "Additional missing context for Dataset Release and Re-identification" in markdown
    assert "Dataset release or sharing is mentioned as absent, unclear, or not documented." in markdown
