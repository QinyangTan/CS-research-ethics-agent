"""Detect web scraping, browser automation, and platform API collection signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_evidence, make_match_evidence, read_text_file
from repo_ethics.engine.text_signals import find_positive_topic_mentions, topic_is_covered
from repo_ethics.schemas import EvidenceItem


SCRAPING_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\brequests\.(get|post)\s*\(", re.I), "Uses Python requests for HTTP collection."),
    (re.compile(r"\burllib(?:\.request)?\b", re.I), "Uses urllib for HTTP collection."),
    (re.compile(r"\b(BeautifulSoup|bs4)\b", re.I), "Uses BeautifulSoup/bs4 for HTML parsing."),
    (re.compile(r"\bscrapy\b", re.I), "Uses Scrapy for web crawling."),
    (re.compile(r"\bselenium\b", re.I), "Uses Selenium browser automation."),
    (re.compile(r"\bplaywright\b", re.I), "Uses Playwright browser automation."),
    (re.compile(r"\bpraw\b", re.I), "Uses PRAW for Reddit collection."),
    (re.compile(r"\btweepy\b", re.I), "Uses Tweepy for platform data collection."),
    (re.compile(r"\bsnscrape\b", re.I), "Uses snscrape for platform scraping."),
    (re.compile(r"\binstaloader\b", re.I), "Uses Instaloader for Instagram data collection."),
    (re.compile(r"\byoutube(?:\s+data)?\s+api\b", re.I), "Mentions YouTube API collection."),
    (re.compile(r"(?<!def\s)\bfetch\s*\(", re.I), "Uses JavaScript fetch for HTTP collection."),
    (re.compile(r"\baxios\.", re.I), "Uses axios for HTTP collection."),
    (re.compile(r"\bpuppeteer\b", re.I), "Uses Puppeteer browser automation."),
    (re.compile(r"\bcheerio\b", re.I), "Uses Cheerio for HTML parsing."),
    (re.compile(r"\brequest\s*\(", re.I), "Uses request-like HTTP collection."),
]

GOVERNANCE_TOPICS: dict[str, list[re.Pattern[str]]] = {
    "platform terms": [re.compile(r"\bterms of service|tos|platform terms\b", re.I)],
    "robots.txt": [re.compile(r"\brobots\.txt\b", re.I)],
    "rate limits": [re.compile(r"\brate[- ]?limit|sleep\(|backoff|retry-after", re.I)],
    "data policy": [re.compile(r"\bdata policy|API policy|collection policy\b", re.I)],
}


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    saw_scraping = False
    docs_text = ""

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        lower_path = scanned.rel_path.lower()
        if lower_path.endswith((".md", ".rst", ".txt")):
            docs_text += "\n" + text
            for topic, patterns in GOVERNANCE_TOPICS.items():
                for start, end, _ in find_positive_topic_mentions(text, patterns):
                    evidence.append(
                        make_match_evidence(
                            category="web_scraping_platform_governance",
                            file_path=scanned.rel_path,
                            text=text,
                            start=start,
                            end=end,
                            reason=f"Documentation includes {topic} guidance.",
                            confidence="medium",
                            evidence_type="positive_control",
                            include_snippets=include_snippets,
                        )
                    )
        for pattern, reason in SCRAPING_PATTERNS:
            for start, end, _ in find_positive_topic_mentions(text, [pattern]):
                saw_scraping = True
                evidence.append(
                    make_match_evidence(
                        category="web_scraping_platform_governance",
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

    missing_topics = [topic for topic, patterns in GOVERNANCE_TOPICS.items() if not topic_is_covered(docs_text, patterns)]
    if saw_scraping and missing_topics:
        evidence.append(
            make_evidence(
                category="web_scraping_platform_governance",
                file_path="README/docs",
                reason="Scraping or API collection was detected, but README/docs do not positively document: "
                + ", ".join(missing_topics)
                + ".",
                confidence="medium",
                evidence_type="missing_context",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)
