"""Stdio MCP server exposing local repo ethics tools."""

from __future__ import annotations

import json
from importlib import resources
from typing import Literal

from repo_ethics.engine.report_builder import build_report, report_to_json, report_to_markdown
from repo_ethics.engine.scan_runner import run_scan
from repo_ethics.scanners.prompt_injection_scanner import scan as scan_prompt_injection_only
from repo_ethics.scanners.secret_scanner import scan as scan_secrets_only


def _load_json_resource(name: str) -> dict:
    with resources.files("repo_ethics.kb").joinpath(name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_text_resource(package: str, name: str) -> str:
    return resources.files(package).joinpath(name).read_text(encoding="utf-8")


def build_mcp_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - depends on optional runtime
        raise RuntimeError("The MCP Python SDK is required. Install package dependencies first.") from exc

    server = FastMCP("repo-ethics")

    @server.tool()
    def scan_repo(root_path: str, include_snippets: bool = True, max_file_size: int = 524_288) -> dict:
        """Scan a repository locally and return structured evidence."""

        return run_scan(root_path, max_file_size=max_file_size, include_snippets=include_snippets).model_dump()

    @server.tool()
    def generate_ethics_report(root_path: str, format: Literal["json", "markdown"] = "markdown") -> str:
        """Generate a JSON or Markdown ethics pre-review report."""

        report = build_report(run_scan(root_path))
        return report_to_json(report) if format == "json" else report_to_markdown(report)

    @server.tool()
    def get_ethics_taxonomy(category: str | None = None) -> dict:
        """Return the full taxonomy or one category."""

        taxonomy = _load_json_resource("taxonomy.json")
        if category is None:
            return taxonomy
        return taxonomy["categories"].get(category, {})

    @server.tool()
    def get_mitigation_suggestions(category: str) -> dict:
        """Return mitigation rules and follow-up questions for a category."""

        mitigations = _load_json_resource("mitigation_rules.json")
        questions = _load_json_resource("followup_questions.json")
        return {
            "category": category,
            "mitigations": mitigations.get(category, []),
            "followup_questions": questions.get(category, []),
        }

    @server.tool()
    def get_report_template() -> str:
        """Return the Markdown report template."""

        return _load_text_resource("repo_ethics.templates", "ethics_report.md")

    @server.tool()
    def list_supported_risk_categories() -> list[dict[str, str]]:
        """List supported category IDs and names."""

        taxonomy = _load_json_resource("taxonomy.json")
        return [
            {"id": category_id, "name": category["name"]}
            for category_id, category in sorted(taxonomy["categories"].items())
        ]

    @server.tool()
    def scan_prompt_injection(root_path: str) -> list[dict]:
        """Scan only for prompt-injection attempts."""

        return [item.model_dump() for item in scan_prompt_injection_only(root_path)]

    @server.tool()
    def scan_secrets(root_path: str) -> list[dict]:
        """Scan only for masked secret exposure evidence."""

        return [item.model_dump() for item in scan_secrets_only(root_path)]

    return server


def run_mcp_server() -> None:
    server = build_mcp_server()
    server.run()

