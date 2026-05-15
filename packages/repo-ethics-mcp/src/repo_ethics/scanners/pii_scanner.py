"""Detect personal, sensitive, or identifiable data signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, line_window_for_match, make_evidence, read_text_file
from repo_ethics.engine.text_signals import find_positive_topic_mentions
from repo_ethics.schemas import EvidenceItem


PII_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("username", re.compile(r"\b(user_?names?|screen_?names?|handles?)\b", re.I), "References usernames or handles."),
    ("user_id", re.compile(r"\b(user_?id|account_?id|author_?id)\b", re.I), "References user identifiers."),
    ("email", re.compile(r"\b(email|e-mail|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})\b", re.I), "References email addresses."),
    ("phone", re.compile(r"\b(phone|telephone|mobile)\b", re.I), "References phone numbers."),
    ("address", re.compile(r"\b(address|street_address|home_address)\b", re.I), "References physical addresses."),
    ("location", re.compile(r"\b(location|geolocation|geo_?lat|geo_?lon|latitude|longitude|gps)\b", re.I), "References location or GPS data."),
    ("ip_address", re.compile(r"\b(ip_?address|remote_addr|\d{1,3}(?:\.\d{1,3}){3})\b", re.I), "References IP addresses."),
    ("face", re.compile(r"\b(face|facial|face_?embedding)\b", re.I), "References facial data."),
    ("image", re.compile(r"\b(image|photo|picture|video frame)\b", re.I), "References images or media that may identify people."),
    ("biometric", re.compile(r"\b(biometric|fingerprint|iris recognition|iris scan|iris biometric|voiceprint|gait)\b", re.I), "References biometric data."),
    ("medical", re.compile(r"\b(medical|health|diagnosis|patient|clinical)\b", re.I), "References health or medical data."),
    ("student_id", re.compile(r"\b(student_?id|school_?record|gradebook|education record)\b", re.I), "References student records or identifiers."),
    ("demographic", re.compile(r"\b(demographic|race|ethnicity|gender|religion|political|income)\b", re.I), "References demographic or sensitive attributes."),
    ("timestamp", re.compile(r"\b(exact_?timestamps?|created_?at|timestamps?|datetime)\b", re.I), "References exact timestamps."),
    ("profile_url", re.compile(r"\b(profile_?url|permalink|author_url)\b", re.I), "References profile URLs or permalinks."),
    ("social_graph", re.compile(r"\b(followers|following|friends|social graph|friend_?list)\b", re.I), "References social graph data."),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        for _, pattern, reason in PII_PATTERNS:
            for start, end, clause in find_positive_topic_mentions(text, [pattern]):
                line_start, line_end, _ = line_window_for_match(text, start, end)
                evidence.append(
                    make_evidence(
                        category="privacy_identifiability",
                        file_path=scanned.rel_path,
                        line_start=line_start,
                        line_end=line_end,
                        snippet=f"{clause.strip()}\nMatched: {text[start:end]}",
                        reason=reason,
                        confidence="medium",
                        evidence_type="risk_signal",
                        include_snippets=include_snippets,
                    )
                )
    return dedupe_evidence(evidence)
