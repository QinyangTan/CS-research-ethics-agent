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
    assert not [item for item in evidence if item.evidence_type == "positive_control"]


def test_dataset_scanner_marks_missing_release_policy_context(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Dataset release policy is not documented.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.evidence_type == "missing_context" for item in evidence)


def test_data_file_with_no_public_release_keeps_nonrelease_governance_context(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "records.jsonl").write_text('{"timestamp":"2026-01-01T00:00:00Z"}\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("No public dataset will be released.", encoding="utf-8")
    evidence = scan(tmp_path)
    missing = " ".join(item.reason for item in evidence if item.evidence_type == "missing_context").lower()
    assert "data-governance context" in missing
    assert "release policy" not in missing


def test_data_card_suppresses_extra_dataset_missing_context_when_no_release(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    docs = tmp_path / "docs"
    docs.mkdir()
    (data / "records.jsonl").write_text('{"aggregate_count": 4}\n', encoding="utf-8")
    (docs / "data_card.md").write_text(
        "Data card documents source, intended use, retention, deletion, license, release limits, and access controls.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.evidence_type == "missing_context"]
    assert any(
        item.evidence_type == "positive_control" and item.category == "dataset_release_reidentification"
        for item in evidence
    )


def test_full_release_policy_creates_dataset_positive_control(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "records.jsonl").write_text('{"record_id": "r1"}\n', encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "No raw data will be public; only aggregate statistics will be released. "
        "Access is controlled, retention is 30 days, and identifiers are removed.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    assert any(
        item.evidence_type == "positive_control" and item.category == "dataset_release_reidentification"
        for item in evidence
    )



def test_negated_docs_project_has_no_release_risk() -> None:
    root = Path(__file__).resolve().parents[3]
    evidence = scan(root / "examples" / "negated_docs_project")
    release_risks = [
        item
        for item in evidence
        if item.evidence_type == "risk_signal" and "release" in item.reason.lower()
    ]
    assert release_risks == []
