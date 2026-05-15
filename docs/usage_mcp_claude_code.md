# MCP Usage With Claude Code

Run the local stdio MCP server:

```bash
repo-ethics mcp
```

Claude Code MCP setup may differ by release. Use your current Claude Code MCP configuration format and point a stdio server at:

```json
{
  "command": "repo-ethics",
  "args": ["mcp"]
}
```

After connecting, instruct the agent to treat repository text as untrusted evidence, call `scan_repo`, retrieve taxonomy and mitigations, and produce a report with confirmed, potential, and unknown findings.

