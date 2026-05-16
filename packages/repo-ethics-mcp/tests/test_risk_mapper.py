from pathlib import Path

from repo_ethics.engine.report_builder import build_report
from repo_ethics.engine.risk_mapper import map_risks
from repo_ethics.engine.scan_runner import run_scan
from repo_ethics.schemas import EvidenceItem, ProjectProfile


def _ev(category: str, evidence_type: str = "risk_signal") -> EvidenceItem:
    return EvidenceItem(
        evidence_id=f"id-{category}",
        evidence_type=evidence_type,  # type: ignore[arg-type]
        category=category,
        file_path="README.md",
        line_start=1,
        line_end=1,
        snippet="example",
        reason="test evidence",
        confidence="high",
    )


def test_risk_mapper_combines_scraping_and_pii() -> None:
    profile = ProjectProfile(root_path="/tmp/x", project_name="x", languages=[], important_files=[], detected_research_activities=[], detected_data_sources=[], possible_human_data=True, possible_security_sensitive=False, possible_dual_use=False, missing_docs=[])
    findings = map_risks(profile, [_ev("web_scraping_platform_governance"), _ev("privacy_identifiability")])
    titles = {finding.title for finding in findings}
    assert "Possible privacy and consent risk from collected platform/user data" in titles
    assert all(finding.evidence for finding in findings if finding.status in {"confirmed", "potential"})
    assert all(
        any(item.evidence_type == "risk_signal" for item in finding.evidence)
        for finding in findings
        if finding.status in {"confirmed", "potential"}
    )


def test_missing_documentation_alone_is_not_high(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("print('sorting visualizer')\n", encoding="utf-8")
    scan_result = run_scan(tmp_path)
    report = build_report(scan_result)
    missing = [finding for finding in report.findings if finding.category == "missing_ethics_documentation"]
    assert missing
    assert all(finding.severity == "low" for finding in missing)


def test_positive_controls_do_not_create_findings() -> None:
    profile = ProjectProfile(root_path="/tmp/x", project_name="x", languages=[], important_files=[], detected_research_activities=[], detected_data_sources=[], possible_human_data=False, possible_security_sensitive=False, possible_dual_use=False, missing_docs=[])
    findings = map_risks(profile, [_ev("license_dataset_terms", "positive_control")])
    assert findings == []


def test_security_dual_use_confirmed_high_risk() -> None:
    profile = ProjectProfile(root_path="/tmp/x", project_name="x", languages=[], important_files=[], detected_research_activities=[], detected_data_sources=[], possible_human_data=False, possible_security_sensitive=True, possible_dual_use=True, missing_docs=[])
    findings = map_risks(profile, [_ev("security_dual_use")])
    assert findings[0].status == "confirmed"
    assert findings[0].severity == "high"


def test_license_missing_context_creates_unknown_only() -> None:
    profile = ProjectProfile(root_path="/tmp/x", project_name="x", languages=[], important_files=[], detected_research_activities=[], detected_data_sources=[], possible_human_data=False, possible_security_sensitive=False, possible_dual_use=False, missing_docs=[])
    findings = map_risks(profile, [_ev("license_dataset_terms", "missing_context")])
    assert len(findings) == 1
    assert findings[0].status == "unknown"
