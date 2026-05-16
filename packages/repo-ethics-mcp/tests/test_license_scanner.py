from __future__ import annotations

from pathlib import Path

from repo_ethics.scanners.license_scanner import scan


def test_package_json_only_does_not_create_broad_license_gap(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"scripts": {"test": "pytest"}}', encoding="utf-8")
    evidence = scan(tmp_path)
    assert [item for item in evidence if item.evidence_type == "missing_context"] == []


def test_explicit_missing_license_statement_creates_context_gap(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("License terms are not documented.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(
        item.category == "license_dataset_terms" and item.evidence_type == "missing_context"
        for item in evidence
    )


def test_license_file_maps_only_to_license_positive_control(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").write_text("MIT License placeholder.", encoding="utf-8")
    evidence = scan(tmp_path)
    positives = [item.category for item in evidence if item.evidence_type == "positive_control"]
    assert positives == ["license_dataset_terms"]
