"""Severity helpers for conservative risk mapping."""

from __future__ import annotations

from repo_ethics.schemas import EvidenceItem, Severity


def max_confidence(evidence: list[EvidenceItem]) -> str:
    order = {"low": 0, "medium": 1, "high": 2}
    if not evidence:
        return "low"
    return max((item.confidence for item in evidence), key=lambda value: order[value])


def category_severity(category: str, evidence: list[EvidenceItem], paired_with_concrete_risk: bool = False) -> Severity:
    if category == "secret_exposure":
        return "critical"
    if category in {"security_dual_use", "biometrics", "surveillance_tracking"}:
        return "high"
    if category == "dataset_release_reidentification":
        return "high" if paired_with_concrete_risk else "medium"
    if category in {"privacy_identifiability", "consent_reasonable_expectation"}:
        return "medium" if not paired_with_concrete_risk else "high"
    if category in {"web_scraping_platform_governance", "ml_fairness_deployment_risk"}:
        return "medium"
    if category in {"prompt_injection_attempt"}:
        return "medium"
    if category == "missing_ethics_documentation":
        return "medium" if paired_with_concrete_risk else "low"
    if category == "license_dataset_terms":
        return "medium"
    return "low"

