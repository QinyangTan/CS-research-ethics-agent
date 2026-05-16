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

`ProjectProfile.reviewed_files` lists representative files considered by the static scanner or metadata walker. Reports cap this list and use it for evidence grounding; it is not a claim that unlisted files were irrelevant or that the project has no risks.

Negation handling is target-aware for common scanner terms. For example, "not a vulnerability scanner" suppresses the vulnerability-scanner match, while "not a toy and it is a vulnerability scanner" remains a positive signal. Missing-context wording such as "not documented" or "TBD" is still treated as missing context rather than documentation coverage.
