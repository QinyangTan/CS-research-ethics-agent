from pathlib import Path

from repo_ethics.scanners.scraping_scanner import scan


def test_scraping_scanner_detects_common_patterns(tmp_path: Path) -> None:
    code = tmp_path / "scrape.py"
    code.write_text(
        "import requests\nfrom bs4 import BeautifulSoup\nfrom selenium import webdriver\nfrom playwright.sync_api import sync_playwright\nimport scrapy\nrequests.get('https://example.com')\n",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    text = " ".join(item.reason for item in evidence)
    assert "requests" in text
    assert "BeautifulSoup" in text
    assert "Selenium" in text
    assert "Playwright" in text
    assert "Scrapy" in text


def test_scraping_scanner_distinguishes_missing_and_positive_governance(tmp_path: Path) -> None:
    (tmp_path / "scrape.py").write_text("import requests\nrequests.get('https://example.com')\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("Platform terms are not documented.", encoding="utf-8")
    missing = scan(tmp_path)
    assert any(item.evidence_type == "missing_context" for item in missing)
    assert not any(item.evidence_type == "positive_control" for item in missing)

    (tmp_path / "README.md").write_text(
        "We reviewed platform terms and robots.txt. The collector uses rate limits.",
        encoding="utf-8",
    )
    positive = scan(tmp_path)
    assert any(item.evidence_type == "positive_control" for item in positive)

