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

