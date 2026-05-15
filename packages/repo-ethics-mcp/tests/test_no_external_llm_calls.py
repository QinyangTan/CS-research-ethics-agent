from pathlib import Path


def test_no_hosted_llm_api_imports_or_calls() -> None:
    root = Path(__file__).resolve().parents[3]
    search_roots = [root / "packages" / "repo-ethics-mcp" / "src", root / "eval", root / "examples"]
    forbidden = [
        "import openai",
        "from openai",
        "import anthropic",
        "from anthropic",
        "api.openai",
        "api.anthropic",
        "chatgpt",
        "claude",
    ]
    hits: list[str] = []
    for search_root in search_roots:
        for path in search_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".py", ".md", ".json", ".toml", ".txt"}:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
                for phrase in forbidden:
                    if phrase in text:
                        hits.append(f"{path.relative_to(root)}: {phrase}")
    assert hits == []

