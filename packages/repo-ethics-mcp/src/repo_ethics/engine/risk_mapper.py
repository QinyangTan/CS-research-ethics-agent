"""Map deterministic evidence into conservative ethics risk findings."""

from __future__ import annotations

import hashlib
import json
from importlib import resources

from repo_ethics.engine.severity import category_severity, max_confidence
from repo_ethics.schemas import EvidenceItem, ProjectProfile, RiskFinding


def _load_json(name: str) -> dict:
    with resources.files("repo_ethics.kb").joinpath(name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _risk_id(title: str, category: str) -> str:
    return "risk_" + hashlib.sha256(f"{category}|{title}".encode("utf-8")).hexdigest()[:10]


def _by_category(evidence: list[EvidenceItem], evidence_types: set[str] | None = None) -> dict[str, list[EvidenceItem]]:
    grouped: dict[str, list[EvidenceItem]] = {}
    for item in evidence:
        if evidence_types is not None and item.evidence_type not in evidence_types:
            continue
        grouped.setdefault(item.category, []).append(item)
    return grouped


def _category_evidence(grouped: dict[str, list[EvidenceItem]], *categories: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for category in categories:
        items.extend(grouped.get(category, []))
    return items


def _rules_for(category: str) -> tuple[list[str], list[str], str]:
    taxonomy = _load_json("taxonomy.json")
    mitigation_rules = _load_json("mitigation_rules.json")
    followups = _load_json("followup_questions.json")
    tax = taxonomy["categories"].get(category, {})
    mitigations = mitigation_rules.get(category, tax.get("mitigation_suggestions", []))
    questions = followups.get(category, tax.get("followup_questions", []))
    why = tax.get("description", "This category may need additional review based on repository evidence.")
    return list(mitigations), list(questions), str(why)


def _category_name(category: str) -> str:
    taxonomy = _load_json("taxonomy.json")
    return str(taxonomy["categories"].get(category, {}).get("name", category.replace("_", " ").title()))


def _has_concrete_support(
    category: str,
    items: list[EvidenceItem],
    grouped: dict[str, list[EvidenceItem]],
    project_profile: ProjectProfile,
) -> bool:
    if grouped.get(category):
        return True
    if category == "missing_ethics_documentation":
        return bool(
            project_profile.missing_docs
            or grouped.get("privacy_identifiability")
            or grouped.get("web_scraping_platform_governance")
            or grouped.get("dataset_release_reidentification")
            or grouped.get("security_dual_use")
            or grouped.get("biometrics")
            or grouped.get("surveillance_tracking")
            or grouped.get("ml_fairness_deployment_risk")
        )
    reason_text = " ".join(item.reason.lower() for item in items)
    if category == "license_dataset_terms":
        return "mentioned as missing" in reason_text or "not documented" in reason_text
    if category == "dataset_release_reidentification":
        return "mentioned as absent" in reason_text or "release policy" in reason_text
    return False


def _finding(
    *,
    title: str,
    category: str,
    status: str,
    evidence: list[EvidenceItem],
    missing_context: list[str],
    paired_with_concrete_risk: bool = False,
) -> RiskFinding:
    if status in {"confirmed", "potential"} and not any(item.evidence_type == "risk_signal" for item in evidence):
        raise ValueError(f"{status} finding requires at least one risk_signal evidence item: {title}")
    mitigations, questions, why = _rules_for(category)
    return RiskFinding(
        risk_id=_risk_id(title, category),
        title=title,
        category=category,
        status=status,  # type: ignore[arg-type]
        severity=category_severity(category, evidence, paired_with_concrete_risk=paired_with_concrete_risk),
        confidence=max_confidence(evidence),  # type: ignore[arg-type]
        evidence=evidence,
        why_it_matters=why,
        missing_context=missing_context,
        recommended_mitigations=mitigations,
        advisor_or_irb_questions=questions,
    )


def map_risks(project_profile: ProjectProfile, evidence: list[EvidenceItem]) -> list[RiskFinding]:
    grouped = _by_category(evidence, {"risk_signal"})
    missing_grouped = _by_category(evidence, {"missing_context"})
    findings: list[RiskFinding] = []
    has_concrete_risk = any(
        category in grouped
        for category in [
            "privacy_identifiability",
            "web_scraping_platform_governance",
            "dataset_release_reidentification",
            "security_dual_use",
            "biometrics",
            "surveillance_tracking",
            "ml_fairness_deployment_risk",
            "secret_exposure",
        ]
    )

    if grouped.get("web_scraping_platform_governance") and grouped.get("privacy_identifiability"):
        items = _category_evidence(grouped, "web_scraping_platform_governance", "privacy_identifiability")
        findings.append(
            _finding(
                title="Possible privacy and consent risk from collected platform/user data",
                category="consent_reasonable_expectation",
                status="potential",
                evidence=items,
                missing_context=[
                    "Whether the data subjects reasonably expected this collection and analysis.",
                    "Whether platform terms, notices, or consent expectations were reviewed.",
                ],
                paired_with_concrete_risk=True,
            )
        )

    if grouped.get("web_scraping_platform_governance"):
        web_evidence = grouped["web_scraping_platform_governance"] + missing_grouped.get("web_scraping_platform_governance", [])
        findings.append(
            _finding(
                title="Web scraping governance and platform terms need review",
                category="web_scraping_platform_governance",
                status="potential",
                evidence=web_evidence,
                missing_context=["Platform terms, robots.txt handling, rate limits, and collection dates."],
            )
        )

    if grouped.get("privacy_identifiability") and grouped.get("dataset_release_reidentification"):
        dataset_evidence = _category_evidence(grouped, "privacy_identifiability", "dataset_release_reidentification")
        dataset_evidence += missing_grouped.get("dataset_release_reidentification", [])
        findings.append(
            _finding(
                title="Possible re-identification risk if dataset is released",
                category="dataset_release_reidentification",
                status="potential",
                evidence=dataset_evidence,
                missing_context=["Whether raw records will be shared, retained, aggregated, or de-identified."],
                paired_with_concrete_risk=True,
            )
        )
    elif grouped.get("dataset_release_reidentification"):
        dataset_evidence = grouped["dataset_release_reidentification"] + missing_grouped.get("dataset_release_reidentification", [])
        findings.append(
            _finding(
                title="Dataset release and retention details need review",
                category="dataset_release_reidentification",
                status="potential",
                evidence=dataset_evidence,
                missing_context=["Dataset sharing scope, retention period, and anonymization limits."],
            )
        )

    if grouped.get("security_dual_use"):
        findings.append(
            _finding(
                title="Security or dual-use research requires misuse and disclosure planning",
                category="security_dual_use",
                status="confirmed",
                evidence=grouped["security_dual_use"],
                missing_context=["Authorized scope, targets, responsible disclosure process, and release boundaries."],
            )
        )

    if grouped.get("biometrics") or grouped.get("surveillance_tracking"):
        findings.append(
            _finding(
                title="Biometric identification or surveillance risk",
                category="biometrics" if grouped.get("biometrics") else "surveillance_tracking",
                status="confirmed",
                evidence=_category_evidence(grouped, "biometrics", "surveillance_tracking"),
                missing_context=["Consent process, data retention, access controls, deployment setting, and affected population."],
            )
        )

    if grouped.get("ml_fairness_deployment_risk") and (project_profile.possible_human_data or grouped.get("privacy_identifiability")):
        findings.append(
            _finding(
                title="Fairness, profiling, or deployment harm risk",
                category="ml_fairness_deployment_risk",
                status="potential",
                evidence=_category_evidence(grouped, "ml_fairness_deployment_risk", "privacy_identifiability"),
                missing_context=["Intended deployment context, evaluation by subgroup, and whether outputs affect people."],
            )
        )

    if grouped.get("prompt_injection_attempt"):
        findings.append(
            _finding(
                title="Repository contains text that may attempt to manipulate reviewer instructions",
                category="prompt_injection_attempt",
                status="confirmed",
                evidence=grouped["prompt_injection_attempt"],
                missing_context=["Whether reviewers and agents treat repository text as evidence rather than instructions."],
            )
        )

    if grouped.get("secret_exposure"):
        findings.append(
            _finding(
                title="Possible secret exposure",
                category="secret_exposure",
                status="confirmed",
                evidence=grouped["secret_exposure"],
                missing_context=["Whether credentials are active and whether they have been rotated."],
            )
        )

    if missing_grouped.get("license_dataset_terms"):
        license_evidence = missing_grouped["license_dataset_terms"]
        findings.append(
            _finding(
                title="License or dataset redistribution terms are unclear",
                category="license_dataset_terms",
                status="unknown",
                evidence=license_evidence,
                missing_context=["Code license, dataset source terms, and redistribution permissions."],
            )
        )

    if missing_grouped.get("missing_ethics_documentation"):
        missing_docs_evidence = missing_grouped["missing_ethics_documentation"]
        findings.append(
            _finding(
                title="Missing ethics, data handling, or release documentation",
                category="missing_ethics_documentation",
                status="unknown",
                evidence=missing_docs_evidence,
                missing_context=project_profile.missing_docs or ["Project purpose, data handling, and release boundaries."],
                paired_with_concrete_risk=has_concrete_risk,
            )
        )

    attached_missing_ids = {
        item.evidence_id
        for finding in findings
        for item in finding.evidence
        if item.evidence_type == "missing_context"
    }
    for category, items in sorted(missing_grouped.items()):
        unattached = [item for item in items if item.evidence_id not in attached_missing_ids]
        if not unattached:
            continue
        if not _has_concrete_support(category, unattached, grouped, project_profile):
            continue
        findings.append(
            _finding(
                title=f"Additional missing context for {_category_name(category)}",
                category=category,
                status="unknown",
                evidence=unattached,
                missing_context=[item.reason for item in unattached],
            )
        )

    return findings
