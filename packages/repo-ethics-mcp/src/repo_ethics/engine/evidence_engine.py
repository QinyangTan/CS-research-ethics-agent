"""Safe repository reading and evidence helpers.

Repository contents are treated as untrusted data. This module never executes
target code and ensures symlinks remain within the requested root.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from repo_ethics.constants import BINARY_EXTENSIONS, DEFAULT_MAX_FILE_SIZE, SKIP_DIRS, SNIPPET_MAX_CHARS
from repo_ethics.schemas import Confidence, EvidenceItem


@dataclass(frozen=True)
class ScannedFile:
    path: Path
    rel_path: str
    size: int


def resolve_root(root_path: str | Path) -> Path:
    root = Path(root_path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root_path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root_path}")
    return root


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def load_gitignore(root: Path) -> PathSpec | None:
    gitignore = root / ".gitignore"
    if not gitignore.exists() or not gitignore.is_file():
        return None
    try:
        lines = gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    return PathSpec.from_lines(GitWildMatchPattern, lines)


def should_skip_dir(path: Path, root: Path) -> bool:
    name = path.name
    if name in SKIP_DIRS:
        return True
    if name.startswith(".") and name not in {".github"}:
        return True
    try:
        resolved = path.resolve()
    except OSError:
        return True
    return not is_relative_to(resolved, root)


def is_binary_path(path: Path) -> bool:
    return path.suffix.lower() in BINARY_EXTENSIONS


def is_likely_binary(path: Path) -> bool:
    if is_binary_path(path):
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(2048)
    except OSError:
        return True
    return b"\x00" in chunk


def iter_repo_files(root_path: str | Path, max_file_size: int = DEFAULT_MAX_FILE_SIZE) -> Iterable[ScannedFile]:
    root = resolve_root(root_path)
    spec = load_gitignore(root)
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        safe_dirs: list[str] = []
        for dirname in sorted(dirnames):
            candidate = current_path / dirname
            if should_skip_dir(candidate, root):
                continue
            rel_dir = candidate.relative_to(root).as_posix()
            if spec is not None and spec.match_file(rel_dir + "/"):
                continue
            safe_dirs.append(dirname)
        dirnames[:] = safe_dirs

        for filename in sorted(filenames):
            path = current_path / filename
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if not is_relative_to(resolved, root):
                continue
            rel_path = resolved.relative_to(root).as_posix()
            if spec is not None and spec.match_file(rel_path):
                continue
            if is_binary_path(resolved):
                continue
            try:
                size = resolved.stat().st_size
            except OSError:
                continue
            if size > max_file_size:
                continue
            if is_likely_binary(resolved):
                continue
            yield ScannedFile(path=resolved, rel_path=rel_path, size=size)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_snippet(snippet: str | None) -> str:
    if not snippet:
        return ""
    return " ".join(snippet.split())


def cap_snippet(text: str | None, max_chars: int = SNIPPET_MAX_CHARS) -> str | None:
    if text is None:
        return None
    normalized = text.strip().replace("\r\n", "\n")
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def stable_evidence_id(
    category: str,
    file_path: str,
    line_start: int | None,
    line_end: int | None,
    snippet: str | None,
) -> str:
    source = "|".join(
        [
            category,
            file_path,
            str(line_start or ""),
            str(line_end or ""),
            normalize_snippet(snippet),
        ]
    )
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def line_window_for_match(text: str, start: int, end: int, context_lines: int = 0) -> tuple[int, int, str]:
    line_starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            line_starts.append(index + 1)

    line_start = 1
    for index, offset in enumerate(line_starts, start=1):
        if offset <= start:
            line_start = index
        else:
            break

    line_end = line_start
    for index, offset in enumerate(line_starts, start=1):
        if offset < end:
            line_end = index
        else:
            break

    lines = text.splitlines()
    window_start = max(1, line_start - context_lines)
    window_end = min(len(lines), line_end + context_lines)
    snippet = "\n".join(lines[window_start - 1 : window_end])
    return line_start, line_end, cap_snippet(snippet) or ""


def is_negated_match(text: str, start: int, window: int = 80) -> bool:
    """Return True when a match appears inside a nearby negative statement."""

    prefix = text[max(0, start - window) : start].lower()
    return any(
        phrase in prefix
        for phrase in [
            "does not",
            "do not",
            "doesn't",
            "don't",
            "no ",
            "not ",
            "without ",
            "never ",
        ]
    )


def make_evidence(
    *,
    category: str,
    file_path: str,
    reason: str,
    confidence: Confidence = "medium",
    line_start: int | None = None,
    line_end: int | None = None,
    snippet: str | None = None,
    include_snippets: bool = True,
) -> EvidenceItem:
    shown_snippet = cap_snippet(snippet) if include_snippets else None
    evidence_id = stable_evidence_id(category, file_path, line_start, line_end, shown_snippet)
    return EvidenceItem(
        evidence_id=evidence_id,
        category=category,
        file_path=file_path,
        line_start=line_start,
        line_end=line_end,
        snippet=shown_snippet,
        reason=reason,
        confidence=confidence,
    )


def make_match_evidence(
    *,
    category: str,
    file_path: str,
    text: str,
    start: int,
    end: int,
    reason: str,
    confidence: Confidence = "medium",
    include_snippets: bool = True,
) -> EvidenceItem:
    line_start, line_end, snippet = line_window_for_match(text, start, end)
    matched_text = cap_snippet(text[start:end], max_chars=80) or ""
    if matched_text and matched_text not in snippet:
        snippet = f"{snippet}\nMatched: {matched_text}"
    elif matched_text:
        snippet = f"{snippet}\nMatched: {matched_text}"
    return make_evidence(
        category=category,
        file_path=file_path,
        reason=reason,
        confidence=confidence,
        line_start=line_start,
        line_end=line_end,
        snippet=snippet,
        include_snippets=include_snippets,
    )


def dedupe_evidence(items: Iterable[EvidenceItem]) -> list[EvidenceItem]:
    seen: set[str] = set()
    result: list[EvidenceItem] = []
    for item in items:
        if item.evidence_id in seen:
            continue
        seen.add(item.evidence_id)
        result.append(item)
    return sorted(result, key=lambda ev: (ev.file_path, ev.line_start or 0, ev.category, ev.evidence_id))
