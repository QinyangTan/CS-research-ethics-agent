from pathlib import Path

from repo_ethics.scanners.pii_scanner import scan


def test_pii_scanner_detects_sensitive_fields(tmp_path: Path) -> None:
    schema = tmp_path / "schema.json"
    schema.write_text(
        '{"username": "u", "email": "a@example.com", "location": "x", "student_id": "s", "face_embedding": []}',
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    assert {item.category for item in evidence} == {"privacy_identifiability"}
    reasons = " ".join(item.reason for item in evidence)
    assert "usernames" in reasons
    assert "email" in reasons
    assert "student" in reasons
    assert "facial" in reasons


def test_pii_scanner_ignores_tokens_and_negated_collection(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "access_token is used for API auth. We do not collect usernames, but we store email addresses.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    rendered = "\n".join(item.model_dump_json() for item in evidence)
    assert "access_token" not in rendered
    assert "usernames" not in rendered
    assert "email" in rendered


def test_negated_docs_project_suppresses_username_but_keeps_timestamp() -> None:
    root = Path(__file__).resolve().parents[3]
    evidence = scan(root / "examples" / "negated_docs_project")
    rendered = "\n".join(item.model_dump_json() for item in evidence)
    assert "usernames" not in rendered
    assert "timestamp" in rendered
