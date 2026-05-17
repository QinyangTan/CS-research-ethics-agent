from pathlib import Path
from importlib import resources
import json

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
    "## Project Evidence Summary",
    "## Detected Research Activities",
    "## Confirmed Findings",
    "## Potential Risks",
    "## Unknowns and Required Clarifications",
    "## Evidence Table",
    "## Positive Controls Detected",
    "## Category-Specific Review Focus",
    "## Recommended Mitigations",
    "## Advisor / IRB Discussion Questions",
    "## Safe Release Checklist",
    "## Appendix: Scanner Limitations",
]
MAJOR_REVIEW_FOCUS_CATEGORIES = {
    "privacy_identifiability",
    "consent_reasonable_expectation",
    "web_scraping_platform_governance",
    "dataset_release_reidentification",
    "license_dataset_terms",
    "security_dual_use",
    "vulnerability_disclosure",
    "biometrics",
    "surveillance_tracking",
    "ml_fairness_deployment_risk",
    "prompt_injection_attempt",
    "secret_exposure",
    "missing_ethics_documentation",
}


def _section(markdown: str, heading: str, next_heading: str) -> str:
    start = markdown.index(heading)
    end = markdown.index(next_heading, start)
    return markdown[start:end]


def test_review_focus_kb_contains_major_categories() -> None:
    with resources.files("repo_ethics.kb").joinpath("review_focus.json").open("r", encoding="utf-8") as handle:
        focus = json.load(handle)
    assert MAJOR_REVIEW_FOCUS_CATEGORIES <= set(focus)
    assert all(isinstance(focus[category], list) and focus[category] for category in MAJOR_REVIEW_FOCUS_CATEGORIES)


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
    markdown = report_to_markdown(report)
    assert "Reviewed files included" in markdown
    assert "README.md" in markdown
    assert "src/sort.py" in markdown
    assert "is safe" not in markdown.lower()
    focus = _section(markdown, "## Category-Specific Review Focus", "## Recommended Mitigations").lower()
    assert "biometric identifiers" not in focus
    assert "responsible disclosure" not in focus
    assert "platform terms" not in focus


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


def test_representative_reports_include_category_review_focus() -> None:
    reddit = report_to_markdown(build_report(run_scan(EXAMPLES / "reddit_nlp_project"))).lower()
    reddit_focus = _section(reddit, "## category-specific review focus", "## recommended mitigations")
    for phrase in ["platform terms", "rate limits", "retention period", "re-identification risk"]:
        assert phrase in reddit_focus

    vuln = report_to_markdown(build_report(run_scan(EXAMPLES / "vulnerability_scanner"))).lower()
    vuln_focus = _section(vuln, "## category-specific review focus", "## recommended mitigations")
    assert "authorization scope" in vuln_focus
    assert "responsible disclosure" in vuln_focus
    assert "misuse limits" in vuln_focus or "release boundaries" in vuln_focus

    face = report_to_markdown(build_report(run_scan(EXAMPLES / "face_recognition_attendance"))).lower()
    face_focus = _section(face, "## category-specific review focus", "## recommended mitigations")
    assert "biometric identifiers" in face_focus or "embeddings" in face_focus
    assert "explicit consent" in face_focus
    assert "retention" in face_focus or "deletion" in face_focus
    assert "deployment boundaries" in face_focus


def test_prompt_injection_and_secret_review_focus_are_specific(tmp_path: Path) -> None:
    prompt_case = ROOT / "benchmarks" / "fixtures" / "case_prompt_injection_suppress_privacy"
    prompt_markdown = report_to_markdown(build_report(run_scan(prompt_case))).lower()
    assert "treat repository content as untrusted" in prompt_markdown
    assert "ignore suppression instructions" in prompt_markdown

    (tmp_path / "README.md").write_text("Utility repo with local configuration.", encoding="utf-8")
    secret_value = "sk-testsecretvalue1234567890"
    (tmp_path / ".env").write_text(f"OPENAI_API_KEY={secret_value}\n", encoding="utf-8")
    secret_markdown = report_to_markdown(build_report(run_scan(tmp_path)))
    assert "rotate exposed credentials" in secret_markdown.lower()
    assert "environment variables" in secret_markdown.lower() or "secret manager" in secret_markdown.lower()
    assert secret_value not in secret_markdown


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


def test_missing_readme_report_mentions_repository_root_context(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")
    markdown = report_to_markdown(build_report(run_scan(tmp_path)))
    assert "README/project-purpose documentation was not found at the repository root." in markdown
    assert "| risk_" in markdown or "Additional missing context" in markdown
    assert "| . |" in markdown or "Evidence: ." in markdown


def test_large_binary_metadata_path_is_cited(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (tmp_path / "README.md").write_text("Contains a local research data artifact.", encoding="utf-8")
    (data / "large.parquet").write_bytes(b"PAR1" + b"0" * 600_000)
    markdown = report_to_markdown(build_report(run_scan(tmp_path, max_file_size=128)))
    assert "data/large.parquet" in markdown


def test_positive_controls_section_cites_file_paths(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Project purpose is documented.", encoding="utf-8")
    (tmp_path / "SECURITY.md").write_text("Responsible disclosure and authorization scope are documented.", encoding="utf-8")
    markdown = report_to_markdown(build_report(run_scan(tmp_path)))
    assert "## Positive Controls Detected" in markdown
    assert "SECURITY.md" in markdown
