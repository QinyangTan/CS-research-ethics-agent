"""Typer CLI for repo-ethics."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Literal

import typer
from rich.console import Console
from rich.table import Table

from repo_ethics.constants import DEFAULT_MAX_FILE_SIZE
from repo_ethics.engine.report_builder import build_report, report_to_json, report_to_markdown
from repo_ethics.engine.scan_runner import run_scan
from repo_ethics.mcp_server import run_mcp_server
from repo_ethics.schemas import EthicsReviewReport


app = typer.Typer(help="Local-first CS research ethics review scanner.")
console = Console()

EXIT_RUNTIME_ERROR = 1
EXIT_CRITICAL_FINDINGS = 2


def _load_taxonomy() -> dict:
    with resources.files("repo_ethics.kb").joinpath("taxonomy.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_or_print(content: str, output: Path | None = None) -> None:
    if output is not None:
        output.write_text(content, encoding="utf-8")
        console.print(f"Wrote {output}")
    else:
        typer.echo(content)


def _critical_count(report: EthicsReviewReport) -> int:
    return sum(1 for finding in report.findings if finding.severity == "critical")


@app.command()
def scan(
    path: Path,
    json_output: bool = typer.Option(False, "--json", help="Print ScanResult as JSON."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Write JSON scan output to a file."),
    max_file_size: int = typer.Option(DEFAULT_MAX_FILE_SIZE, "--max-file-size", help="Maximum bytes scanned per file."),
    include_snippets: bool = typer.Option(True, "--include-snippets/--no-include-snippets", help="Include evidence snippets."),
    fail_on_critical: bool = typer.Option(False, "--fail-on-critical", help="Exit 2 if critical findings are detected."),
) -> None:
    """Run scanners and print a summary or JSON evidence."""

    try:
        result = run_scan(path, max_file_size=max_file_size, include_snippets=include_snippets)
        report = build_report(result)
    except Exception as exc:  # pragma: no cover - CLI guard
        console.print(f"[red]Scanner error:[/red] {exc}")
        raise typer.Exit(EXIT_RUNTIME_ERROR) from exc

    if json_output or output is not None:
        content = json.dumps(result.model_dump(), indent=2, sort_keys=True)
        _write_or_print(content, output)
    else:
        table = Table(title="Repo Ethics Scan Summary")
        table.add_column("Category")
        table.add_column("Evidence Count", justify="right")
        counts: dict[str, int] = {}
        for item in result.evidence:
            counts[item.category] = counts.get(item.category, 0) + 1
        for category in sorted(counts):
            table.add_row(category, str(counts[category]))
        if not counts:
            table.add_row("none", "0")
        console.print(table)
        console.print(f"Project: {result.project_profile.project_name}")
        console.print(f"Warnings: {len(result.warnings)}")

    if fail_on_critical and _critical_count(report):
        raise typer.Exit(EXIT_CRITICAL_FINDINGS)


@app.command()
def report(
    path: Path,
    format: Literal["markdown", "json"] = typer.Option("markdown", "--format", help="Report format."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Write report to a file."),
    include_low_confidence: bool = typer.Option(True, "--include-low-confidence/--no-include-low-confidence", help="Include low-confidence evidence."),
    fail_on_critical: bool = typer.Option(False, "--fail-on-critical", help="Exit 2 if critical findings are detected."),
    max_file_size: int = typer.Option(DEFAULT_MAX_FILE_SIZE, "--max-file-size", help="Maximum bytes scanned per file."),
) -> None:
    """Run scan, map risks, and generate an ethics pre-review report."""

    try:
        result = run_scan(path, max_file_size=max_file_size, include_snippets=True)
        review = build_report(result, include_low_confidence=include_low_confidence)
        content = report_to_json(review) if format == "json" else report_to_markdown(review)
    except Exception as exc:  # pragma: no cover - CLI guard
        console.print(f"[red]Report error:[/red] {exc}")
        raise typer.Exit(EXIT_RUNTIME_ERROR) from exc

    _write_or_print(content, output)
    if fail_on_critical and _critical_count(review):
        raise typer.Exit(EXIT_CRITICAL_FINDINGS)


@app.command()
def mcp() -> None:
    """Start the MCP server over stdio."""

    run_mcp_server()


@app.command()
def taxonomy() -> None:
    """Print available risk categories."""

    data = _load_taxonomy()
    table = Table(title="Supported CS Ethics Risk Categories")
    table.add_column("ID")
    table.add_column("Name")
    for category_id, category in sorted(data["categories"].items()):
        table.add_row(category_id, category["name"])
    console.print(table)


@app.command()
def schema(output: Path | None = typer.Option(None, "--output", "-o", help="Write JSON Schema to a file.")) -> None:
    """Print the JSON Schema for EthicsReviewReport."""

    content = json.dumps(EthicsReviewReport.model_json_schema(), indent=2, sort_keys=True)
    _write_or_print(content, output)


if __name__ == "__main__":
    app()

