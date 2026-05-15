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


def test_checker_does_not_flag_provider_name_markdown_prose(tmp_path: Path) -> None:
    doc = tmp_path / "notes.md"
    doc.write_text("We compare Groq-style provider ecosystems conceptually.\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload == {"ok": True, "violations": []}


def test_checker_catches_groq_import(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("import " + "groq\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["violations"][0]["pattern"] == "import " + "groq"


def test_checker_catches_markdown_openai_import_unless_allowlisted(tmp_path: Path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text("```python\nimport " + "openai\n```\n", encoding="utf-8")
    bad_result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert bad_result.returncode == 1

    bad.write_text(
        "```python\nimport " + "openai  # repo-ethics-allow-hosted-llm-pattern\n```\n",
        encoding="utf-8",
    )
    allowed_result = subprocess.run(
        ["python3", str(CHECKER), "--root", str(tmp_path), "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(allowed_result.stdout) == {"ok": True, "violations": []}
