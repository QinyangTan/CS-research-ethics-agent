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
from repo_ethics.scanners.file_classifier import classify_file


SIGNAL_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "scraping": [
        re.compile(r"\brequests\.(get|post)\s*\(|BeautifulSoup|bs4|scrapy|selenium|playwright|praw|tweepy|snscrape|instaloader|API collection|scrap", re.I)
    ],
    "pii": [
        re.compile(r"\b(user_?names?|user_?id|email|location|gps|ip_?address|face|biometric|student_?id|patient|demographic|profile_?url)\b", re.I)
    ],
    "dataset": [
        re.compile(r"\bpublic dataset|release\s+(?:the\s+)?dataset|dataset release|publish\s+(?:the\s+)?dataset|share\s+(?:the\s+)?dataset|data release|data directory\b", re.I)
    ],
    "security": [
        re.compile(r"\bexploit|CVE|vulnerability scanner|nmap|socket scanning|port scanning|socket\.(?:socket|connect_ex|connect)|fuzzing|malware|phishing|credential dumping\b", re.I)
    ],
    "biometrics": [
        re.compile(r"\bface_recognition|cv2\.(?:CascadeClassifier|detectMultiScale)|deepface|face embedding|attendance tracking|surveillance|multi-camera tracking|track_people|tracking people|people across cameras|person re-identification\b", re.I)
    ],
    "ml": [
        re.compile(r"\bsklearn|torch|tensorflow|transformers|classification of people|profiling|recommender system|toxicity|emotion detection\b", re.I)
    ],
}
SENSITIVE_ML_PATTERNS = [
    re.compile(
        r"\btoxicity|emotion detection|recommender system|profiling|engagement ranking|manipulation risks?|admissions?|hiring|credit risk|classification of people|user comments?\b",
        re.I,
    )
]

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


def _doc_has_concrete_control(rel_path: str, text: str) -> bool:
    rel = rel_path.lower()
    lower = text.lower()
    if Path(rel).name == "security.md":
        return any(term in lower for term in ["responsible disclosure", "authorization", "scope", "misuse", "safe release", "release boundaries"])
    if any(token in rel for token in ["data_card", "datacard", "datasheet"]):
        return any(term in lower for term in ["source", "provenance", "intended use", "retention", "deletion", "license", "release", "access"])
    if any(token in rel for token in ["privacy", "ethics"]):
        return any(term in lower for term in ["privacy", "consent", "retention", "access", "de-identification", "anonymization", "deletion"])
    if any(token in rel for token in ["model_card", "modelcard"]):
        return any(term in lower for term in ["intended use", "limitations", "fairness", "bias", "deployment"])
    return False


def _is_excluded_signal_path(rel_path: str) -> bool:
    parts = Path(rel_path.lower()).parts
    return bool(parts and parts[0] in {"test", "tests", "eval", "benchmarks", "benchmark", "skills"})


def _is_signal_source(rel_path: str) -> bool:
    if _is_excluded_signal_path(rel_path):
        return False
    classification = classify_file(rel_path)
    if classification in {"project_description", "source_code", "data_schema", "dependency_manifest", "notebook"}:
        return True
    name = Path(rel_path.lower()).name
    if name in {"dockerfile", "compose.yaml", "docker-compose.yml"}:
        return True
    return False


def _is_documentation_source(rel_path: str) -> bool:
    classification = classify_file(rel_path)
    if classification in {"project_description", "documentation", "ethics_documentation", "security_policy"}:
        return True
    suffix = Path(rel_path.lower()).suffix
    return suffix in {".md", ".rst", ".txt"} or rel_path.lower().startswith("docs/")


def _is_fallback_project_doc(rel_path: str) -> bool:
    rel = rel_path.lower()
    name = Path(rel).stem
    if not rel.startswith("docs/"):
        return False
    return name in {"index", "overview", "project", "readme", "introduction"} or "overview" in name


def _has_dataset_path(root_path: str | Path, max_file_size: int) -> bool:
    for scanned in iter_repo_file_paths(root_path, include_binary=True, max_file_size=None):
        rel = scanned.rel_path.lower()
        suffix = Path(rel).suffix
        if (rel.startswith(("data/", "dataset/", "datasets/")) and suffix in {".csv", ".tsv", ".json", ".jsonl", ".parquet", ".sqlite", ".db", ".feather", ".arrow", ".pkl", ".pickle"}):
            return True
    return False


def _required_topics(signals: dict[str, bool], *, has_project_source: bool, has_readme: bool) -> list[str]:
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
    if signals["dataset"] and (signals["pii"] or signals["scraping"] or signals.get("dataset_release", False)):
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
    if signals["ml"] and (signals["pii"] or signals.get("sensitive_ml", False)):
        topics.extend(["model card or limitations", "fairness/bias evaluation", "deployment boundaries"])
    if not any(signals.values()) and has_project_source and not has_readme:
        topics.extend(["README/project purpose"])
    return sorted(set(topics))


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    signal_text = ""
    docs_text = ""
    docs: list[tuple[str, str]] = []
    fallback_docs: list[tuple[str, str]] = []
    docs_files: list[str] = []
    evidence: list[EvidenceItem] = []
    has_project_source = False
    has_readme = False

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        rel = scanned.rel_path.lower()
        if classify_file(scanned.rel_path) == "project_description":
            has_readme = True
        if _is_signal_source(scanned.rel_path):
            signal_text += "\n" + text
            if classify_file(scanned.rel_path) in {"project_description", "source_code", "data_schema", "notebook"}:
                has_project_source = True
        if _is_documentation_source(scanned.rel_path):
            docs_files.append(scanned.rel_path)
            docs.append((scanned.rel_path, text))
            docs_text += "\n" + text
            if _is_fallback_project_doc(scanned.rel_path):
                fallback_docs.append((scanned.rel_path, text))
            if "security.md" == Path(rel).name and _doc_has_concrete_control(scanned.rel_path, text):
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
            if any(token in rel for token in ["ethics", "privacy", "data_card", "datacard", "datasheet", "model_card", "modelcard"]) and _doc_has_concrete_control(scanned.rel_path, text):
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

    if not signal_text.strip() and fallback_docs:
        signal_text = "\n".join(text for _, text in fallback_docs)

    signals = {name: _has_signal(signal_text, patterns) for name, patterns in SIGNAL_PATTERNS.items()}
    signals["dataset"] = signals["dataset"] or _has_dataset_path(root_path, max_file_size)
    signals["dataset_release"] = _has_signal(signal_text, SIGNAL_PATTERNS["dataset"])
    signals["sensitive_ml"] = _has_signal(signal_text, SENSITIVE_ML_PATTERNS)
    required = _required_topics(signals, has_project_source=has_project_source, has_readme=has_readme)

    covered_topics: list[str] = []
    missing_topics: list[str] = []
    for topic in required:
        patterns = TOPIC_PATTERNS[topic]
        if topic_is_covered(docs_text, patterns):
            covered_topics.append(topic)
            if topic == "README/project purpose":
                continue
            for doc_path, doc_text in docs:
                mentions = find_positive_topic_mentions(doc_text, patterns)
                if not mentions:
                    continue
                start, end, _ = mentions[0]
                evidence.append(
                    make_match_evidence(
                        category="missing_ethics_documentation",
                        file_path=doc_path,
                        text=doc_text,
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
