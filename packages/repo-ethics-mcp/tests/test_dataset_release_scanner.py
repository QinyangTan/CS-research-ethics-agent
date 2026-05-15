from pathlib import Path

from repo_ethics.scanners.dataset_release_scanner import scan


def test_dataset_scanner_detects_binary_metadata_without_content(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "sample.parquet").write_bytes(b"\x00PAR1")
    (data / "research.sqlite").write_bytes(b"\x00SQLite")
    evidence = scan(tmp_path)
    paths = {item.file_path for item in evidence if item.evidence_type == "risk_signal"}
    assert "data/sample.parquet" in paths
    assert "data/research.sqlite" in paths


def test_dataset_scanner_detects_large_data_file_metadata(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    large_file = data / "large.parquet"
    large_file.write_bytes(b"0" * 2048)
    evidence = scan(tmp_path, max_file_size=10)
    assert any(item.file_path == "data/large.parquet" for item in evidence)


def test_dataset_scanner_avoids_config_json_and_negated_release(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"scripts": {"test": "pytest"}}', encoding="utf-8")
    (tmp_path / "README.md").write_text("No public dataset will be released.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.evidence_type == "risk_signal"]


def test_dataset_scanner_marks_missing_release_policy_context(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Dataset release policy is not documented.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.evidence_type == "missing_context" for item in evidence)



def test_negated_docs_project_has_no_release_risk() -> None:
    root = Path(__file__).resolve().parents[3]
    evidence = scan(root / "examples" / "negated_docs_project")
    release_risks = [
        item
        for item in evidence
        if item.evidence_type == "risk_signal" and "release" in item.reason.lower()
    ]
    assert release_risks == []
