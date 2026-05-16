# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_surveillance_tracking`
- Root path: `benchmarks/fixtures/case_surveillance_tracking`
- Languages: Markdown, Python
- Important files: README.md
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `src/main.py`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

### Biometric identification or surveillance risk
- Risk ID: `risk_e1fc61af82`
- Category: `surveillance_tracking`
- Status: `confirmed`
- Severity: `high`
- Confidence: `high`
- Why it matters: The project may monitor, identify, or track people across spaces, cameras, or institutional contexts.
- Evidence: README.md:1
- Missing context: Consent process, data retention, access controls, deployment setting, and affected population.

## Potential Risks

No findings in this section based on available repository evidence.

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
| risk_e1fc61af82 | `risk_signal` | `surveillance_tracking` | `README.md:1` | References person re-identification or cross-camera tracking. | Tracks people across cameras for a multi-camera tracking demo. Consent and deployment limits are not documented. Matched: multi-camera tracking |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: bias/performance limitations, consent/reasonable expectation, data access controls, data retention/deletion, deployment limitations, privacy. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

No positive controls were detected from repository evidence.

## Category-Specific Review Focus

- `surveillance_tracking`: confirm tracking scope, notice/consent, bystander risk, retention, deployment limits, and aggregation/anonymization.
- `missing_ethics_documentation`: confirm project purpose, data provenance, consent or notice assumptions, intended release/deployment, limitations, and documented controls.

## Recommended Mitigations

- Limit tracking to the narrowest necessary purpose.
- Document tracking scope, notice, consent or opt-out, access control, and retention.
- Address bystander and non-participant risks.
- Define deployment limits and prohibited uses.
- Review deployment context with an advisor or appropriate review body.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Who is tracked and in what setting?
- Can affected people opt out?
- Who can access tracking records?
- What bystander, non-participant, or deployment risks need review?
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
