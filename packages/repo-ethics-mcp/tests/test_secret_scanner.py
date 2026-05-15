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

