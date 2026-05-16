# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_iot_sensor_location`
- Root path: `benchmarks/fixtures/case_iot_sensor_location`
- Languages: JSON, Markdown
- Important files: README.md, data/schema.json
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `data/schema.json`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

No findings in this section based on available repository evidence.

## Potential Risks

### Possible re-identification risk if dataset is released
- Risk ID: `risk_33c2faca73`
- Category: `dataset_release_reidentification`
- Status: `potential`
- Severity: `high`
- Confidence: `medium`
- Why it matters: The repository contains data or release signals that may require review for re-identification, retention, and sharing risk.
- Evidence: README.md:1, README.md:1, README.md:1, data/schema.json:1, data/schema.json:1, data/schema.json:1, data/schema.json, .
- Missing context: Whether raw records will be shared, retained, aggregated, or de-identified.

## Unknowns and Required Clarifications

### Missing ethics, data handling, or release documentation
- Risk ID: `risk_8877616584`
- Category: `missing_ethics_documentation`
- Status: `unknown`
- Severity: `medium`
- Confidence: `medium`
- Why it matters: Documentation does not appear to explain key ethics, privacy, safety, release, or limitation topics.
- Evidence: README/docs
- Missing context: LICENSE; ethics/privacy/data handling documentation

## Evidence Table

| Finding | Evidence Type | Category | Evidence | Reason | Snippet |
|---|---|---|---|---|---|
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `README.md:1` | References location or GPS data. | Citizen science sensors upload GPS location and exact timestamps. Matched: GPS |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `README.md:1` | References location or GPS data. | Citizen science sensors upload GPS location and exact timestamps. Matched: location |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `README.md:1` | References exact timestamps. | Citizen science sensors upload GPS location and exact timestamps. Matched: timestamps |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `data/schema.json:1` | References exact timestamps. | {"gps": "latlon", "timestamp": "datetime", "device_id": "string"} Matched: timestamp |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `data/schema.json:1` | References exact timestamps. | {"gps": "latlon", "timestamp": "datetime", "device_id": "string"} Matched: datetime |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `data/schema.json:1` | References location or GPS data. | {"gps": "latlon", "timestamp": "datetime", "device_id": "string"} Matched: gps |
| risk_33c2faca73 | `risk_signal` | `dataset_release_reidentification` | `data/schema.json` | Repository contains a dataset-like file by extension; content was not read. Release, retention, and de-identification review may be needed if it contains research data. |  |
| risk_33c2faca73 | `missing_context` | `dataset_release_reidentification` | `.` | Dataset files or release language were detected, but the following data-governance context may need clarification: retention/deletion policy, provenance/access policy. |  |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: anonymization/de-identification, consent/reasonable expectation, data access controls, data card/datasheet, data retention/deletion, privacy, release policy. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

No positive controls were detected from repository evidence.

## Category-Specific Review Focus

- `dataset_release_reidentification`: review data card or datasheet, release tiers, raw data versus aggregate release, controlled access, and license or source terms.
- `missing_ethics_documentation`: review project purpose, data handling, release boundaries, advisor or review-body discussion, and documentation owner.
- `privacy_identifiability`: review data minimization, de-identification or anonymization, retention period, access control, and re-identification risk.

## Recommended Mitigations

- Create a data card or datasheet.
- State whether raw records, derived features, or only aggregate statistics will be released.
- Define a release policy for public, restricted, or no-release data.
- Avoid public release of raw identifiable records.
- Aggregate, redact, or perturb fields that could identify people.
- Define retention and deletion policy.
- Document anonymization limits.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Will raw data, derived data, or only aggregate statistics be released?
- What fields could enable re-identification?
- Is there a data card or datasheet?
- What release, retention, deletion, and access-control policy applies?
- What data is collected and why?
- What release limits apply?
- What mitigations are already in place but not documented?
- Project purpose, population, data provenance, consent/notice process, and intended release/deployment should be clarified when not documented.

## Safe Release Checklist

- [ ] Confirm the project purpose, affected populations, and deployment context are documented.
- [ ] Review whether data collection aligns with reasonable expectations and platform terms.
- [ ] Remove, aggregate, or protect direct identifiers and sensitive quasi-identifiers.
- [ ] Define data retention, deletion, access control, and sharing limits.
- [ ] Avoid public release of raw sensitive or identifiable records.
- [ ] Document known limitations, misuse risks, and appropriate use boundaries.
- [ ] Prepare responsible disclosure steps for security-sensitive work.
- [ ] Rotate any exposed credentials and keep secrets out of reports and commits.

## Appendix: Scanner Limitations

- Static scanning can miss risks that depend on project intent, population, deployment setting, or data provenance.
- Pattern matching can produce false positives and false negatives.
- Repository text is treated as untrusted evidence, including README files and comments.
- This report should support, not replace, advisor or appropriate review-body discussion.
