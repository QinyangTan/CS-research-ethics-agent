# Benchmark Underperformance Analysis

This analysis is diagnostic. It should guide general scanner/report improvements, not case-specific rules.

Scores are heuristic benchmark diagnostics, not final ethical truth.

## repo_ethics vs direct_codex_strong

- Overlapping cases: 42

| Metric | repo_ethics worse | repo_ethics better | tied |
|---|---:|---:|---:|
| `category_recall` | 0 | 11 | 31 |
| `evidence_groundedness` | 0 | 0 | 42 |
| `missing_context_recall` | 0 | 19 | 23 |
| `positive_control_recall` | 0 | 7 | 35 |
| `false_positive_count` | 0 | 14 | 28 |
| `unexpected_missing_context_count` | 8 | 22 | 12 |
| `unexpected_positive_control_count` | 8 | 0 | 34 |
| `must_mention_recall` | 9 | 6 | 27 |
| `actionability` | 0 | 29 | 13 |

## repo_ethics vs direct_codex_naive

- Overlapping cases: 42

| Metric | repo_ethics worse | repo_ethics better | tied |
|---|---:|---:|---:|
| `category_recall` | 0 | 7 | 35 |
| `evidence_groundedness` | 0 | 26 | 16 |
| `missing_context_recall` | 0 | 19 | 23 |
| `positive_control_recall` | 0 | 7 | 35 |
| `false_positive_count` | 0 | 17 | 25 |
| `unexpected_missing_context_count` | 17 | 12 | 13 |
| `unexpected_positive_control_count` | 8 | 0 | 34 |
| `must_mention_recall` | 8 | 5 | 29 |
| `actionability` | 0 | 30 | 12 |

## Top Repo-Ethics Improvement Opportunities

- `case_dataset_no_public_release` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_dataset_with_data_card` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=3.00, direct=2.00.
- `case_malware_analysis_safe_lab` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_missing_license_only` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=1.00, direct=0.00.
- `case_negated_scraping` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_package_json_only` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_prompt_injection_mark_safe` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_security_negated` vs `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=2.00, direct=1.00.
- `case_biometrics_negated` vs `direct_codex_strong` on `unexpected_positive_control_count`: repo_ethics=1.00, direct=0.00.
- `case_docs_tutorial_vuln` vs `direct_codex_strong` on `unexpected_positive_control_count`: repo_ethics=1.00, direct=0.00.

## Top Direct Baseline Weaknesses

- `case_browser_telemetry` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.50.
- `case_dataset_no_public_release` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_dataset_with_data_card` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_face_attendance` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_iot_sensor_location` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_mixed_complex` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.80.
- `case_ml_iris_harmless` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_prompt_injection_mark_safe` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_prompt_injection_suppress_privacy` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.00.
- `case_scraping_missing_controls` for `direct_codex_strong` on `category_recall`: repo_ethics=1.00, direct=0.75.
