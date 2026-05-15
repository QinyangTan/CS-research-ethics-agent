"""Check that the project does not implement hosted LLM API call paths."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ALLOWLIST_COMMENT = "repo-ethics-allow-hosted-llm-pattern"
IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
}
IGNORE_PREFIXES = {
    Path("benchmarks") / "fixtures",
    Path("benchmarks") / "outputs",
    Path("benchmarks") / "results",
}
IGNORE_FILES = {
    Path("scripts") / "check_no_hosted_llm_calls.py",
}
SCAN_SUFFIXES = {
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".md",
    ".txt",
}
ALLOWLISTED_PATTERN_FILES = {
    Path("packages") / "repo-ethics-mcp" / "src" / "repo_ethics" / "scanners" / "secret_scanner.py",
}


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    markdown_scan: bool = True
    requires_anthropic_context: bool = False


@dataclass(frozen=True)
class Violation:
    path: str
    line: int
    pattern: str
    text: str


RULES = [
    Rule("import openai", re.compile(r"\bimport\s+openai\b")),
    Rule("from openai", re.compile(r"\bfrom\s+openai\b")),
    Rule("OpenAI client", re.compile(r"\bOpenAI\s*\(")),
    Rule("AsyncOpenAI client", re.compile(r"\bAsyncOpenAI\s*\(")),
    Rule("import anthropic", re.compile(r"\bimport\s+anthropic\b")),
    Rule("from anthropic", re.compile(r"\bfrom\s+anthropic\b")),
    Rule("Anthropic client", re.compile(r"\bAnthropic\s*\(")),
    Rule("AsyncAnthropic client", re.compile(r"\bAsyncAnthropic\s*\(")),
    Rule("Claude model id", re.compile(r"\bclaude-[A-Za-z0-9._-]+")),
    Rule("Anthropic API URL", re.compile(r"api\.anthropic\.com")),
    Rule("OpenAI API URL", re.compile(r"api\.openai\.com")),
    Rule("OpenAI chat completions", re.compile(r"client\.chat\.completions")),
    Rule("OpenAI responses create", re.compile(r"\bresponses\.create\s*\(")),
    Rule("chat completions create", re.compile(r"\bchat\.completions\.create\s*\(")),
    Rule("Anthropic messages create", re.compile(r"\bmessages\.create\s*\("), requires_anthropic_context=True),
    Rule("Google generative AI", re.compile(r"\bgoogle\.generativeai\b")),
    Rule("Google genai client", re.compile(r"\bgenai\.Client\s*\(")),
    Rule("import mistralai", re.compile(r"\bimport\s+mistralai\b")),
    Rule("from mistralai", re.compile(r"\bfrom\s+mistralai\b")),
    Rule("Mistral client", re.compile(r"\bMistral\s*\(")),
    Rule("Mistral API URL", re.compile(r"api\.mistral\.ai")),
    Rule("import groq", re.compile(r"\bimport\s+groq\b")),
    Rule("from groq", re.compile(r"\bfrom\s+groq\b")),
    Rule("Groq client", re.compile(r"\bGroq\s*\(")),
    Rule("Groq API URL", re.compile(r"api\.groq\.com")),
    Rule("import together", re.compile(r"\bimport\s+together\b")),
    Rule("from together", re.compile(r"\bfrom\s+together\b")),
    Rule("Together client", re.compile(r"\bTogether\s*\(")),
    Rule("Together API URL", re.compile(r"api\.together\.xyz|api\.together\.ai")),
    Rule("import cohere", re.compile(r"\bimport\s+cohere\b")),
    Rule("from cohere", re.compile(r"\bfrom\s+cohere\b")),
    Rule("Cohere client", re.compile(r"\bcohere\.Client\s*\(")),
    Rule("Cohere API URL", re.compile(r"api\.cohere\.ai")),
    Rule("Replicate client", re.compile(r"\breplicate\.Client\s*\(")),
]


def is_ignored(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if rel in IGNORE_FILES or rel in ALLOWLISTED_PATTERN_FILES:
        return True
    if any(part in IGNORE_DIRS for part in rel.parts):
        return True
    return any(rel == prefix or prefix in rel.parents for prefix in IGNORE_PREFIXES)


def should_scan(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SCAN_SUFFIXES


def _line_is_documentation_only(path: Path, line: str) -> bool:
    if path.suffix.lower() != ".md":
        return False
    lower = line.lower()
    allowed_context = [
        "does not call",
        "no hosted llm",
        "no external llm",
        "manual baseline",
        "optional and manual",
        "not called",
        "without calling",
    ]
    return any(phrase in lower for phrase in allowed_context)


def scan_file(path: Path, root: Path) -> list[Violation]:
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8", errors="ignore")
    lower_text = text.lower()
    anthropic_context = "import anthropic" in lower_text or "from anthropic" in lower_text or "anthropic(" in lower_text
    violations: list[Violation] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if ALLOWLIST_COMMENT in line or _line_is_documentation_only(path, line):
            continue
        for rule in RULES:
            if path.suffix.lower() == ".md" and not rule.markdown_scan:
                continue
            if rule.requires_anthropic_context and not anthropic_context:
                continue
            if rule.pattern.search(line):
                violations.append(
                    Violation(
                        path=str(rel),
                        line=line_number,
                        pattern=rule.name,
                        text=line.strip()[:200],
                    )
                )
    return violations


def scan_root(root: Path) -> list[Violation]:
    root = root.resolve()
    violations: list[Violation] = []
    for path in root.rglob("*"):
        if is_ignored(path, root) or not should_scan(path):
            continue
        violations.extend(scan_file(path, root))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect hosted LLM API imports and call paths.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output for CI.")
    args = parser.parse_args()

    violations = scan_root(args.root)
    if args.json:
        print(json.dumps({"ok": not violations, "violations": [asdict(item) for item in violations]}, indent=2))
    elif violations:
        for item in violations:
            print(f"{item.path}:{item.line}: {item.pattern}: {item.text}")
    else:
        print("No hosted LLM API call paths detected.")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
