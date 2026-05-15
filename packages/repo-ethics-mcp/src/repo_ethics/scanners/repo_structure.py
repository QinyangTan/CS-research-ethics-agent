"""Repository structure discovery and project profile construction."""

from __future__ import annotations

from pathlib import Path

from repo_ethics.constants import LANGUAGE_BY_EXTENSION
from repo_ethics.engine.evidence_engine import iter_repo_files, read_text_file, resolve_root
from repo_ethics.engine.text_signals import strip_negated_sentences
from repo_ethics.schemas import ProjectProfile
from repo_ethics.scanners.file_classifier import classify_file


IMPORTANT_NAMES = {
    "readme.md",
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    "dockerfile",
    "license",
    "license.md",
    "security.md",
    "contributing.md",
    "ethics.md",
}

DATA_SOURCE_KEYWORDS = {
    "reddit": "Reddit",
    "twitter": "Twitter/X",
    "youtube": "YouTube",
    "kaggle": "Kaggle",
    "huggingface": "Hugging Face",
    "s3": "S3",
    "web scrape": "web scraping",
    "scrap": "web scraping",
    "api": "API",
}

ACTIVITY_KEYWORDS = {
    "classification": "classification",
    "nlp": "NLP",
    "machine learning": "machine learning",
    "scrap": "web scraping",
    "survey": "survey",
    "attendance": "attendance tracking",
    "face": "face analysis",
    "vulnerability": "vulnerability scanning",
    "security": "security research",
    "dataset": "dataset construction",
}


def detect_languages(paths: list[str]) -> list[str]:
    languages = {
        LANGUAGE_BY_EXTENSION[Path(path).suffix.lower()]
        for path in paths
        if Path(path).suffix.lower() in LANGUAGE_BY_EXTENSION
    }
    return sorted(languages)


def important_files(paths: list[str]) -> list[str]:
    result: list[str] = []
    for path in paths:
        rel = path.lower()
        name = Path(path).name.lower()
        classification = classify_file(path)
        if (
            name in IMPORTANT_NAMES
            or rel.startswith("docs/")
            or rel.startswith("data/")
            or "paper" in rel
            or classification in {"ethics_documentation", "data_schema", "data_file"}
        ):
            result.append(path)
    return sorted(result)


def _read_repo_text(root: Path, files: list[str], max_chars: int = 80_000) -> str:
    parts: list[str] = []
    total = 0
    for rel in files:
        if classify_file(rel) not in {"project_description", "documentation", "data_schema", "source_code"}:
            continue
        path = root / rel
        try:
            text = read_text_file(path)
        except OSError:
            continue
        total += len(text)
        parts.append(text[:4000])
        if total >= max_chars:
            break
    return "\n".join(parts).lower()


def build_project_profile(root_path: str | Path, max_file_size: int = 524_288) -> ProjectProfile:
    root = resolve_root(root_path)
    scanned = list(iter_repo_files(root, max_file_size=max_file_size))
    paths = [item.rel_path for item in scanned]
    repo_text = _read_repo_text(root, paths)
    signal_text = strip_negated_sentences(repo_text)

    detected_sources = sorted({label for keyword, label in DATA_SOURCE_KEYWORDS.items() if keyword in signal_text})
    detected_activities = sorted({label for keyword, label in ACTIVITY_KEYWORDS.items() if keyword in signal_text})

    lower_paths = {path.lower() for path in paths}
    missing_docs: list[str] = []
    if not any(path.endswith("readme.md") for path in lower_paths):
        missing_docs.append("README.md")
    if not any("license" == Path(path).name.lower() or Path(path).name.lower().startswith("license.") for path in lower_paths):
        missing_docs.append("LICENSE")
    if not any("ethics" in path or "privacy" in path or "data_card" in path or "datasheet" in path for path in lower_paths):
        missing_docs.append("ethics/privacy/data handling documentation")

    human_terms = ["user", "student", "participant", "patient", "email", "username", "face", "biometric", "demographic"]
    security_terms = ["cve", "exploit", "vulnerability", "nmap", "metasploit", "scanner"]

    return ProjectProfile(
        root_path=str(root),
        project_name=root.name,
        languages=detect_languages(paths),
        important_files=important_files(paths),
        detected_research_activities=detected_activities,
        detected_data_sources=detected_sources,
        possible_human_data=any(term in signal_text for term in human_terms),
        possible_security_sensitive=any(term in signal_text for term in security_terms),
        possible_dual_use=any(term in signal_text for term in security_terms),
        missing_docs=missing_docs,
    )


def build_file_tree(root_path: str | Path, max_file_size: int = 524_288) -> list[str]:
    return [item.rel_path for item in iter_repo_files(root_path, max_file_size=max_file_size)]
