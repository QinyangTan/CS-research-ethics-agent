# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_scraping_positive_governance`
- Root path: `benchmarks/fixtures/case_scraping_positive_governance`
- Languages: Markdown, Python
- Important files: README.md, docs/governance.md
- Possible human data: False
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `docs/governance.md`, `src/main.py`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

No findings in this section based on available repository evidence.

## Potential Risks

### Web scraping governance and platform terms need review
- Risk ID: `risk_719682d322`
- Category: `web_scraping_platform_governance`
- Status: `potential`
- Severity: `medium`
- Confidence: `high`
- Why it matters: The project appears to collect data from websites, APIs, or platforms where terms, robots.txt, rate limits, and community expectations matter.
- Evidence: src/main.py:2
- Missing context: Platform terms, robots.txt handling, rate limits, and collection dates.

## Unknowns and Required Clarifications

### License or dataset redistribution terms are unclear
- Risk ID: `risk_fc19ee1aa0`
- Category: `license_dataset_terms`
- Status: `unknown`
- Severity: `low`
- Confidence: `medium`
- Why it matters: Repository evidence leaves code, data, or platform redistribution terms unclear.
- Evidence: .
- Missing context: Code license, dataset source terms, and redistribution permissions.

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
| risk_719682d322 | `risk_signal` | `web_scraping_platform_governance` | `src/main.py:2` | Uses Python requests for HTTP collection. | requests.get('https://example.test') Matched: requests.get( |
| risk_fc19ee1aa0 | `missing_context` | `license_dataset_terms` | `.` | No code or dataset license documentation was detected. |  |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: consent/reasonable expectation. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

- `README.md:1`: `missing_ethics_documentation` - Documentation includes platform terms.
- `README.md:1`: `missing_ethics_documentation` - Documentation includes robots.txt or rate limiting.
- `README.md:1`: `missing_ethics_documentation` - Documentation includes collection method/dates.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes rate limits guidance.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes data policy guidance.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes robots.txt guidance.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes platform terms guidance.
- `docs/governance.md:1`: `web_scraping_platform_governance` - Documentation includes platform terms guidance.
- `docs/governance.md:1`: `web_scraping_platform_governance` - Documentation includes robots.txt guidance.
- `docs/governance.md:1`: `web_scraping_platform_governance` - Documentation includes rate limits guidance.
- `docs/governance.md:1`: `web_scraping_platform_governance` - Documentation includes rate limits guidance.

## Recommended Mitigations

- Check platform terms.
- Check robots.txt where applicable.
- Add rate limiting.
- Document deletion or edit handling for collected platform content.
- Document redistribution limits for raw posts, comments, or metadata.
- Avoid collecting private or access-controlled data.
- Avoid collecting sensitive communities without review.
- Document collection method and dates.
- Consider whether consent or notice is needed.
- Add a clear code license.
- Document dataset source terms and redistribution limits.
- Avoid redistributing data unless terms permit it.
- Track third-party license obligations.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Which platform terms, API policies, or robots.txt files apply?
- What rate limits and collection dates were used?
- Is any private or access-controlled data collected?
- How are deleted, edited, or restricted platform records handled?
- Can collected platform content or metadata be redistributed?
- What license applies to the code?
- What terms apply to collected or derived data?
- Is redistribution permitted?
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
