"""Detect license and redistribution documentation signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_evidence, make_match_evidence, read_text_file
from repo_ethics.engine.text_signals import find_negated_topic_mentions, find_positive_topic_mentions
from repo_ethics.schemas import EvidenceItem


LICENSE_PATTERNS = [
    (re.compile(r"\b(MIT License|Apache License|BSD License|GPL|Creative Commons|CC-BY|ODC-BY)\b", re.I), "Mentions a code or dataset license."),
    (re.compile(r"\bdataset license|data license|redistribution|non-commercial|terms of use\b", re.I), "Mentions dataset terms or redistribution limits."),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    saw_license_file = False
    saw_license_mention = False
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        name = Path(scanned.rel_path).name.lower()
        text = read_text_file(scanned.path)
        if name == "license" or name.startswith("license."):
            saw_license_file = True
            evidence.append(
                make_evidence(
                    category="license_dataset_terms",
                    file_path=scanned.rel_path,
                    reason="Repository includes a license file.",
                    confidence="high",
                    evidence_type="positive_control",
                    include_snippets=include_snippets,
                )
            )
        for pattern, reason in LICENSE_PATTERNS:
            for start, end, _ in find_positive_topic_mentions(text, [pattern]):
                saw_license_mention = True
                evidence.append(
                    make_match_evidence(
                        category="license_dataset_terms",
                        file_path=scanned.rel_path,
                        text=text,
                        start=start,
                        end=end,
                        reason=reason,
                        confidence="medium",
                        evidence_type="positive_control",
                        include_snippets=include_snippets,
                    )
                )
            for start, end, _ in find_negated_topic_mentions(text, [pattern]):
                evidence.append(
                    make_match_evidence(
                        category="license_dataset_terms",
                        file_path=scanned.rel_path,
                        text=text,
                        start=start,
                        end=end,
                        reason="License or dataset terms are mentioned as missing, unclear, or not documented.",
                        confidence="medium",
                        evidence_type="missing_context",
                        include_snippets=include_snippets,
                    )
                )

    if not saw_license_file and not saw_license_mention:
        evidence.append(
            make_evidence(
                category="license_dataset_terms",
                file_path=".",
                reason="No code or dataset license documentation was detected.",
                confidence="medium",
                evidence_type="missing_context",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)

