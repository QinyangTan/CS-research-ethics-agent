# repo-ethics-mcp

Local-first scanner, report builder, and stdio MCP server for CS research ethics pre-review.

Install from the repository root:

```bash
python3 -m pip install -e packages/repo-ethics-mcp
repo-ethics scan examples/reddit_nlp_project --json
repo-ethics report examples/reddit_nlp_project
repo-ethics mcp
```

This package does not call hosted LLM APIs. It provides deterministic tools and structured evidence for a user's own coding agent or reviewer.

From the repository root, `python3 scripts/check_no_hosted_llm_calls.py` checks source files for hosted LLM import or API-call paths while allowing benchmark fixtures and documentation-only mentions.
