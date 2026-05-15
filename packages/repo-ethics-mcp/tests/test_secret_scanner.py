from pathlib import Path

from repo_ethics.scanners.secret_scanner import scan


def test_secret_scanner_masks_secrets(tmp_path: Path) -> None:
    secret = "sk-" + "a" * 28
    config = tmp_path / "config.py"
    config.write_text(f"API_KEY = '{secret}'\n", encoding="utf-8")
    evidence = scan(tmp_path)
    assert evidence
    rendered = "\n".join(item.model_dump_json() for item in evidence)
    assert secret not in rendered
    assert "[REDACTED_SECRET_LIKE_VALUE]" in rendered


def test_secret_scanner_env_file_does_not_show_contents(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("PASSWORD=supersecretvalue123\n", encoding="utf-8")
    evidence = scan(tmp_path)
    rendered = "\n".join(item.model_dump_json() for item in evidence)
    assert "supersecretvalue123" not in rendered
    assert any(item.evidence_type == "risk_signal" for item in evidence)


def test_secret_scanner_ignores_env_example_placeholders(tmp_path: Path) -> None:
    env = tmp_path / ".env.example"
    env.write_text("API_KEY=replace-me\nTOKEN=example-token\n", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not evidence
