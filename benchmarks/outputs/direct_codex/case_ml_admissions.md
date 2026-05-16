# Computer Science Research Ethics Pre-Review

## Project Summary

This repository appears to describe an ML project for predicting admissions decisions from student profiles. The available implementation is minimal: `src/model.py` imports `sklearn` and includes a comment describing an “admissions grading model over student_id and demographic features.”

Evidence:
- [README.md](benchmarks/fixtures/case_ml_admissions/README.md:1): states the project predicts admissions decisions from student profiles.
- [src/model.py](benchmarks/fixtures/case_ml_admissions/src/model.py:2): references `student_id` and demographic features.

## Risk Categories And Evidence

### High-Stakes Decision Support

Admissions prediction or grading can affect educational access, opportunity, and institutional outcomes. Even if used only as research, the domain is high impact.

Evidence:
- [README.md](benchmarks/fixtures/case_ml_admissions/README.md:1) says the system predicts admissions decisions.
- [src/model.py](benchmarks/fixtures/case_ml_admissions/src/model.py:2) describes an admissions grading model.

### Bias And Discrimination Risk

The code comment explicitly references demographic features. In admissions, demographic variables may be protected or sensitive attributes depending on context, and may also proxy for socioeconomic status, race, ethnicity, gender, disability, geography, or other legally and ethically sensitive categories.

Evidence:
- [src/model.py](benchmarks/fixtures/case_ml_admissions/src/model.py:2) references “demographic features.”
- [README.md](benchmarks/fixtures/case_ml_admissions/README.md:1) says fairness and bias evaluation are not documented.

### Privacy And Re-Identification Risk

The reference to `student_id` suggests the project may use directly identifying or linkable student-level records. Even if names are absent, student IDs can enable re-identification or linkage to institutional records.

Evidence:
- [src/model.py](benchmarks/fixtures/case_ml_admissions/src/model.py:2) references `student_id`.

### Lack Of Deployment Boundaries

The README explicitly says deployment boundaries are not documented. For an admissions model, unclear boundaries create risks of inappropriate operational use, automation bias, overreliance, and use outside the validated population.

Evidence:
- [README.md](benchmarks/fixtures/case_ml_admissions/README.md:1).

### Insufficient Transparency And Reproducibility

The repository does not include dataset documentation, feature definitions, model training logic, evaluation metrics, intended use, exclusion criteria, governance process, or human review policy.

Evidence:
- Only two visible project files were found: [README.md](benchmarks/fixtures/case_ml_admissions/README.md:1) and [src/model.py](benchmarks/fixtures/case_ml_admissions/src/model.py:1).
- The source file contains only an import and a comment.

## Missing Context And Clarification Questions

- What data source is used, and were students notified or consent obtained where appropriate?
- What exact demographic features are included, and why are they necessary?
- Is `student_id` used as a feature, key, join field, audit field, or leakage-prone identifier?
- Is the model intended for research only, decision support, ranking, screening, or fully automated admissions action?
- What outcomes are predicted: historical admit decisions, academic success, enrollment, yield, or something else?
- What fairness analyses are planned across demographic groups and intersectional subgroups?
- How will errors be handled, appealed, audited, and explained to affected applicants?
- Who has access to raw data, trained models, predictions, and logs?
- Are there institutional policies, advisor review, data use agreements, or review-body expectations governing this work?

## Concrete Mitigations

- Remove direct identifiers such as `student_id` from model features unless there is a justified, documented non-predictive use.
- Create a data card documenting provenance, consent/authorization basis, retention, fields, missingness, linkage risks, and access controls.
- Create a model card documenting intended use, non-use cases, training data scope, evaluation metrics, subgroup performance, and known limitations.
- Define deployment boundaries clearly: research-only, offline analysis, decision support only, or prohibited operational uses.
- Run fairness evaluation before any real-world use, including group and intersectional metrics relevant to admissions harms.
- Test for target leakage, especially if historical admissions decisions are used as labels.
- Require human review and appeal pathways for any use that could influence admissions outcomes.
- Add privacy controls: de-identification, access logging, least-privilege access, encrypted storage, and deletion timelines.
- Document whether demographic attributes are used for fairness auditing only, model training, post-processing, or reporting.
- Add explicit review checkpoints with the advisor, department, data steward, or appropriate institutional review process before using real applicant data.

## Advisor Or Review-Body Discussion Questions

- Is it ethically appropriate to predict admissions decisions from historical data that may encode past institutional bias?
- Should demographic variables be used in training, excluded from training but used for auditing, or handled through another fairness-aware design?
- What level of human oversight is required before predictions can influence admissions-related judgments?
- What harms could arise from false positives, false negatives, or differential error rates across groups?
- What evidence would be required before considering any operational pilot?
- What privacy protections are proportionate for student-level admissions data?
- How will affected students understand, contest, or receive explanation for model-influenced decisions?

## Limitations Of This Review

This review is based only on direct inspection of the visible repository files. The repository contains very little implementation detail and no dataset, training code, evaluation results, consent documentation, or governance materials. I did not use repo-ethics MCP tools or scanner output. This is a pre-review risk assessment, not a final ethical approval, rejection, legal determination, compliance finding, safety certification, or IRB determination.