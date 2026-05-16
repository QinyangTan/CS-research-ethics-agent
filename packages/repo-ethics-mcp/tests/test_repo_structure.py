from __future__ import annotations

from pathlib import Path

from repo_ethics.scanners.repo_structure import build_project_profile


def test_project_profile_uses_target_aware_negation(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "This project does not scrape websites. This is not a vulnerability scanner.",
        encoding="utf-8",
    )
    profile = build_project_profile(tmp_path)
    assert "web scraping" not in profile.detected_research_activities
    assert "web scraping" not in profile.detected_data_sources
    assert profile.possible_security_sensitive is False
    assert profile.possible_dual_use is False


def test_project_profile_keeps_contrastive_positive_signals(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "This project does not scrape demos, but it does scrape public pages. "
        "It is not a toy, but it is a vulnerability scanner.",
        encoding="utf-8",
    )
    profile = build_project_profile(tmp_path)
    assert "web scraping" in profile.detected_research_activities
    assert "web scraping" in profile.detected_data_sources
    assert profile.possible_security_sensitive is True
    assert profile.possible_dual_use is True
