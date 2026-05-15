"""Shared constants and conservative report language."""

from __future__ import annotations

DEFAULT_MAX_FILE_SIZE = 524_288
SNIPPET_MAX_CHARS = 240

DISCLAIMER = (
    "This is a local, evidence-grounded CS research ethics pre-review. It does not "
    "make final ethical, legal, compliance, or IRB determinations. Findings should "
    "be discussed with an advisor or appropriate review body, especially where "
    "context is missing."
)

FORBIDDEN_REPORT_PHRASES = [
    "This project is ethical",
    "This project is unethical",
    "IRB approval is required",
    "This violates IRB",
    "This is illegal",
    "This is compliant",
    "This is safe",
]

SAFE_RELEASE_CHECKLIST = [
    "Confirm the project purpose, affected populations, and deployment context are documented.",
    "Review whether data collection aligns with reasonable expectations and platform terms.",
    "Remove, aggregate, or protect direct identifiers and sensitive quasi-identifiers.",
    "Define data retention, deletion, access control, and sharing limits.",
    "Avoid public release of raw sensitive or identifiable records.",
    "Document known limitations, misuse risks, and appropriate use boundaries.",
    "Prepare responsible disclosure steps for security-sensitive work.",
    "Rotate any exposed credentials and keep secrets out of reports and commits.",
]

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".tox",
    ".idea",
    ".vscode",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".tgz",
    ".xz",
    ".7z",
    ".mp4",
    ".mov",
    ".avi",
    ".sqlite",
    ".db",
    ".parquet",
    ".pyc",
    ".so",
    ".dylib",
    ".exe",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".r": "R",
    ".ipynb": "Jupyter Notebook",
    ".md": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
}

