"""Detect dataset storage, release, and re-identification signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, is_negated_match, iter_repo_files, make_evidence, make_match_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


DATA_FILE_EXTENSIONS = {".csv", ".json", ".jsonl", ".parquet", ".sqlite", ".db"}
RELEASE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bpush_to_hub\b|\bhuggingface\b.*\bdataset\b", re.I | re.S), "References Hugging Face dataset upload or release."),
    (re.compile(r"\bkaggle\b.*\bupload\b", re.I | re.S), "References Kaggle dataset upload."),
    (re.compile(r"\bs3\.(upload_file|download_file)|aws s3 cp\b", re.I), "References S3 data upload/download."),
    (re.compile(r"\bpublic dataset|release dataset|publish dataset|data release\b", re.I), "Mentions public dataset release."),
]

POLICY_PATTERNS = [
    re.compile(r"\bdata card|datacard|datasheet\b", re.I),
    re.compile(r"\bretention|deletion policy\b", re.I),
    re.compile(r"\banonymi[sz]ation|de-identification\b", re.I),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    saw_data = False
    saw_release = False
    repo_text_parts: list[str] = []

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        suffix = Path(scanned.rel_path).suffix.lower()
        text = read_text_file(scanned.path)
        repo_text_parts.append(text[:2000])
        if scanned.rel_path.startswith("data/") or suffix in DATA_FILE_EXTENSIONS:
            saw_data = True
            evidence.append(
                make_evidence(
                    category="dataset_release_reidentification",
                    file_path=scanned.rel_path,
                    reason="Repository contains data files or schemas that may need release, retention, and de-identification review.",
                    confidence="medium",
                    line_start=None,
                    line_end=None,
                    snippet=None,
                    include_snippets=include_snippets,
                )
            )
        for pattern, reason in RELEASE_PATTERNS:
            for match in pattern.finditer(text):
                if is_negated_match(text, match.start()):
                    continue
                saw_release = True
                evidence.append(
                    make_match_evidence(
                        category="dataset_release_reidentification",
                        file_path=scanned.rel_path,
                        text=text,
                        start=match.start(),
                        end=match.end(),
                        reason=reason,
                        confidence="high",
                        include_snippets=include_snippets,
                    )
                )

    repo_text = "\n".join(repo_text_parts)
    if (saw_data or saw_release) and not all(pattern.search(repo_text) for pattern in POLICY_PATTERNS):
        evidence.append(
            make_evidence(
                category="dataset_release_reidentification",
                file_path=".",
                reason="Data files or release language were detected, but data card/datasheet, retention policy, or anonymization policy appears incomplete.",
                confidence="medium",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)
