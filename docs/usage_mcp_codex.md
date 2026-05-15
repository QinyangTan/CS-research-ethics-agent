# MCP Usage With Codex

Run the local stdio MCP server:

```bash
repo-ethics mcp
```

MCP client configuration varies by agent and version. A typical local configuration maps a server name to the command above:

```json
{
  "mcpServers": {
    "repo-ethics": {
      "command": "repo-ethics",
      "args": ["mcp"]
    }
  }
}
```

Adapt this example to your Codex MCP configuration format. Once connected, ask the agent to use `scan_repo`, `generate_ethics_report`, `get_ethics_taxonomy`, and `get_mitigation_suggestions` before writing a report.

