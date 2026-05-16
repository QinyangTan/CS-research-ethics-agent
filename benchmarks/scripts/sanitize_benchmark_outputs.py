"""Sanitize local absolute repository paths in benchmark output artifacts."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIRS = [
    REPO_ROOT / "benchmarks" / "outputs" / "direct_codex",
    REPO_ROOT / "benchmarks" / "outputs" / "direct_codex_naive",
    REPO_ROOT / "benchmarks" / "outputs" / "repo_ethics",
]


@dataclass(frozen=True)
class SanitizeStats:
    files_scanned: int = 0
    files_changed: int = 0
    replacements: int = 0

    def add(self, *, changed: bool, replacements: int) -> "SanitizeStats":
        return SanitizeStats(
            files_scanned=self.files_scanned + 1,
            files_changed=self.files_changed + int(changed),
            replacements=self.replacements + replacements,
        )


def _repo_prefixes() -> list[str]:
    raw = str(REPO_ROOT)
    return [raw, raw.replace(" ", "%20")]


def sanitize_text(text: str) -> tuple[str, int]:
    sanitized = text
    replacements = 0
    for prefix in _repo_prefixes():
        count = sanitized.count(prefix)
        if count:
            sanitized = sanitized.replace(prefix + "/", "")
            sanitized = sanitized.replace(prefix, ".")
            replacements += count
    return sanitized, replacements


def iter_output_files(directories: list[Path]) -> list[Path]:
    files: list[Path] = []
    for directory in directories:
        if not directory.exists():
            continue
        files.extend(sorted(path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json"}))
    return files


def sanitize_files(directories: list[Path], *, dry_run: bool = False, check: bool = False) -> SanitizeStats:
    stats = SanitizeStats()
    remaining: list[Path] = []
    for path in iter_output_files(directories):
        text = path.read_text(encoding="utf-8", errors="ignore")
        sanitized, replacements = sanitize_text(text)
        changed = sanitized != text
        if check and any(prefix in text for prefix in _repo_prefixes()):
            remaining.append(path)
        if changed and not dry_run and not check:
            path.write_text(sanitized, encoding="utf-8")
        stats = stats.add(changed=changed, replacements=replacements)

    if check and remaining:
        for path in remaining:
            print(f"Unsanitized repo-root path remains in {path.relative_to(REPO_ROOT)}")
        raise SystemExit(1)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove local repo-root absolute paths from benchmark output artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Report replacements without modifying files.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if any local repo-root paths remain.")
    parser.add_argument(
        "--dir",
        action="append",
        type=Path,
        dest="dirs",
        help="Output directory to sanitize. May be repeated. Defaults to benchmark output Markdown directories.",
    )
    args = parser.parse_args()

    directories = [path if path.is_absolute() else REPO_ROOT / path for path in (args.dirs or DEFAULT_DIRS)]
    stats = sanitize_files(directories, dry_run=args.dry_run, check=args.check)
    mode = "checked" if args.check else "dry-run" if args.dry_run else "sanitized"
    print(
        f"Benchmark outputs {mode}: files scanned={stats.files_scanned}, "
        f"files changed={stats.files_changed}, replacements={stats.replacements}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
