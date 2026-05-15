# Benchmark Summary

These scores measure report behavior on synthetic controlled cases, not final ethical truth.

## Output Availability

- `direct_codex_naive`: 0/42 outputs available
- `direct_codex_strong`: 0/42 outputs available
- `repo_ethics`: 42/42 outputs available

## Metrics

| System | Cases | Category Recall | Groundedness | Missing Context | Positive Controls | False Positives | Must Mention | Must-not Violations | Forbidden | Overclaims | Secret Leaks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| repo_ethics | 42 | 1.00 | 0.87 | 0.95 | 0.96 | 0.00 | 0.71 | 0.00 | 0.00 | 0.00 | 0.00 |

## Interpretation

- Compare systems by separate metrics rather than a blended score.
- Higher category recall on this synthetic benchmark means a report named more expected taxonomy categories; it is not a final ethics judgment.
- Lower expected-absent false positives indicate fewer expected-absent categories were reported as risks for these controlled cases.
- Higher evidence-groundedness means expected repository paths were cited more often.
- Positive-control recognition is reported separately from risk recall so safeguards do not erase underlying risk signals.
- Direct Codex output counts may cover only a subset of cases; check output availability before comparing aggregate metrics.

## Per-Category Recall

| Category | repo_ethics |
|---|---:|
| `biometrics` | 1/1 |
| `consent_reasonable_expectation` | 2/2 |
| `dataset_release_reidentification` | 9/9 |
| `ml_fairness_deployment_risk` | 5/5 |
| `privacy_identifiability` | 12/12 |
| `prompt_injection_attempt` | 4/4 |
| `secret_exposure` | 1/1 |
| `security_dual_use` | 4/4 |
| `surveillance_tracking` | 2/2 |
| `web_scraping_platform_governance` | 5/5 |

## Hardest Repo-Ethics Cases

- `case_secret_placeholder_safe`: recall 1.00, groundedness 0.00, false positives 0.
- `case_readme_absent`: recall 1.00, groundedness 0.00, false positives 0.
- `case_large_binary_assets`: recall 1.00, groundedness 0.00, false positives 0.
- `case_surveillance_tracking`: recall 1.00, groundedness 0.50, false positives 0.
- `case_prompt_injection_suppress_privacy`: recall 1.00, groundedness 0.50, false positives 0.

## Comparative Notes

- No direct Codex baseline outputs were present, so comparative claims are not reported.

## Recommended Improvements

- Review hardest cases manually before changing scanner logic.
- Expand reviewed labels with real, permissioned teaching repositories.
- Add aliases when direct baseline reports identify correct issues with different wording.
- Keep positive-control and missing-context metrics separate from category recall.
