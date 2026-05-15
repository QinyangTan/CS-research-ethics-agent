# Installation

Install the local package from the repository root:

```bash
python3 -m pip install -e packages/repo-ethics-mcp
```

Try the CLI:

```bash
repo-ethics scan .
repo-ethics report . --output ethics_report.md
repo-ethics mcp
```

The package declares constrained dependency ranges for Typer, Rich, Pydantic, the MCP Python SDK, pathspec, PyYAML, and pytest.

