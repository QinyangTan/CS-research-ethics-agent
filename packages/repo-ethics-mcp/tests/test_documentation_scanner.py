from pathlib import Path

from repo_ethics.scanners.documentation_scanner import scan


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples"


def test_harmless_project_does_not_get_broad_missing_doc_gaps() -> None:
    evidence = scan(EXAMPLES / "harmless_sorting_visualizer")
    missing_reasons = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context")
    assert "consent" not in missing_reasons.lower()
    assert "responsible disclosure" not in missing_reasons.lower()
    assert "platform terms" not in missing_reasons.lower()


def test_conditional_missing_docs_for_example_risks() -> None:
    vuln = scan(EXAMPLES / "vulnerability_scanner")
    vuln_missing = " ".join(item.reason for item in vuln if item.evidence_type == "missing_context")
    assert "responsible disclosure" in vuln_missing
    assert "authorization/scope" in vuln_missing

    face = scan(EXAMPLES / "face_recognition_attendance")
    face_missing = " ".join(item.reason for item in face if item.evidence_type == "missing_context")
    assert "consent" in face_missing
    assert "data retention" in face_missing
    assert "data access" in face_missing

    reddit = scan(EXAMPLES / "reddit_nlp_project")
    reddit_missing = " ".join(item.reason for item in reddit if item.evidence_type == "missing_context")
    assert "platform terms" in reddit_missing
    assert "data retention" in reddit_missing


def test_positive_controls_preserve_exact_file_paths(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    policy = docs / "privacy.md"
    policy.write_text(
        "This privacy note documents consent, data retention, data access controls, and anonymization.",
        encoding="utf-8",
    )
    readme = tmp_path / "README.md"
    readme.write_text("This project stores email addresses.", encoding="utf-8")
    evidence = scan(tmp_path)
    positive_paths = {item.file_path for item in evidence if item.evidence_type == "positive_control"}
    assert "docs/privacy.md" in positive_paths

