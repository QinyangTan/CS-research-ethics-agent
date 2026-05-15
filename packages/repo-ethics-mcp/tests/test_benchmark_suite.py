from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCH = ROOT / "benchmarks"
CASES = BENCH / "cases" / "cs_ethics_cases.jsonl"
GOLD = BENCH / "gold"
TAXONOMY = ROOT / "packages" / "repo-ethics-mcp" / "src" / "repo_ethics" / "kb" / "taxonomy.json"
REQUIRED_CASE_FIELDS = {
    "benchmark_version",
    "case_version",
    "review_status",
    "case_id",
    "title",
    "fixture_path",
    "input_type",
    "source_family",
    "expected_risk_categories",
    "expected_missing_context_categories",
    "expected_positive_controls",
    "expected_absent_categories",
}
RESERVED_EMAIL_SUFFIXES = (".test", ".example")


def _load_cases() -> list[dict]:
    return [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]


def _fixture_text(fixture: Path) -> str:
    parts: list[str] = []
    for path in fixture.rglob("*"):
        if path.is_file() and path.stat().st_size < 200_000:
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def _score_direct_markdown(tmp_path: Path, markdown: str, row: dict) -> dict:
    cases = tmp_path / "cases.jsonl"
    gold_dir = tmp_path / "gold"
    direct = tmp_path / "direct"
    results_dir = tmp_path / "results"
    gold_dir.mkdir()
    direct.mkdir()
    cases.write_text(json.dumps(row) + "\n", encoding="utf-8")
    (gold_dir / f"{row['case_id']}.json").write_text(json.dumps(row), encoding="utf-8")
    (direct / f"{row['case_id']}.md").write_text(markdown, encoding="utf-8")
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "score_reports.py"),
            "--cases",
            str(cases),
            "--gold-dir",
            str(gold_dir),
            "--repo-output-dir",
            str(tmp_path / "missing_repo"),
            "--direct-output-dir",
            str(direct),
            "--results-dir",
            str(results_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
    rows = [item for item in results["cases"] if item["system"] == "direct_codex_strong"]
    assert len(rows) == 1
    return rows[0]


def _base_scoring_row(case_id: str = "direct_case") -> dict:
    return {
        "benchmark_version": "0.1.0",
        "case_version": "1.0.0",
        "review_status": "reviewed",
        "case_id": case_id,
        "title": "Direct Markdown scoring case",
        "fixture_path": "benchmarks/fixtures/case_readme_clear_harmless",
        "input_type": "repo",
        "source_family": ["unit_test"],
        "expected_risk_categories": [],
        "expected_missing_context_categories": [],
        "expected_positive_controls": [],
        "expected_absent_categories": [],
        "expected_evidence_paths": [],
        "secret_values_to_check": [],
        "must_mention": [],
        "must_not_mention": [],
    }


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
        assert REQUIRED_CASE_FIELDS <= set(case), case.get("case_id")
        fixture = ROOT / case["fixture_path"]
        gold = GOLD / f"{case['case_id']}.json"
        assert fixture.exists(), case["case_id"]
        assert gold.exists(), case["case_id"]
        gold_data = json.loads(gold.read_text(encoding="utf-8"))
        assert REQUIRED_CASE_FIELDS <= set(gold_data), case["case_id"]
        for field in [
            "case_id",
            "benchmark_version",
            "case_version",
            "fixture_path",
            "expected_risk_categories",
            "expected_missing_context_categories",
            "expected_positive_controls",
            "expected_absent_categories",
        ]:
            assert gold_data[field] == case[field], case["case_id"]
        assert gold_data["benchmark_version"] == "0.1.0"
        assert gold_data["case_version"] == "1.0.0"
        assert gold_data["review_status"] in {"reviewed", "needs_human_review"}
        for field in ["expected_risk_categories", "expected_missing_context_categories", "expected_positive_controls", "expected_absent_categories"]:
            assert set(gold_data[field]) <= known
        fixture_size = sum(path.stat().st_size for path in fixture.rglob("*") if path.is_file())
        assert fixture_size < 800_000
        assert all(path.stat().st_size < 600_000 for path in fixture.rglob("*") if path.is_file())
        fixture_text = _fixture_text(fixture)
        emails = re.findall(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", fixture_text, flags=re.I)
        assert all(domain.lower().endswith(RESERVED_EMAIL_SUFFIXES) for domain in emails), case["case_id"]
        assert not re.search(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", fixture_text), case["case_id"]
        assert not re.search(r"\b\d{1,5}\s+[A-Za-z0-9 .'-]+\s+(?:Street|St\.|Avenue|Ave\.|Road|Rd\.|Boulevard|Blvd\.)\b", fixture_text), case["case_id"]
        forbidden_payload_terms = ["shellcode", "reverse shell", "credential dumping", "ransomware", "metasploit", "payload ="]
        assert not any(term in fixture_text.lower() for term in forbidden_payload_terms), case["case_id"]
        for value in gold_data.get("secret_values_to_check", []):
            assert value.startswith("sk-benchmarkfake") or "fake" in value.lower() or "placeholder" in value.lower()
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
    assert "direct_codex_strong" not in results["systems"]
    assert results["output_availability"]["direct_codex_strong"]["available"] == 0
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
    assert results["systems"]["direct_codex_strong"]["category_recall"] == 1.0
    assert results["cases"][0]["markdown_scoring_mode"] == "fallback_markdown"


def test_sectioned_markdown_missing_context_not_overcounted_from_mitigations(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["privacy_identifiability"]
    markdown = """## Potential Risks
Privacy risk: personal data in README.md.

## Mitigations
Add documentation where missing.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "privacy_identifiability" in scored["risk_categories_found"]
    assert "privacy_identifiability" not in scored["missing_context_categories_found"]
    assert scored["markdown_scoring_mode"] == "sectioned_markdown"


def test_sectioned_markdown_positive_controls_not_overcounted_from_recommendations(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["security_dual_use"]
    markdown = """## Potential Risks
Security dual-use risk in src/scanner.py.

## Recommendations
Add responsible disclosure documentation.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" in scored["risk_categories_found"]
    assert "security_dual_use" not in scored["positive_controls_found"]


def test_sectioned_markdown_positive_control_section_counts(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_positive_controls"] = ["security_dual_use"]
    markdown = """## Existing Safeguards
SECURITY.md documents responsible disclosure and authorization scope.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" in scored["positive_controls_found"]


def test_sectioned_markdown_missing_context_section_counts(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_missing_context_categories"] = ["security_dual_use"]
    markdown = """## Missing Context
Responsible disclosure and authorization scope are not documented.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" in scored["missing_context_categories_found"]


def test_evidence_absence_does_not_count_security_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_absent_categories"] = ["security_dual_use"]
    markdown = """## Evidence
No security dual-use evidence was found.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" not in scored["risk_categories_found"]
    assert scored["false_positive_count"] == 0


def test_evidence_absence_with_file_path_does_not_count_biometrics_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_absent_categories"] = ["biometrics"]
    markdown = """## File Evidence
No biometrics evidence was detected in src/main.py.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "biometrics" not in scored["risk_categories_found"]
    assert scored["false_positive_count"] == 0


def test_evidence_with_file_path_and_risk_marker_counts_security_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["security_dual_use"]
    markdown = """## Evidence
src/scanner.py contains socket scanning logic, suggesting security dual-use concerns.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" in scored["risk_categories_found"]


def test_evidence_with_file_reference_only_counts_security_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["security_dual_use"]
    markdown = """## Repository Evidence
README.md describes a vulnerability scanner.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "security_dual_use" in scored["risk_categories_found"]


def test_evidence_with_data_path_counts_privacy_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["privacy_identifiability"]
    markdown = """## Repository Evidence
data/schema.json contains email and student_id fields.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "privacy_identifiability" in scored["risk_categories_found"]


def test_absent_personal_data_with_file_path_does_not_count_privacy_risk(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_absent_categories"] = ["privacy_identifiability"]
    markdown = """## Evidence
No personal data was found in data/schema.json.
"""
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert "privacy_identifiability" not in scored["risk_categories_found"]
    assert scored["false_positive_count"] == 0


def test_markdown_fallback_missing_context_requires_local_window(tmp_path: Path) -> None:
    row = _base_scoring_row()
    row["expected_risk_categories"] = ["privacy_identifiability"]
    row["expected_missing_context_categories"] = ["privacy_identifiability"]
    markdown = "Privacy risk around personal data. Consent process is unclear near the personal data discussion."
    scored = _score_direct_markdown(tmp_path, markdown, row)
    assert scored["markdown_scoring_mode"] == "fallback_markdown"
    assert "privacy_identifiability" in scored["risk_categories_found"]
    assert "privacy_identifiability" in scored["missing_context_categories_found"]


def test_naive_direct_baseline_placeholder_is_manual_by_default() -> None:
    result = subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "run_direct_codex_placeholder.py"),
            "--baseline",
            "naive",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "No direct Codex command was run." in result.stdout
    assert "Baseline: naive" in result.stdout
    assert "direct_codex_naive" in result.stdout


def test_direct_baseline_help_warns_about_local_command_execution() -> None:
    result = subprocess.run(
        ["python3", str(BENCH / "scripts" / "run_direct_codex_placeholder.py"), "--help"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "executed on your" in result.stdout
    assert "machine; review it carefully" in result.stdout


def test_scoring_includes_naive_direct_outputs_and_summary_availability(tmp_path: Path) -> None:
    cases = tmp_path / "cases.jsonl"
    gold_dir = tmp_path / "gold"
    naive = tmp_path / "naive"
    results_dir = tmp_path / "results"
    gold_dir.mkdir()
    naive.mkdir()
    row = _base_scoring_row("naive_case")
    row["expected_risk_categories"] = ["privacy_identifiability"]
    cases.write_text(json.dumps(row) + "\n", encoding="utf-8")
    (gold_dir / "naive_case.json").write_text(json.dumps(row), encoding="utf-8")
    (naive / "naive_case.md").write_text("Privacy risk around personal data in README.md.", encoding="utf-8")
    subprocess.run(
        [
            "python3",
            str(BENCH / "scripts" / "score_reports.py"),
            "--cases",
            str(cases),
            "--gold-dir",
            str(gold_dir),
            "--repo-output-dir",
            str(tmp_path / "missing_repo"),
            "--direct-output-dir",
            str(tmp_path / "missing_strong"),
            "--direct-naive-output-dir",
            str(naive),
            "--results-dir",
            str(results_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
    summary = (results_dir / "summary.md").read_text(encoding="utf-8")
    assert "direct_codex_naive" in results["systems"]
    assert results["output_availability"]["direct_codex_naive"]["available"] == 1
    assert "`direct_codex_naive`: 1/1 outputs available" in summary
    assert "These scores measure report behavior on synthetic controlled cases, not final ethical truth." in summary
    lowered = summary.lower()
    assert "guarantees" not in lowered
    assert "proves" not in lowered
    assert "definitively" not in lowered
