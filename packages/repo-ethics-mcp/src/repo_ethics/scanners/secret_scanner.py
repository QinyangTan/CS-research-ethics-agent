"""Detect possible secrets while never returning the full value."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, line_window_for_match, make_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "Possible AWS access key."),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "Possible GitHub token."),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "Possible hosted AI/API key pattern."),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----"), "Possible private key block."),
    (re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|password)\s*[:=]\s*['\"]?[^'\"\s]{12,}"), "Possible secret assignment."),
]


def mask_secret_snippet(snippet: str) -> str:
    masked = snippet
    for pattern, _ in SECRET_PATTERNS:
        masked = pattern.sub("[REDACTED_SECRET_LIKE_VALUE]", masked)
    return masked


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        if Path(scanned.rel_path).name.startswith(".env"):
            evidence.append(
                make_evidence(
                    category="secret_exposure",
                    file_path=scanned.rel_path,
                    reason=".env-like file detected; these often contain credentials and should not be committed.",
                    confidence="medium",
                    evidence_type="risk_signal",
                    include_snippets=False,
                )
            )
        for pattern, reason in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line_start, line_end, snippet = line_window_for_match(text, match.start(), match.end())
                masked = mask_secret_snippet(snippet)
                evidence.append(
                    make_evidence(
                        category="secret_exposure",
                        file_path=scanned.rel_path,
                        line_start=line_start,
                        line_end=line_end,
                        snippet=masked,
                        reason=reason,
                        confidence="high",
                        evidence_type="risk_signal",
                        include_snippets=include_snippets,
                    )
                )
    return dedupe_evidence(evidence)
