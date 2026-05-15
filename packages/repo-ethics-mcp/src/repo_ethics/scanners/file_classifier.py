"""Path-based file classifier."""

from __future__ import annotations

from pathlib import Path


def classify_file(path: str | Path) -> str:
    rel = Path(path).as_posix().lower()
    name = Path(rel).name
    suffix = Path(rel).suffix.lower()

    if name in {"readme.md", "readme.rst", "readme.txt"}:
        return "project_description"
    if name in {"license", "license.md", "license.txt", "copying"}:
        return "license"
    if name in {"security.md"}:
        return "security_policy"
    if any(part in rel for part in ["ethics", "irb", "datasheet", "data_card", "datacard", "model_card", "modelcard"]):
        return "ethics_documentation"
    if rel.startswith("docs/") or "/docs/" in rel or suffix in {".md", ".rst"}:
        return "documentation"
    if suffix == ".ipynb":
        return "notebook"
    if suffix in {".json", ".jsonl", ".schema"} and ("schema" in name or "/data/" in rel):
        return "data_schema"
    if suffix in {".csv", ".tsv", ".parquet", ".sqlite", ".db"}:
        return "data_file"
    if name in {"requirements.txt", "pyproject.toml", "package.json", "package-lock.json", "pnpm-lock.yaml", "poetry.lock"}:
        return "dependency_manifest"
    if name in {"dockerfile", "compose.yaml", "docker-compose.yml"} or suffix in {".toml", ".yaml", ".yml", ".ini", ".cfg"}:
        return "config"
    if suffix in {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".c", ".cc", ".cpp", ".h", ".rb", ".php", ".swift", ".kt", ".r"}:
        return "source_code"
    return "unknown"

