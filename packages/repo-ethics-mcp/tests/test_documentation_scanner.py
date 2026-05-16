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


def test_positive_control_uses_first_doc_with_topic_not_later_doc(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    first = docs / "01-privacy.md"
    first.write_text("This privacy note documents consent for email data collection.", encoding="utf-8")
    later = docs / "99-unrelated.md"
    later.write_text("This unrelated note discusses project setup only.", encoding="utf-8")
    readme = tmp_path / "README.md"
    readme.write_text("This project stores email addresses.", encoding="utf-8")

    evidence = scan(tmp_path)
    consent_controls = [
        item
        for item in evidence
        if item.evidence_type == "positive_control" and "consent/reasonable expectation" in item.reason
    ]
    assert consent_controls
    assert {item.file_path for item in consent_controls} == {"docs/01-privacy.md"}


def test_docs_tutorial_security_terms_do_not_trigger_security_requirements(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "security_tutorial.md").write_text(
        "This tutorial explains what a vulnerability scanner is in general.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context")
    assert "responsible disclosure" not in missing.lower()
    assert "authorization/scope" not in missing.lower()


def test_readme_security_signal_triggers_security_requirements(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("This is a vulnerability scanner.", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context")
    assert "responsible disclosure" in missing.lower()
    assert "authorization/scope" in missing.lower()


def test_tests_security_terms_do_not_trigger_requirements(tmp_path: Path) -> None:
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_security.py").write_text("# exploit regression fixture text only\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("This project visualizes sorting algorithms.", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context")
    assert "responsible disclosure" not in missing.lower()


def test_source_socket_scanning_triggers_security_requirements(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "scanner.py").write_text("import socket\nsock = socket.socket(); sock.connect_ex(('host', 80))\n", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context")
    assert "responsible disclosure" in missing.lower()
    assert "authorization/scope" in missing.lower()


def test_negated_readme_security_claim_does_not_create_doc_noise(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("This is not a vulnerability scanner.", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context").lower()
    assert "responsible disclosure" not in missing
    assert "authorization/scope" not in missing
    assert "readme/project purpose" not in missing


def test_missing_readme_with_source_creates_project_purpose_gap(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("print('visualize sorting')\n", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context").lower()
    assert "readme/project purpose" in missing


def test_sensitive_ml_requires_model_context_but_harmless_ml_does_not(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Builds a toxicity classifier for user comments.", encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    (src / "model.py").write_text("from transformers import AutoModel\n", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context").lower()
    assert "model card" in missing
    assert "fairness/bias evaluation" in missing

    harmless = tmp_path / "harmless"
    harmless.mkdir()
    (harmless / "README.md").write_text("Classifies iris flowers.", encoding="utf-8")
    hsrc = harmless / "src"
    hsrc.mkdir()
    (hsrc / "model.py").write_text("from sklearn.linear_model import LogisticRegression\n", encoding="utf-8")
    harmless_evidence = scan(harmless)
    harmless_missing = " ".join(item.reason for item in harmless_evidence if item.evidence_type == "missing_context").lower()
    assert "model card" not in harmless_missing


def test_dataset_public_release_requires_docs_but_negated_release_does_not(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "users.jsonl").write_text('{"user_id": "u1"}\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("This project will release the dataset publicly.", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context").lower()
    assert "release policy" in missing

    negated = tmp_path / "negated"
    negated.mkdir()
    ndata = negated / "data"
    ndata.mkdir()
    (ndata / "users.jsonl").write_text('{"count": 1}\n', encoding="utf-8")
    (negated / "README.md").write_text("No public dataset will be released.", encoding="utf-8")
    negated_evidence = scan(negated)
    negated_missing = " ".join(item.reason for item in negated_evidence if item.evidence_type == "missing_context").lower()
    assert "release policy" not in negated_missing
