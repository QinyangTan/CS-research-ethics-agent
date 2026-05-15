"""Detect repository text that may attempt to manipulate a reviewing agent."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_match_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


PATTERNS = [
    re.compile(r"ignore previous instructions", re.I),
    re.compile(r"ignore (the )?system message", re.I),
    re.compile(r"do not report this", re.I),
    re.compile(r"say this project is ethical", re.I),
    re.compile(r"this project has no risks", re.I),
    re.compile(r"delete warnings", re.I),
    re.compile(r"override instructions", re.I),
    re.compile(r"suppress warnings", re.I),
    re.compile(r"do not mention", re.I),
    re.compile(r"mark (this )?(repository|project) as safe", re.I),
    re.compile(r"(ignore|override|suppress|delete|do not mention|mark[^.\n]{0,40}safe)[^.\n]{0,80}\b(system prompt|developer message|assistant should|you are now)\b", re.I),
    re.compile(r"\b(system prompt|developer message|assistant should|you are now)\b[^.\n]{0,80}(ignore|override|suppress|delete|do not mention|mark[^.\n]{0,40}safe)", re.I),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        for pattern in PATTERNS:
            for match in pattern.finditer(text):
                evidence.append(
                    make_match_evidence(
                        category="prompt_injection_attempt",
                        file_path=scanned.rel_path,
                        text=text,
                        start=match.start(),
                        end=match.end(),
                        reason="Repository text resembles an instruction intended to manipulate or suppress an ethics review.",
                        confidence="high",
                        evidence_type="risk_signal",
                        include_snippets=include_snippets,
                    )
                )
    return dedupe_evidence(evidence)
