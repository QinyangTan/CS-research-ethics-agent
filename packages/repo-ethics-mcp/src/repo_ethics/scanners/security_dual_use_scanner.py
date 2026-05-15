"""Detect security-sensitive and dual-use research signals without improving capability."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_match_evidence, read_text_file
from repo_ethics.schemas import EvidenceItem


SECURITY_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\bexploit\b", re.I), "Mentions exploit development or use.", "medium"),
    (re.compile(r"\bpayload\b", re.I), "Mentions payloads.", "medium"),
    (re.compile(r"\bshellcode\b", re.I), "Mentions shellcode.", "high"),
    (re.compile(r"\breverse shell\b", re.I), "Mentions reverse shells.", "high"),
    (re.compile(r"\bprivilege escalation\b", re.I), "Mentions privilege escalation.", "high"),
    (re.compile(r"\bCVE-\d{4}-\d+\b|\bCVE\b", re.I), "Mentions CVEs or vulnerability identifiers.", "medium"),
    (re.compile(r"\bfuzz(?:ing|er)?\b", re.I), "Mentions fuzzing.", "medium"),
    (re.compile(r"\bnmap\b", re.I), "Mentions nmap scanning.", "medium"),
    (re.compile(r"\bmetasploit\b|\bburp\b|\bsqlmap\b", re.I), "Mentions offensive security tooling.", "high"),
    (re.compile(r"\bscapy\b", re.I), "Mentions packet tooling.", "medium"),
    (re.compile(r"\bsocket\.(?:socket|connect_ex|connect)\b", re.I), "Uses socket scanning primitives.", "medium"),
    (re.compile(r"\bport scan|port_scan|scan_port|socket scanning\b", re.I), "Mentions socket or port scanning.", "medium"),
    (re.compile(r"\bpacket injection\b", re.I), "Mentions packet injection.", "high"),
    (re.compile(r"\bcredential dumping|password spraying\b", re.I), "Mentions credential attacks.", "high"),
    (re.compile(r"\bmalware|ransomware|keylogger|phishing|command and control|botnet\b", re.I), "Mentions malware or abuse infrastructure.", "high"),
    (re.compile(r"\bvulnerability scanner\b", re.I), "Describes vulnerability scanning.", "medium"),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        for pattern, reason, confidence in SECURITY_PATTERNS:
            for match in pattern.finditer(text):
                evidence.append(
                    make_match_evidence(
                        category="security_dual_use",
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

