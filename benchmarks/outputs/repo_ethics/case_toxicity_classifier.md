# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_toxicity_classifier`
- Root path: `benchmarks/fixtures/case_toxicity_classifier`
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
- Confidence: `medium`
- Why it matters: ML systems may classify, rank, profile, recommend to, or otherwise affect people.
- Evidence: README.md:1, src/model.py:1
- Missing context: Intended deployment context, evaluation by subgroup, and whether outputs affect people.

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
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `README.md:1` | References toxicity or emotion classification. | Builds a toxicity detection model for user comments. Model card and bias evaluation are not documented. Matched: toxicity detection |
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `src/model.py:1` | Uses machine learning libraries. | from transformers import AutoModel Matched: transformers |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: deployment boundaries, fairness/bias evaluation, model card or limitations. Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

No positive controls were detected from repository evidence.

## Category-Specific Review Focus

- `ml_fairness_deployment_risk`: confirm model card coverage, intended use, limitations, bias/fairness evaluation, affected groups, and deployment monitoring.
- `missing_ethics_documentation`: confirm project purpose, data provenance, consent or notice assumptions, intended release/deployment, limitations, and documented controls.

## Recommended Mitigations

- Document intended use and non-use.
- Create or update a model card.
- Evaluate subgroup performance where appropriate.
- Document fairness and bias evaluation methods.
- Document uncertainty and failure modes.
- Set deployment boundaries and human-review expectations.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Who is affected by model outputs?
- Were subgroup errors evaluated?
- What deployment constraints and human review steps exist?
- Is there a model card documenting intended use, limitations, and fairness/bias evaluation?
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
