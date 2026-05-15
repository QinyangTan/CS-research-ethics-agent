"""Run all scanners and return structured scan results."""

from __future__ import annotations

from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence
from repo_ethics.schemas import EvidenceItem, ScanResult
from repo_ethics.scanners import (
    biometrics_surveillance_scanner,
    dataset_release_scanner,
    documentation_scanner,
    license_scanner,
    ml_risk_scanner,
    pii_scanner,
    prompt_injection_scanner,
    scraping_scanner,
    secret_scanner,
    security_dual_use_scanner,
)
from repo_ethics.scanners.repo_structure import build_project_profile


SCANNERS = [
    pii_scanner.scan,
    scraping_scanner.scan,
    security_dual_use_scanner.scan,
    biometrics_surveillance_scanner.scan,
    ml_risk_scanner.scan,
    dataset_release_scanner.scan,
    license_scanner.scan,
    documentation_scanner.scan,
    prompt_injection_scanner.scan,
    secret_scanner.scan,
]


def run_scan(
    root_path: str | Path,
    *,
    max_file_size: int = 524_288,
    include_snippets: bool = True,
) -> ScanResult:
    profile = build_project_profile(root_path, max_file_size=max_file_size)
    evidence: list[EvidenceItem] = []
    warnings: list[str] = []
    for scanner in SCANNERS:
        try:
            evidence.extend(
                scanner(root_path, max_file_size=max_file_size, include_snippets=include_snippets)
            )
        except OSError as exc:
            warnings.append(f"{scanner.__module__} skipped due to read error: {exc}")
    evidence = dedupe_evidence(evidence)

    categories = {item.category for item in evidence}
    profile.possible_human_data = profile.possible_human_data or bool(
        {"privacy_identifiability", "biometrics", "surveillance_tracking"} & categories
    )
    profile.possible_security_sensitive = profile.possible_security_sensitive or "security_dual_use" in categories
    profile.possible_dual_use = profile.possible_dual_use or "security_dual_use" in categories

    return ScanResult(project_profile=profile, evidence=evidence, warnings=warnings)

