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

