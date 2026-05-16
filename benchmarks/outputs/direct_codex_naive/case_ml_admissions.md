**Project Summary**

This appears to be an ML admissions decision project. The README says it “predicts admissions decisions from student profiles,” while the model file indicates use of `sklearn` and an “admissions grading model over student_id and demographic features” ([README.md](benchmarks/fixtures/case_ml_admissions/README.md:1), [model.py](benchmarks/fixtures/case_ml_admissions/src%202/model.py:2)).

**Ethics Risks**

- **High-stakes automated decision-making:** Admissions decisions affect educational access and life opportunities. The repo does not define whether predictions are advisory, triage-only, or used directly in decisions ([README.md](benchmarks/fixtures/case_ml_admissions/README.md:1)).

- **Demographic feature use and discrimination risk:** The model comment explicitly references “demographic features,” which can encode protected characteristics or proxies. Without fairness evaluation, this creates risk of disparate impact across race, gender, disability, socioeconomic status, nationality, or other protected groups ([model.py](benchmarks/fixtures/case_ml_admissions/src%202/model.py:2)).

- **Use of `student_id`:** `student_id` is likely personally identifying or linkable to student records. It may also let the model memorize historical outcomes rather than learn legitimate admissions-relevant signals ([model.py](benchmarks/fixtures/case_ml_admissions/src%202/model.py:2)).

- **Missing bias and validity documentation:** The README explicitly states that fairness, bias evaluation, and deployment boundaries are not documented. For an admissions model, that is a major governance gap ([README.md](benchmarks/fixtures/case_ml_admissions/README.md:1)).

- **Privacy and consent uncertainty:** The repo does not describe data provenance, consent, retention, de-identification, access controls, or compliance obligations such as FERPA in the U.S.

- **Opacity and contestability:** There is no model card, data card, explanation policy, audit process, or appeal mechanism documented. Affected applicants may be unable to understand or challenge adverse outcomes.

**Suggested Mitigations**

- Treat the system as decision support only, with a documented human review process and a ban on fully automated rejection/admission decisions.

- Remove `student_id` from model features unless there is a narrowly justified, audited reason. Use stable anonymous row IDs only outside the feature matrix.

- Create a model card covering intended use, prohibited use, training data, evaluation metrics, subgroup performance, known limitations, and monitoring.

- Add fairness evaluations before deployment: subgroup accuracy, false positive/false negative rates, calibration, selection rates, and intersectional analysis.

- Document data provenance, legal basis or consent, retention period, access controls, and de-identification strategy.

- Define deployment boundaries: who may use the model, what decisions it may inform, required review thresholds, logging, periodic audits, and rollback criteria.

- Add applicant-facing transparency and an appeal or reconsideration path.

**Questions For The Researcher**

1. Is this model intended for research analysis only, admissions staff decision support, or operational admissions decisions?

2. Which demographic attributes are used, and are any protected characteristics or close proxies included?

3. Why is `student_id` part of the model inputs? Is it used as a feature or only as an identifier?

4. What dataset was used, and were students informed or asked for consent for this use?

5. Have you measured subgroup performance and disparate impact across protected and intersectional groups?

6. What human review, appeal, and audit processes exist for applicants affected by model outputs?

7. What are the explicit prohibited uses of this model?