# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_ml_admissions`
- Root path: `benchmarks/fixtures/case_ml_admissions`
- Languages: Markdown, Python
- Important files: README.md
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `src/model.py`.
- Absence of detected high-risk categories is not a final ethics or safety determination.

## Detected Research Activities

- Activities: Not detected from repository text
- Data sources: Not detected from repository text

## Confirmed Findings

No findings in this section based on available repository evidence.

## Potential Risks

### Fairness, profiling, or deployment harm risk
- Risk ID: `risk_3b31fd16ac`
- Category: `ml_fairness_deployment_risk`
- Status: `potential`
- Severity: `medium`
- Confidence: `high`
- Why it matters: ML systems may classify, rank, profile, recommend to, or otherwise affect people.
- Evidence: README.md:1, src/model.py:1, src/model.py:2, src/model.py:2, src/model.py:2, src/model.py:2
- Missing context: Intended deployment context, evaluation by subgroup, and whether outputs affect people.

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
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `README.md:1` | References high-impact decision contexts. | Predicts admissions decisions from student profiles. Fairness, bias evaluation, and deployment boundaries are not documented. Matched: admissions |
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `src/model.py:1` | Uses machine learning libraries. | import sklearn Matched: sklearn |
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `src/model.py:2` | References high-impact decision contexts. | # admissions grading model over student_id and demographic features Matched: grading |
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `src/model.py:2` | References high-impact decision contexts. | # admissions grading model over student_id and demographic features Matched: admissions |
| risk_3b31fd16ac | `risk_signal` | `privacy_identifiability` | `src/model.py:2` | References student records or identifiers. | # admissions grading model over student_id and demographic features Matched: student_id |
| risk_3b31fd16ac | `risk_signal` | `privacy_identifiability` | `src/model.py:2` | References demographic or sensitive attributes. | # admissions grading model over student_id and demographic features Matched: demographic |
| risk_fc19ee1aa0 | `missing_context` | `license_dataset_terms` | `.` | No code or dataset license documentation was detected. |  |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: anonymization/de-identification, consent/reasonable expectation, data access controls, data retention/deletion, deployment boundaries, fairness/bias evaluation, model card or limitations, privacy. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

No positive controls were detected from repository evidence.

## Recommended Mitigations

- Document intended use and non-use.
- Create or update a model card.
- Evaluate subgroup performance where appropriate.
- Document fairness and bias evaluation methods.
- Document uncertainty and failure modes.
- Set deployment boundaries and human-review expectations.
- Add a clear code license.
- Document dataset source terms and redistribution limits.
- Avoid redistributing data unless terms permit it.
- Track third-party license obligations.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Who is affected by model outputs?
- Were subgroup errors evaluated?
- What deployment constraints and human review steps exist?
- Is there a model card documenting intended use, limitations, and fairness/bias evaluation?
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
