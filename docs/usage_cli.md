# CLI Usage

## Scan

```bash
repo-ethics scan PATH
repo-ethics scan PATH --json
repo-ethics scan PATH --json --output scan.json
repo-ethics scan PATH --max-file-size 524288 --no-include-snippets
```

`scan` returns deterministic evidence and project profile data. Snippet suppression keeps file path, line range, reason, and confidence.

## Report

```bash
repo-ethics report PATH
repo-ethics report PATH --format json
repo-ethics report PATH --output ethics_report.md
repo-ethics report PATH --fail-on-critical
```

Exit codes:

- `0`: completed, no critical findings or `--fail-on-critical` was not triggered.
- `1`: scanner/runtime/configuration error.
- `2`: critical findings detected with `--fail-on-critical`.

## Taxonomy And Schema

```bash
repo-ethics taxonomy
repo-ethics schema
repo-ethics schema --output docs/report_schema.json
```

