# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_recommender_manipulation`
- Root path: `benchmarks/fixtures/case_recommender_manipulation`
- Languages: Markdown, Python
- Important files: README.md
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Project Evidence Summary

- Reviewed files included `README.md`, `src/recommend.py`.
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
- Evidence: README.md:1
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

## Evidence Table

| Finding | Evidence Type | Category | Evidence | Reason | Snippet |
|---|---|---|---|---|---|
| risk_3b31fd16ac | `risk_signal` | `ml_fairness_deployment_risk` | `README.md:1` | References recommender systems. | A recommender system ranks content to maximize engagement. Deployment boundaries and manipulation risks are not documented. Matched: recommender system |
| risk_fc19ee1aa0 | `missing_context` | `license_dataset_terms` | `.` | No code or dataset license documentation was detected. |  |

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

## Advisor / IRB Discussion Questions

- Who is affected by model outputs?
- Were subgroup errors evaluated?
- What deployment constraints and human review steps exist?
- Is there a model card documenting intended use, limitations, and fairness/bias evaluation?
- What license applies to the code?
- What terms apply to collected or derived data?
- Is redistribution permitted?
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
