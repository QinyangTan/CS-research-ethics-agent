"""Conditional checks for ethics, privacy, safety, and release documentation."""

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
from repo_ethics.engine.text_signals import find_positive_topic_mentions, topic_is_covered
from repo_ethics.schemas import EvidenceItem


SIGNAL_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "scraping": [
        re.compile(r"\brequests\.(get|post)\s*\(|BeautifulSoup|bs4|scrapy|selenium|playwright|praw|tweepy|snscrape|instaloader|API collection|scrap", re.I)
    ],
    "pii": [
        re.compile(r"\b(user_?names?|user_?id|email|location|face|biometric|student_?id|patient|demographic|profile_?url|timestamp)\b", re.I)
    ],
    "dataset": [
        re.compile(r"\bpublic dataset|release dataset|dataset release|publish dataset|data release|data directory\b", re.I)
    ],
    "security": [
        re.compile(r"\bexploit|CVE|vulnerability scanner|nmap|socket scanning|fuzzing|malware|phishing|credential dumping\b", re.I)
    ],
    "biometrics": [
        re.compile(r"\bface_recognition|cv2\.(?:CascadeClassifier|detectMultiScale)|deepface|face embedding|attendance tracking|surveillance\b", re.I)
    ],
    "ml": [
        re.compile(r"\bsklearn|torch|tensorflow|transformers|classification of people|profiling|recommender system|toxicity|emotion detection\b", re.I)
    ],
}

TOPIC_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "README/project purpose": [re.compile(r"\bpurpose|project|prototype|research|visuali[sz]es?\b", re.I)],
    "platform terms": [re.compile(r"\bplatform terms|terms of service|tos\b", re.I)],
    "robots.txt or rate limiting": [re.compile(r"\brobots\.txt|rate[- ]?limit|sleep\(|backoff|retry-after\b", re.I)],
    "collection method/dates": [re.compile(r"\bcollection method|collected on|collection dates?|data collection\b", re.I)],
    "consent/reasonable expectation": [re.compile(r"\bconsent|notice|reasonable expectation\b", re.I)],
    "privacy": [re.compile(r"\bprivacy|personal data\b", re.I)],
    "anonymization/de-identification": [re.compile(r"\banonymi[sz]ation|de-identification|deidentified\b", re.I)],
    "data retention/deletion": [re.compile(r"\bretention|deletion|delete data|retained for\b", re.I)],
    "data access controls": [re.compile(r"\baccess control|data access|restricted access\b", re.I)],
    "data card/datasheet": [re.compile(r"\bdata card|datacard|datasheet\b", re.I)],
    "release policy": [re.compile(r"\brelease policy|public release|sharing policy|safe release\b", re.I)],
    "authorization/scope": [re.compile(r"\bauthori[sz]ation|authorized scope|safe targets?|scope\b", re.I)],
    "responsible disclosure": [re.compile(r"\bresponsible disclosure|vulnerability disclosure\b", re.I)],
    "misuse/dual-use limits": [re.compile(r"\bmisuse|abuse|dual-use|dual use\b", re.I)],
    "safe release boundaries": [re.compile(r"\bsafe release|release boundaries|withheld details\b", re.I)],
    "deployment limitations": [re.compile(r"\bdeployment limitations?|deployment limits?|non-use|not for deployment\b", re.I)],
    "bias/performance limitations": [re.compile(r"\bbias|fairness|performance limitations?|known limitations?\b", re.I)],
    "model card or limitations": [re.compile(r"\bmodel card|modelcard|limitations?|known limits\b", re.I)],
    "fairness/bias evaluation": [re.compile(r"\bfairness|bias evaluation|subgroup performance\b", re.I)],
    "deployment boundaries": [re.compile(r"\bdeployment boundaries|deployment limits?|intended use|non-use\b", re.I)],
    "limitations": [re.compile(r"\blimitations?|known limits\b", re.I)],
}


def _has_signal(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(find_positive_topic_mentions(text, [pattern]) for pattern in patterns)


def _has_dataset_path(root_path: str | Path, max_file_size: int) -> bool:
    for scanned in iter_repo_file_paths(root_path, include_binary=True, max_file_size=max_file_size):
        rel = scanned.rel_path.lower()
        suffix = Path(rel).suffix
        if (rel.startswith(("data/", "dataset/", "datasets/")) and suffix in {".csv", ".tsv", ".json", ".jsonl", ".parquet", ".sqlite", ".db", ".feather", ".arrow", ".pkl", ".pickle"}):
            return True
    return False


def _required_topics(signals: dict[str, bool]) -> list[str]:
    topics: list[str] = []
    if signals["scraping"]:
        topics.extend([
            "platform terms",
            "robots.txt or rate limiting",
            "collection method/dates",
            "consent/reasonable expectation",
        ])
        if signals["dataset"] or signals["pii"]:
            topics.append("data retention/deletion")
    if signals["pii"]:
        topics.extend([
            "privacy",
            "anonymization/de-identification",
            "data retention/deletion",
            "data access controls",
            "consent/reasonable expectation",
        ])
    if signals["dataset"]:
        topics.extend([
            "data card/datasheet",
            "release policy",
            "data retention/deletion",
            "anonymization/de-identification",
        ])
    if signals["security"]:
        topics.extend([
            "authorization/scope",
            "responsible disclosure",
            "misuse/dual-use limits",
            "safe release boundaries",
        ])
    if signals["biometrics"]:
        topics.extend([
            "consent/reasonable expectation",
            "privacy",
            "data retention/deletion",
            "data access controls",
            "deployment limitations",
            "bias/performance limitations",
        ])
    if signals["ml"] and signals["pii"]:
        topics.extend(["model card or limitations", "fairness/bias evaluation", "deployment boundaries"])
    if not any(signals.values()):
        topics.extend(["README/project purpose"])
    return sorted(set(topics))


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    repo_text = ""
    docs_text = ""
    docs_files: list[str] = []
    evidence: list[EvidenceItem] = []

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        repo_text += "\n" + text
        rel = scanned.rel_path.lower()
        if rel.endswith((".md", ".rst", ".txt")) or rel.startswith("docs/"):
            docs_files.append(scanned.rel_path)
            docs_text += "\n" + text
            if "security.md" == Path(rel).name:
                evidence.append(
                    make_evidence(
                        category="missing_ethics_documentation",
                        file_path=scanned.rel_path,
                        reason="Repository includes a security policy document.",
                        confidence="medium",
                        evidence_type="positive_control",
                        include_snippets=include_snippets,
                    )
                )
            if any(token in rel for token in ["ethics", "privacy", "data_card", "datacard", "datasheet", "model_card", "modelcard"]):
                evidence.append(
                    make_evidence(
                        category="missing_ethics_documentation",
                        file_path=scanned.rel_path,
                        reason="Repository includes dedicated ethics, privacy, data-card, or model-card documentation.",
                        confidence="medium",
                        evidence_type="positive_control",
                        include_snippets=include_snippets,
                    )
                )

    signals = {name: _has_signal(repo_text, patterns) for name, patterns in SIGNAL_PATTERNS.items()}
    signals["dataset"] = signals["dataset"] or _has_dataset_path(root_path, max_file_size)
    required = _required_topics(signals)

    covered_topics: list[str] = []
    missing_topics: list[str] = []
    for topic in required:
        patterns = TOPIC_PATTERNS[topic]
        if topic_is_covered(docs_text, patterns):
            covered_topics.append(topic)
            for start, end, _ in find_positive_topic_mentions(docs_text, patterns):
                evidence.append(
                    make_match_evidence(
                        category="missing_ethics_documentation",
                        file_path="README/docs",
                        text=docs_text,
                        start=start,
                        end=end,
                        reason=f"Documentation includes {topic}.",
                        confidence="medium",
                        evidence_type="positive_control",
                        include_snippets=include_snippets,
                    )
                )
                break
        else:
            missing_topics.append(topic)

    if missing_topics:
        subject = ", ".join(missing_topics[:8])
        if len(missing_topics) > 8:
            subject += ", ..."
        evidence.append(
            make_evidence(
                category="missing_ethics_documentation",
                file_path="README/docs" if docs_files else ".",
                reason=f"Repository evidence suggests these documentation topics may need clarification: {subject}. Missing context is not proof of wrongdoing.",
                confidence="medium",
                evidence_type="missing_context",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)

