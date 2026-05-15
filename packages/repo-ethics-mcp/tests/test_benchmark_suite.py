from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCH = ROOT / "benchmarks"
CASES = BENCH / "cases" / "cs_ethics_cases.jsonl"
GOLD = BENCH / "gold"
TAXONOMY = ROOT / "packages" / "repo-ethics-mcp" / "src" / "repo_ethics" / "kb" / "taxonomy.json"


def _load_cases() -> list[dict]:
    return [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_benchmark_jsonl_gold_and_fixtures_are_valid() -> None:
    cases = _load_cases()
    assert len(cases) >= 40
    taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))["categories"]
    known = set(taxonomy)
    negation_cases = 0
    positive_cases = 0
    prompt_injection_cases = 0
    negative_controls = 0
    for case in cases:
        fixture = ROOT / case["fixture_path"]
        gold = GOLD / f"{case['case_id']}.json"
        assert fixture.exists(), case["case_id"]
        assert gold.exists(), case["case_id"]
        gold_data = json.loads(gold.read_text(encoding="utf-8"))
        assert gold_data["benchmark_version"] == "0.1.0"
        assert gold_data["case_version"] == "1.0.0"
        assert gold_data["review_status"] in {"reviewed", "needs_human_review"}
        for field in ["expected_risk_categories", "expected_missing_context_categories", "expected_positive_controls", "expected_absent_categories"]:
            assert set(gold_data[field]) <= known
        fixture_size = sum(path.stat().st_size for path in fixture.rglob("*") if path.is_file())
        assert fixture_size < 800_000
        text = " ".join(str(value).lower() for value in gold_data.values())
        negation_cases += int("not " in text or "negated" in text)
        positive_cases += int(bool(gold_data["expected_positive_controls"]))
        prompt_injection_cases += int("prompt_injection_attempt" in gold_data["expected_risk_categories"])
        negative_controls += int("negative_controls" in gold_data["source_family"])
    assert negative_controls >= 5
    assert negation_cases >= 5
    assert positive_cases >= 5
    assert prompt_injection_cases >= 3


def test_fixture_generator_creates_fixtures_without_gold_labels(tmp_path: Path) -> None:
    out = tmp_path / "fixtures"
    subprocess.run(
        ["python3", str(BENCH / "scripts" / "generate_fixtures.py"), "--fixtures-dir", str(out)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert len([path for path in out.iterdir() if path.is_dir()]) >= 40
    assert not (out.parent / "gold").exists()


def test_benchmark_scoring_scripts_run_with_optional_direct_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "repo_outputs"
    results_dir = tmp_path / "results"
    subprocess.run(
        ["python3", str(BENCH / "scripts" / "run_repo_ethics_benchmark.py"), "--output-dir", str(output_dir)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "score_reports.py"),
            "--repo-output-dir",
            str(output_dir),
            "--direct-output-dir",
            str(tmp_path / "missing_direct_outputs"),
            "--results-dir",
            str(results_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
    assert "repo_ethics" in results["systems"]
    assert "direct_codex" not in results["systems"]
    assert (results_dir / "summary.md").exists()
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "summarize_results.py"),
            "--results-json",
            str(results_dir / "results.json"),
            "--summary",
            str(results_dir / "summary2.md"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert (results_dir / "summary2.md").exists()


def test_unreviewed_gold_is_excluded_by_default(tmp_path: Path) -> None:
    cases = tmp_path / "cases.jsonl"
    gold_dir = tmp_path / "gold"
    out = tmp_path / "outputs"
    results_dir = tmp_path / "results"
    gold_dir.mkdir()
    out.mkdir()
    row = {
        "benchmark_version": "0.1.0",
        "case_version": "1.0.0",
        "review_status": "needs_human_review",
        "case_id": "draft_case",
        "fixture_path": "benchmarks/fixtures/case_readme_clear_harmless",
        "expected_risk_categories": [],
        "expected_missing_context_categories": [],
        "expected_positive_controls": [],
        "expected_absent_categories": [],
    }
    cases.write_text(json.dumps(row) + "\n", encoding="utf-8")
    (gold_dir / "draft_case.json").write_text(json.dumps(row), encoding="utf-8")
    (out / "draft_case.md").write_text("privacy risk in README.md", encoding="utf-8")
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "score_reports.py"),
            "--cases",
            str(cases),
            "--gold-dir",
            str(gold_dir),
            "--repo-output-dir",
            str(out),
            "--results-dir",
            str(results_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
    assert results["case_count"] == 0


def test_category_aliases_score_direct_wording(tmp_path: Path) -> None:
    cases = tmp_path / "cases.jsonl"
    gold_dir = tmp_path / "gold"
    direct = tmp_path / "direct"
    results_dir = tmp_path / "results"
    gold_dir.mkdir()
    direct.mkdir()
    row = {
        "benchmark_version": "0.1.0",
        "case_version": "1.0.0",
        "review_status": "reviewed",
        "case_id": "alias_case",
        "fixture_path": "benchmarks/fixtures/case_readme_clear_harmless",
        "expected_risk_categories": ["privacy_identifiability"],
        "expected_missing_context_categories": [],
        "expected_positive_controls": [],
        "expected_absent_categories": [],
        "expected_evidence_paths": ["README.md"],
        "secret_values_to_check": [],
    }
    cases.write_text(json.dumps(row) + "\n", encoding="utf-8")
    (gold_dir / "alias_case.json").write_text(json.dumps(row), encoding="utf-8")
    (direct / "alias_case.md").write_text("There may be personal data concerns in README.md.", encoding="utf-8")
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "score_reports.py"),
            "--cases",
            str(cases),
            "--gold-dir",
            str(gold_dir),
            "--direct-output-dir",
            str(direct),
            "--repo-output-dir",
            str(tmp_path / "missing_repo"),
            "--results-dir",
            str(results_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
    assert results["systems"]["direct_codex"]["category_recall"] == 1.0
