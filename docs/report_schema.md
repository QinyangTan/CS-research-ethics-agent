# Report Schema

The canonical schema is defined with Pydantic models in `repo_ethics.schemas`.

Generate JSON Schema:

```bash
repo-ethics schema --output docs/report_schema.json
```

Primary models:

- `EvidenceItem`
- `ProjectProfile`
- `RiskFinding`
- `EthicsReviewReport`
- `ScanResult`

Every confirmed or potential finding includes at least one evidence item. Unknown findings may represent concrete absence evidence or missing context.

