from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "scripts" / "check_no_hosted_llm_calls.py"


def test_no_hosted_llm_call_paths_in_repo() -> None:
    result = subprocess.run(
        ["python3", str(CHECKER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "No hosted LLM API call paths detected." in result.stdout


def test_checker_catches_temp_openai_import(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("import " + "openai\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["violations"][0]["path"] == "bad.py"


def test_checker_ignores_benchmark_fixture_fake_secret(tmp_path: Path) -> None:
    fixture = tmp_path / "benchmarks" / "fixtures" / "case_fake_secret"
    fixture.mkdir(parents=True)
    (fixture / ".env").write_text("OPENAI_API_KEY=sk-fakefixturevalue000000\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_checker_json_output_and_inline_allowlist(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed.py"
    allowed.write_text("import " + "openai  # repo-ethics-allow-hosted-llm-pattern\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload == {"ok": True, "violations": []}
