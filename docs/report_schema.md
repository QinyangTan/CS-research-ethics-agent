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

Evidence items include `evidence_type`:

- `risk_signal`: direct evidence that may indicate an ethics risk.
- `missing_context`: absent, unclear, negated, TBD, or undocumented context.
- `positive_control`: helpful safeguards or documentation such as a license, data card, security policy, documented rate limits, ethics note, or responsible disclosure policy.

`ScanResult.evidence` contains all evidence types. `EthicsReviewReport.findings` contains risk and unknown findings, while `EthicsReviewReport.positive_controls` lists helpful controls separately for balanced human-readable reports.
