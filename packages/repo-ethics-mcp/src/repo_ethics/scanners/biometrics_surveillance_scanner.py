"""Detect biometrics and surveillance/tracking signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_match_evidence, read_text_file
from repo_ethics.engine.text_signals import find_positive_topic_mentions
from repo_ethics.schemas import EvidenceItem


PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("biometrics", re.compile(r"\bface_recognition\b|\bdeepface\b|\bretinaface\b|\bface embedding\b", re.I), "References face recognition or biometric libraries/data."),
    ("biometrics", re.compile(r"\bcv2\.(CascadeClassifier|detectMultiScale)\b|haar.?cascade.*face", re.I), "Uses OpenCV face detection patterns."),
    ("biometrics", re.compile(r"\bmediapipe\b.*\bface mesh\b|\bgait recognition\b|\bemotion detection\b", re.I | re.S), "References biometric, gait, or emotion analysis."),
    ("surveillance_tracking", re.compile(r"\battendance tracking\b|\bclassroom attendance\b|\bsurveillance\b", re.I), "References attendance or surveillance tracking."),
    ("surveillance_tracking", re.compile(r"\bperson re-?identification\b|\btrack(?:ing)? people across cameras\b|\bmulti-camera tracking\b", re.I), "References person re-identification or cross-camera tracking."),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        for category, pattern, reason in PATTERNS:
            for start, end, _ in find_positive_topic_mentions(text, [pattern]):
                evidence.append(
                    make_match_evidence(
                        category=category,
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
    return dedupe_evidence(evidence)
