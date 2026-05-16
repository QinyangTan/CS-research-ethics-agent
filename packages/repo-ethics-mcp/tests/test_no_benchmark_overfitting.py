from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "packages" / "repo-ethics-mcp" / "src"
FORBIDDEN_PRODUCTION_STRINGS = [
    "case_",
    "benchmarks/gold",
    "benchmarks/results",
    "benchmarks/fixtures",
    "direct_codex",
    "direct_codex_naive",
]


def test_production_code_does_not_reference_benchmark_cases_or_outputs() -> None:
    offenders: list[str] = []
    for path in SRC.rglob("*"):
        if not path.is_file() or path.suffix not in {".py", ".json", ".md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for needle in FORBIDDEN_PRODUCTION_STRINGS:
            if needle in text:
                offenders.append(f"{path.relative_to(ROOT)} contains {needle!r}")
    assert offenders == []
