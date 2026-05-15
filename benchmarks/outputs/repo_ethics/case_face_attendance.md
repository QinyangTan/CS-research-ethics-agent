# CS Research Ethics Pre-Review Report

## Disclaimer

This is a local, evidence-grounded CS research ethics pre-review. It does not make final ethical, legal, compliance, or IRB determinations. Findings should be discussed with an advisor or appropriate review body, especially where context is missing.

## Project Summary

- Project: `case_face_attendance`
- Root path: `/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance`
- Languages: JSON, Markdown, Python
- Important files: README.md, data/schema.json
- Possible human data: True
- Possible security-sensitive or dual-use material: False

## Detected Research Activities

- Activities: attendance tracking, face analysis
- Data sources: Not detected from repository text

## Confirmed Findings

### Biometric identification or surveillance risk
- Risk ID: `risk_f2588a928e`
- Category: `biometrics`
- Status: `confirmed`
- Severity: `high`
- Confidence: `high`
- Why it matters: Evidence references biometric identifiers such as face recognition, face embeddings, gait, or emotion recognition.
- Evidence: src/main.py:1, src/main.py:2, README.md:1, src/main.py:2
- Missing context: Consent process, data retention, access controls, deployment setting, and affected population.

## Potential Risks

### Possible re-identification risk if dataset is released
- Risk ID: `risk_33c2faca73`
- Category: `dataset_release_reidentification`
- Status: `potential`
- Severity: `high`
- Confidence: `medium`
- Why it matters: The repository contains data or release signals that may require review for re-identification, retention, and sharing risk.
- Evidence: data/schema.json:1, data/schema.json:1, src/main.py:2, data/schema.json, .
- Missing context: Whether raw records will be shared, retained, aggregated, or de-identified.

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
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `data/schema.json:1` | References student records or identifiers. | {"student_id": "string", "face_embedding": [0.1, 0.2]} Matched: student_id |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `data/schema.json:1` | References facial data. | {"student_id": "string", "face_embedding": [0.1, 0.2]} Matched: face_embedding |
| risk_33c2faca73 | `risk_signal` | `privacy_identifiability` | `src/main.py:2` | References facial data. | # compute face embedding for attendance tracking Matched: face |
| risk_33c2faca73 | `risk_signal` | `dataset_release_reidentification` | `data/schema.json` | Repository contains a dataset-like file by extension; content was not read. Release, retention, and de-identification review may be needed if it contains research data. |  |
| risk_33c2faca73 | `missing_context` | `dataset_release_reidentification` | `.` | Dataset files or release language were detected, but the following context may need clarification: data card/datasheet, retention/deletion policy, anonymization/de-identification policy. |  |
| risk_f2588a928e | `risk_signal` | `biometrics` | `src/main.py:1` | References face recognition or biometric libraries/data. | import face_recognition Matched: face_recognition |
| risk_f2588a928e | `risk_signal` | `biometrics` | `src/main.py:2` | References face recognition or biometric libraries/data. | # compute face embedding for attendance tracking Matched: face embedding |
| risk_f2588a928e | `risk_signal` | `surveillance_tracking` | `README.md:1` | References attendance or surveillance tracking. | Identifies students for classroom attendance. Consent, retention, and access controls are not documented. Matched: classroom attendance |
| risk_f2588a928e | `risk_signal` | `surveillance_tracking` | `src/main.py:2` | References attendance or surveillance tracking. | # compute face embedding for attendance tracking Matched: attendance tracking |
| risk_fc19ee1aa0 | `missing_context` | `license_dataset_terms` | `.` | No code or dataset license documentation was detected. |  |
| risk_8877616584 | `missing_context` | `missing_ethics_documentation` | `README/docs` | Repository evidence suggests these documentation topics may need clarification: anonymization/de-identification, bias/performance limitations, consent/reasonable expectation, data access controls, data card/datasheet, data retention/deletion, deployment limitations, privacy, .... Missing context is not proof of wrongdoing. |  |

## Positive Controls Detected

No positive controls were detected from repository evidence.

## Recommended Mitigations

- Create a data card or datasheet.
- Avoid public release of raw identifiable records.
- Aggregate, redact, or perturb fields that could identify people.
- Define retention and deletion policy.
- Document anonymization limits.
- Avoid identifying individuals unless necessary.
- Get appropriate consent.
- Avoid deployment in attendance, policing, employment, or surveillance contexts without review.
- Document bias and performance limitations.
- Avoid storing face images unless required.
- Add a clear code license.
- Document dataset source terms and redistribution limits.
- Avoid redistributing data unless terms permit it.
- Track third-party license obligations.
- Add an ethics, privacy, and data-handling section when relevant.
- Document limitations, release boundaries, and misuse considerations.
- Use a data card or model card for datasets or models.

## Advisor / IRB Discussion Questions

- Will raw data, derived data, or only aggregate statistics be released?
- What fields could enable re-identification?
- Is there a data card or datasheet?
- Why is biometric identification necessary?
- How is consent handled?
- How are embeddings, images, and identifiers protected or deleted?
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
