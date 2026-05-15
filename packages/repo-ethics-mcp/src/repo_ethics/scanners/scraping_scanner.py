"""Detect web scraping, browser automation, and platform API collection signals."""

from __future__ import annotations

import re
from pathlib import Path

from repo_ethics.engine.evidence_engine import dedupe_evidence, iter_repo_files, make_evidence, make_match_evidence, read_text_file
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
    (re.compile(r"\bfetch\s*\(", re.I), "Uses JavaScript fetch for HTTP collection."),
    (re.compile(r"\baxios\.", re.I), "Uses axios for HTTP collection."),
    (re.compile(r"\bpuppeteer\b", re.I), "Uses Puppeteer browser automation."),
    (re.compile(r"\bcheerio\b", re.I), "Uses Cheerio for HTML parsing."),
    (re.compile(r"\brequest\s*\(", re.I), "Uses request-like HTTP collection."),
]

GOVERNANCE_PATTERNS = [
    re.compile(r"\brobots\.txt\b", re.I),
    re.compile(r"\brate[- ]?limit|sleep\(|backoff|retry-after", re.I),
    re.compile(r"\bterms of service|tos|platform terms|data policy\b", re.I),
]


def scan(root_path: str | Path, max_file_size: int = 524_288, include_snippets: bool = True) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    saw_scraping = False
    saw_governance = False
    docs_text = ""

    for scanned in iter_repo_files(root_path, max_file_size=max_file_size):
        text = read_text_file(scanned.path)
        lower_path = scanned.rel_path.lower()
        if lower_path.endswith((".md", ".rst", ".txt")):
            docs_text += "\n" + text
        if any(pattern.search(text) for pattern in GOVERNANCE_PATTERNS):
            saw_governance = True
        for pattern, reason in SCRAPING_PATTERNS:
            for match in pattern.finditer(text):
                saw_scraping = True
                evidence.append(
                    make_match_evidence(
                        category="web_scraping_platform_governance",
                        file_path=scanned.rel_path,
                        text=text,
                        start=match.start(),
                        end=match.end(),
                        reason=reason,
                        confidence="high",
                        include_snippets=include_snippets,
                    )
                )

    docs_have_governance = any(pattern.search(docs_text) for pattern in GOVERNANCE_PATTERNS)
    if saw_scraping and not (saw_governance and docs_have_governance):
        evidence.append(
            make_evidence(
                category="web_scraping_platform_governance",
                file_path=".",
                reason="Scraping or API collection was detected, but README/docs do not document platform terms, robots.txt, rate limits, or data policy.",
                confidence="medium",
                include_snippets=include_snippets,
            )
        )
    return dedupe_evidence(evidence)

