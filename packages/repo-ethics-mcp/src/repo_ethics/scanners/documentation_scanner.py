"""Check for ethics, privacy, safety, and release documentation coverage."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


REQUIRED_TOPICS: dict[str, re.Pattern[str]] = {
    "ethics": re.compile(r"\bethics|ethical\b", re.I),
    "privacy": re.compile(r"\bprivacy|personal data\b", re.I),
    "consent": re.compile(r"\bconsent|notice\b", re.I),
    "anonymization": re.compile(r"\banonymi[sz]ation|de-identification\b", re.I),
    "data retention": re.compile(r"\bretention|delete|deletion\b", re.I),
    "data access": re.compile(r"\baccess control|data access\b", re.I),
    "responsible disclosure": re.compile(r"\bresponsible disclosure|vulnerability disclosure\b", re.I),
    "IRB/review body": re.compile(r"\bIRB|review body|ethics review\b", re.I),
    "platform terms": re.compile(r"\bplatform terms|terms of service|robots\.txt|data policy\b", re.I),
    "limitations": re.compile(r"\blimitations?|known limits\b", re.I),
    "misuse": re.compile(r"\bmisuse|abuse|dual-use\b", re.I),
    "release policy": re.compile(r"\brelease policy|public release|sharing\b", re.I),
    "safety": re.compile(r"\bsafety|safe release\b", re.I),
    "model card": re.compile(r"\bmodel card|modelcard\b", re.I),
    "data card": re.compile(r"\bdata card|datacard|datasheet\b", re.I),
}


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    docs_text = ""
    docs_files: list[str] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        rel = scanned.rel_path.lower()
        if rel.endswith((".md", ".rst", ".txt")) or rel.startswith("docs/"):
            docs_files.append(scanned.rel_path)
            docs_text += "\n" + read_text_file(scanned.path)

    missing = [topic for topic, pattern in REQUIRED_TOPICS.items() if not pattern.search(docs_text)]
    evidence: list[EvidenceItem] = []
    if missing:
        subject = ", ".join(missing[:8])
        if len(missing) > 8:
            subject += ", ..."
        evidence.append(
            make_evidence(
                category="missing_ethics_documentation",
                file_path="README/docs" if docs_files else ".",
                reason=f"Documentation does not appear to cover: {subject}. Missing documentation alone is treated as low-severity unknown context unless paired with concrete risk evidence.",
                confidence="medium",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)

