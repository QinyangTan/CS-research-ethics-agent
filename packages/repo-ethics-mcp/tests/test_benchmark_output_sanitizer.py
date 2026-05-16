from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SANITIZER = ROOT / "benchmarks" / "scripts" / "sanitize_benchmark_outputs.py"
ABS_PREFIX = str(ROOT)


def test_sanitizer_rewrites_absolute_fixture_path(tmp_path: Path) -> None:
    out = tmp_path / "outputs"
    out.mkdir()
    target = out / "case.md"
    target.write_text(f"{ABS_PREFIX}/benchmarks/fixtures/case_x/src/main.py:12\n", encoding="utf-8")
    subprocess.run(["python3", str(SANITIZER), "--dir", str(out)], cwd=ROOT, check=True, capture_output=True, text=True)
    assert target.read_text(encoding="utf-8") == "benchmarks/fixtures/case_x/src/main.py:12\n"


def test_sanitizer_rewrites_markdown_link_and_preserves_line_suffix(tmp_path: Path) -> None:
    out = tmp_path / "outputs"
    out.mkdir()
    target = out / "case.md"
    target.write_text(
        f"[README.md]({ABS_PREFIX}/benchmarks/fixtures/case_x/README.md#L3)\n",
        encoding="utf-8",
    )
    subprocess.run(["python3", str(SANITIZER), "--dir", str(out)], cwd=ROOT, check=True, capture_output=True, text=True)
    assert target.read_text(encoding="utf-8") == "[README.md](benchmarks/fixtures/case_x/README.md#L3)\n"


def test_sanitizer_ignores_non_repo_absolute_path(tmp_path: Path) -> None:
    out = tmp_path / "outputs"
    out.mkdir()
    target = out / "case.md"
    target.write_text("/var/tmp/other-repo/benchmarks/fixtures/case_x/README.md\n", encoding="utf-8")
    subprocess.run(["python3", str(SANITIZER), "--dir", str(out)], cwd=ROOT, check=True, capture_output=True, text=True)
    assert "/var/tmp/other-repo" in target.read_text(encoding="utf-8")


def test_sanitizer_dry_run_does_not_modify_files(tmp_path: Path) -> None:
    out = tmp_path / "outputs"
    out.mkdir()
    target = out / "case.md"
    original = f"{ABS_PREFIX}/benchmarks/fixtures/case_x/README.md\n"
    target.write_text(original, encoding="utf-8")
    subprocess.run(
        ["python3", str(SANITIZER), "--dry-run", "--dir", str(out)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert target.read_text(encoding="utf-8") == original


def test_sanitizer_check_exits_nonzero_when_paths_remain(tmp_path: Path) -> None:
    out = tmp_path / "outputs"
    out.mkdir()
    (out / "case.md").write_text(f"{ABS_PREFIX}/benchmarks/fixtures/case_x/README.md\n", encoding="utf-8")
    result = subprocess.run(
        ["python3", str(SANITIZER), "--check", "--dir", str(out)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
