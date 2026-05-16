# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_scraping_with_controls`
- Root path: `benchmarks/fixtures/case_scraping_with_controls`
- Languages: Markdown, Python
- Important files: README.md, docs/data_policy.md
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `docs/data_policy.md`, `src/main.py`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

No findings in this section based on available repository evidence.

## Potential Risks

### Possible privacy and consent risk from collected platform/user data
- Risk ID: `risk_661f2d7c4c`
- Category: `consent_reasonable_expectation`
- Status: `potential`
- Severity: `high`
- Confidence: `high`
- Why it matters: Evidence suggests collected data may involve people or communities where consent, notice, or reasonable expectations need review.
- Evidence: src/main.py:2, docs/data_policy.md:1
- Missing context: Whether the data subjects reasonably expected this collection and analysis.; Whether platform terms, notices, or consent expectations were reviewed.

### Web scraping governance and platform terms need review
- Risk ID: `risk_719682d322`
- Category: `web_scraping_platform_governance`
- Status: `potential`
- Severity: `medium`
- Confidence: `high`
- Why it matters: The project appears to collect data from websites, APIs, or platforms where terms, robots.txt, rate limits, and community expectations matter.
- Evidence: src/main.py:2, README/docs
- Missing context: Platform terms, robots.txt handling, rate limits, and collection dates.

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
| risk_661f2d7c4c | `risk_signal` | `web_scraping_platform_governance` | `src/main.py:2` | Uses Python requests for HTTP collection. | response = requests.get('https://example.test/posts', timeout=5) Matched: requests.get( |
| risk_661f2d7c4c | `risk_signal` | `privacy_identifiability` | `docs/data_policy.md:1` | References usernames or handles. | Raw usernames are removed before analysis. Matched: usernames |
| risk_719682d322 | `risk_signal` | `web_scraping_platform_governance` | `src/main.py:2` | Uses Python requests for HTTP collection. | response = requests.get('https://example.test/posts', timeout=5) Matched: requests.get( |
| risk_719682d322 | `missing_context` | `web_scraping_platform_governance` | `README/docs` | Scraping or API collection was detected, but README/docs do not positively document: data policy. |  |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: consent/reasonable expectation. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

- `README.md:1`: `dataset_release_reidentification` - Documentation includes retention/deletion policy.
- `README.md:1`: `missing_ethics_documentation` - Documentation includes robots.txt or rate limiting.
- `README.md:1`: `missing_ethics_documentation` - Documentation includes platform terms.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes platform terms guidance.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes rate limits guidance.
- `README.md:1`: `web_scraping_platform_governance` - Documentation includes robots.txt guidance.
- `docs/data_policy.md:1`: `missing_ethics_documentation` - Documentation includes collection method/dates.

## Category-Specific Review Focus

- `consent_reasonable_expectation`: confirm public/private boundaries, notice or consent assumptions, participant expectations, vulnerable communities, and opt-out or takedown paths.
- `web_scraping_platform_governance`: confirm platform/API terms, robots.txt where relevant, rate limits, deletion/edit handling, redistribution limits, and user-content policy.
- `missing_ethics_documentation`: confirm project purpose, data provenance, consent or notice assumptions, intended release/deployment, limitations, and documented controls.
- `dataset_release_reidentification`: confirm data card or datasheet coverage, release tiers, raw versus aggregate release, controlled access, license/terms, provenance, and re-identification risk.

## Recommended Mitigations

- Document the collection context, consent or notice assumptions, and reasonable-expectation analysis.
- Avoid collecting private, access-controlled, or sensitive-community data without review.
- Minimize retained raw content and identifiers.
- Check platform terms.
- Check robots.txt where applicable.
- Add rate limiting.
- Document deletion or edit handling for collected platform content.
- Document redistribution limits for raw posts, comments, or metadata.
- Avoid collecting private or access-controlled data.
- Avoid collecting sensitive communities without review.
- Document collection method and dates.
- Consider whether consent or notice is needed.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Would the people represented reasonably expect this collection and analysis?
- Was consent or notice provided?
- Are private or sensitive communities involved?
- Which platform terms, API policies, or robots.txt files apply?
- What rate limits and collection dates were used?
- Is any private or access-controlled data collected?
- How are deleted, edited, or restricted platform records handled?
- Can collected platform content or metadata be redistributed?
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
