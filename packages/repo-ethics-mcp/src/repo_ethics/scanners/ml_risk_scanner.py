"""Detect ML components and people-impacting deployment signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_match_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\b(sklearn|torch|tensorflow|keras|transformers|xgboost)\b", re.I), "Uses machine learning libraries.", "medium"),
    (re.compile(r"\bclassification of people|classify users|profiling|user profile\b", re.I), "References classification or profiling of people.", "high"),
    (re.compile(r"\brecommender system|recommendation model\b", re.I), "References recommender systems.", "medium"),
    (re.compile(r"\btoxicity detection|emotion detection\b", re.I), "References toxicity or emotion classification.", "medium"),
    (re.compile(r"\bcredit scoring|risk scoring|hiring|admissions|grading\b", re.I), "References high-impact decision contexts.", "high"),
    (re.compile(r"\bdemographic prediction|predict demographic|race prediction|gender prediction\b", re.I), "References demographic prediction.", "high"),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        for pattern, reason, confidence in PATTERNS:
            for match in pattern.finditer(text):
                evidence.append(
                    make_match_evidence(
                        category="ml_fairness_deployment_risk",
                        file_path=scanned.rel_path,
                        text=text,
                        start=match.start(),
                        end=match.end(),
                        reason=reason,
                        confidence=confidence,  # type: ignore[arg-type]
                        include_snippets=include_snippets,
                    )
                )
    return dedupe_evidence(evidence)

