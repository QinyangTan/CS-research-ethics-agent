"""Detect dataset storage, release, and re-identification signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import (
    dedupe_evidence,
    iter_repo_file_paths,
    iter_repo_files,
    make_evidence,
    make_match_evidence,
    read_text_file,
)
from repo_ethics.engine.text_signals import find_negated_topic_mentions, find_positive_topic_mentions, topic_is_covered
from repo_ethics.schemas import EvidenceItem


DATA_FILE_EXTENSIONS = {".csv", ".tsv", ".json", ".jsonl", ".parquet", ".sqlite", ".db", ".feather", ".arrow", ".pkl", ".pickle"}
PICKLE_EXTENSIONS = {".pkl", ".pickle"}
DATA_NAME_HINTS = {"schema", "data", "records", "samples", "posts", "users", "annotations", "labels", "dataset"}
DATA_DIRS = {"data", "dataset", "datasets"}

RELEASE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bpush_to_hub\b|\bhuggingface\b.*\bdataset\b", re.I | re.S), "References Hugging Face dataset upload or release."),
    (re.compile(r"\bkaggle\b.*\bupload\b", re.I | re.S), "References Kaggle dataset upload."),
    (re.compile(r"\bs3\.(upload_file|download_file)|aws s3 cp\b", re.I), "References S3 data upload/download."),
    (re.compile(r"\bpublic dataset|release dataset|dataset release|publish dataset|data release\b", re.I), "Mentions public dataset release."),
]

POLICY_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "data card/datasheet": [re.compile(r"\bdata card|datacard|datasheet\b", re.I)],
    "retention/deletion policy": [re.compile(r"\bretention|deletion policy|delete data|deletion\b", re.I)],
    "anonymization/de-identification policy": [re.compile(r"\banonymi[sz]ation|de-identification|deidentified\b", re.I)],
}


def _is_missing_context_clause(clause: str) -> bool:
    lower = clause.lower()
    return any(
        phrase in lower
        for phrase in [
            "not documented",
            "not yet documented",
            "missing",
            "unclear",
            "unknown",
            "not specified",
            "not described",
            "not stated",
            "not addressed",
            "lacks",
            "to be determined",
            "tbd",
        ]
    )


def _path_parts(rel_path: str) -> list[str]:
    return [part.lower() for part in Path(rel_path).parts]


def _is_data_like_path(rel_path: str) -> bool:
    suffix = Path(rel_path).suffix.lower()
    if suffix not in DATA_FILE_EXTENSIONS:
        return False
    parts = _path_parts(rel_path)
    name = Path(rel_path).name.lower()
    stem = Path(rel_path).stem.lower()
    if name in {"package.json", "tsconfig.json", "pyproject.toml"}:
        return False
    if parts and parts[0] in DATA_DIRS:
        return True
    if any(part in DATA_DIRS for part in parts[:-1]):
        return True
    if any(hint in stem for hint in DATA_NAME_HINTS):
        return True
    return False


def _dataset_file_confidence(rel_path: str) -> str:
    suffix = Path(rel_path).suffix.lower()
    parts = _path_parts(rel_path)
    if suffix in PICKLE_EXTENSIONS and not (parts and parts[0] in DATA_DIRS):
        return "low"
    return "medium"


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    saw_data = False
    saw_release = False
    repo_text_parts: list[str] = []

    for scanned in iter_repo_file_paths(root_path, include_binary=True, max_file_size=None):
        if _is_data_like_path(scanned.rel_path):
            saw_data = True
            evidence.append(
                make_evidence(
                    category="dataset_release_reidentification",
                    file_path=scanned.rel_path,
                    reason="Repository contains a dataset-like file by extension; content was not read. Release, retention, and de-identification review may be needed if it contains research data.",
                    confidence=_dataset_file_confidence(scanned.rel_path),  # type: ignore[arg-type]
                    evidence_type="risk_signal",
                    include_snippets=include_snippets,
                )
            )

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        repo_text_parts.append(text[:4000])

        for pattern, reason in RELEASE_PATTERNS:
            for start, end, _ in find_positive_topic_mentions(text, [pattern]):
                saw_release = True
                evidence.append(
                    make_match_evidence(
                        category="dataset_release_reidentification",
                        file_path=scanned.rel_path,
                        text=text,
                        start=start,
                        end=end,
                        reason=reason,
                        confidence="high",
                        evidence_type="risk_signal",
                        include_snippets=include_snippets,
                    )
                )
            for start, end, clause in find_negated_topic_mentions(text, [pattern]):
                if not _is_missing_context_clause(clause):
                    continue
                evidence.append(
                    make_match_evidence(
                        category="dataset_release_reidentification",
                        file_path=scanned.rel_path,
                        text=text,
                        start=start,
                        end=end,
                        reason="Dataset release or sharing is mentioned as absent, unclear, or not documented.",
                        confidence="medium",
                        evidence_type="missing_context",
                        include_snippets=include_snippets,
                    )
                )

        for topic, patterns in POLICY_PATTERNS.items():
            for start, end, _ in find_positive_topic_mentions(text, patterns):
                evidence.append(
                    make_match_evidence(
                        category="dataset_release_reidentification",
                        file_path=scanned.rel_path,
                        text=text,
                        start=start,
                        end=end,
                        reason=f"Documentation includes {topic}.",
                        confidence="medium",
                        evidence_type="positive_control",
                        include_snippets=include_snippets,
                    )
                )

    repo_text = "\n".join(repo_text_parts)
    missing_policy_topics = [topic for topic, patterns in POLICY_PATTERNS.items() if not topic_is_covered(repo_text, patterns)]
    if (saw_data or saw_release) and missing_policy_topics:
        evidence.append(
            make_evidence(
                category="dataset_release_reidentification",
                file_path=".",
                reason="Dataset files or release language were detected, but the following context may need clarification: "
                + ", ".join(missing_policy_topics)
                + ".",
                confidence="medium",
                evidence_type="missing_context",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)
