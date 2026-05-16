# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_dataset_with_data_card`
- Root path: `benchmarks/fixtures/case_dataset_with_data_card`
- Languages: Markdown
- Important files: README.md, data/samples.csv, docs/data_card.md
- Possible human data: False
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `data/samples.csv`, `docs/data_card.md`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

No findings in this section based on available repository evidence.

## Potential Risks

### Dataset release and retention details need review
- Risk ID: `risk_ee234ffc02`
- Category: `dataset_release_reidentification`
- Status: `potential`
- Severity: `medium`
- Confidence: `medium`
- Why it matters: The repository contains data or release signals that may require review for re-identification, retention, and sharing risk.
- Evidence: data/samples.csv
- Missing context: Dataset sharing scope, retention period, and anonymization limits.

## Unknowns and Required Clarifications

No findings in this section based on available repository evidence.

## Evidence Table

| Finding | Evidence Type | Category | Evidence | Reason | Snippet |
|---|---|---|---|---|---|
| risk_ee234ffc02 | `risk_signal` | `dataset_release_reidentification` | `data/samples.csv` | Repository contains a dataset-like file by extension; content was not read. Release, retention, and de-identification review may be needed if it contains research data. |  |

## Positive Controls Detected

- `docs/data_card.md`: `missing_ethics_documentation` - Repository includes dedicated ethics, privacy, data-card, or model-card documentation.
- `docs/data_card.md:1`: `dataset_release_reidentification` - Documentation includes retention/deletion policy.
- `docs/data_card.md:1`: `dataset_release_reidentification` - Documentation includes data card/datasheet.
- `docs/data_card.md:1`: `dataset_release_reidentification` - Documentation includes retention/deletion policy.

## Category-Specific Review Focus

- `dataset_release_reidentification`: confirm data card or datasheet coverage, release tiers, raw versus aggregate release, controlled access, license/terms, provenance, and re-identification risk.
- `missing_ethics_documentation`: confirm project purpose, data provenance, consent or notice assumptions, intended release/deployment, limitations, and documented controls.

## Recommended Mitigations

- Create a data card or datasheet.
- State whether raw records, derived features, or only aggregate statistics will be released.
- Define a release policy for public, restricted, or no-release data.
- Avoid public release of raw identifiable records.
- Aggregate, redact, or perturb fields that could identify people.
- Define retention and deletion policy.
- Document anonymization limits.

## Advisor / IRB Discussion Questions

- Will raw data, derived data, or only aggregate statistics be released?
- What fields could enable re-identification?
- Is there a data card or datasheet?
- What release, retention, deletion, and access-control policy applies?
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
