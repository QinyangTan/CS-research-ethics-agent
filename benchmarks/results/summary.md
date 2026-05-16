# Benchmark Summary

These scores measure report behavior on synthetic controlled cases, not final ethical truth.

## Output Availability

- `direct_codex_naive`: 42/42 outputs available
- `direct_codex_strong`: 42/42 outputs available
- `repo_ethics`: 42/42 outputs available

## Metrics

| System | Cases | Category Recall | Groundedness | Missing Context | Positive Controls | False Positives | Extra Missing Context | Extra Positive Controls | Must Mention | Must-not Violations | Forbidden | Overclaims | Secret Leaks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| direct_codex_naive | 42 | 0.86 | 0.60 | 0.54 | 0.83 | 0.55 | 1.69 | 0.00 | 0.82 | 0.00 | 0.00 | 0.00 | 0.00 |
| direct_codex_strong | 42 | 0.79 | 1.00 | 0.52 | 0.83 | 0.50 | 2.24 | 0.00 | 0.82 | 0.00 | 0.00 | 0.02 | 0.00 |
| repo_ethics | 42 | 1.00 | 1.00 | 0.95 | 0.96 | 0.00 | 1.57 | 0.24 | 0.74 | 0.00 | 0.00 | 0.00 | 0.00 |

## Scoring Mode Counts

| System | structured_json | sectioned_markdown | fallback_markdown |
|---|---:|---:|---:|
| direct_codex_naive | 0 | 42 | 0 |
| direct_codex_strong | 0 | 42 | 0 |
| repo_ethics | 42 | 0 | 0 |

## Interpretation

- Compare systems by separate metrics rather than a blended score.
- Higher category recall on this synthetic benchmark means a report named more expected taxonomy categories; it is not a final ethics judgment.
- Lower expected-absent false positives indicate fewer expected-absent categories were reported as risks for these controlled cases.
- Extra missing context means the system surfaced missing-context categories beyond the gold labels.
- Extra positive controls means the system surfaced safeguard/control categories beyond the gold labels.
- Extra categories are not automatically errors, but they may indicate useful caution or noisy reporting and should be manually reviewed.
- Higher evidence-groundedness means expected repository paths were cited more often.
- Positive-control recognition is reported separately from risk recall so safeguards do not erase underlying risk signals.
- Direct Codex output counts may cover only a subset of cases; check output availability before comparing aggregate metrics.

## Per-Category Recall

| Category | direct_codex_naive | direct_codex_strong | repo_ethics |
|---|---:|---:|---:|
| `biometrics` | 1/1 | 0/1 | 1/1 |
| `consent_reasonable_expectation` | 2/2 | 1/2 | 2/2 |
| `dataset_release_reidentification` | 5/9 | 5/9 | 9/9 |
| `ml_fairness_deployment_risk` | 4/5 | 3/5 | 5/5 |
| `privacy_identifiability` | 11/12 | 8/12 | 12/12 |
| `prompt_injection_attempt` | 3/4 | 1/4 | 4/4 |
| `secret_exposure` | 1/1 | 1/1 | 1/1 |
| `security_dual_use` | 4/4 | 4/4 | 4/4 |
| `surveillance_tracking` | 2/2 | 1/2 | 2/2 |
| `web_scraping_platform_governance` | 4/5 | 4/5 | 5/5 |

## Hardest Repo-Ethics Cases

- `case_scraping_missing_controls`: recall 1.00, groundedness 1.00, false positives 0.
- `case_scraping_with_controls`: recall 1.00, groundedness 1.00, false positives 0.
- `case_negated_scraping`: recall 1.00, groundedness 1.00, false positives 0.
- `case_pii_student_contacts`: recall 1.00, groundedness 1.00, false positives 0.
- `case_pii_negated_aggregate`: recall 1.00, groundedness 1.00, false positives 0.

## Comparative Notes

- Direct baselines are scored only where manually collected Markdown outputs are present; compare overlapping cases and individual metrics.
- `direct_codex_naive` overlaps repo-ethics on 42 cases.
- `direct_codex_strong` overlaps repo-ethics on 42 cases.

## Recommended Improvements

- Review hardest cases manually before changing scanner logic.
- Expand reviewed labels with real, permissioned teaching repositories.
- Add aliases when direct baseline reports identify correct issues with different wording.
- Keep positive-control and missing-context metrics separate from category recall.
- Review extra missing-context and positive-control categories to distinguish useful caution from noise.
