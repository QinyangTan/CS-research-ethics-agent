# Benchmark Underperformance Analysis

This analysis is diagnostic. It should guide general scanner/report improvements, not case-specific rules.

Scores are heuristic benchmark diagnostics, not final ethical truth.

## repo_ethics vs direct_codex_strong

- Overlapping cases: 42

| Metric | repo_ethics worse | repo_ethics better | tied |
|---|---:|---:|---:|
| `category_recall` | 0 | 11 | 31 |
| `evidence_groundedness` | 0 | 0 | 42 |
| `missing_context_recall` | 0 | 21 | 21 |
| `positive_control_recall` | 0 | 7 | 35 |
| `false_positive_count` | 0 | 14 | 28 |
| `unexpected_missing_context_count` | 0 | 39 | 3 |
| `unexpected_positive_control_count` | 0 | 0 | 42 |
| `must_mention_recall` | 7 | 4 | 31 |
| `actionability` | 0 | 29 | 13 |

## repo_ethics vs direct_codex_naive

- Overlapping cases: 42

| Metric | repo_ethics worse | repo_ethics better | tied |
|---|---:|---:|---:|
| `category_recall` | 0 | 7 | 35 |
| `evidence_groundedness` | 0 | 26 | 16 |
| `missing_context_recall` | 0 | 21 | 21 |
| `positive_control_recall` | 0 | 7 | 35 |
| `false_positive_count` | 0 | 17 | 25 |
| `unexpected_missing_context_count` | 0 | 32 | 10 |
| `unexpected_positive_control_count` | 0 | 0 | 42 |
| `must_mention_recall` | 8 | 5 | 29 |
| `actionability` | 0 | 30 | 12 |

## Root-Cause Buckets

| Bucket | Cases | Likely follow-up area |
|---|---:|---|
| `actionability_gap` | 0 | mitigation/question KB |
| `extra_missing_context_noise` | 0 | scanner precision |
| `extra_positive_control_noise` | 0 | scanner precision |
| `false_positive` | 0 | scanner precision |
| `lower_groundedness` | 0 | report template |
| `missed_expected_category` | 0 | scanner precision or taxonomy mapping |
| `must_mention_gap` | 15 | mitigation/question KB |
| `report_discipline_issue` | 0 | report language policy |

## Top Improvement Themes

- must mention gap: 15 occurrence(s); follow-up area: mitigation/question KB.

## Top Repo-Ethics Improvement Opportunities

- `case_dataset_no_public_release` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_ml_iris_harmless` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_negated_scraping` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_package_json_only` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_pii_negated_aggregate` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_security_negated` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_tests_mention_exploit` vs `direct_codex_strong` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_biometrics_negated` vs `direct_codex_naive` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_dataset_no_public_release` vs `direct_codex_naive` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.
- `case_ml_iris_harmless` vs `direct_codex_naive` on `must_mention_recall`: repo_ethics=0.00, direct=1.00; bucket=`must_mention_gap`, follow-up=mitigation/question KB.

## Top Direct Baseline Weaknesses

- `case_model_card_present` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=5.00.
- `case_surveillance_tracking` for `direct_codex_naive` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=5.00.
- `case_dataset_public_release` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=4.00.
- `case_scraping_with_controls` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=1.00, direct=5.00.
- `case_surveillance_tracking` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=4.00.
- `case_dataset_public_release` for `direct_codex_naive` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=4.00.
- `case_face_attendance` for `direct_codex_naive` on `unexpected_missing_context_count`: repo_ethics=1.00, direct=5.00.
- `case_readme_clear_harmless` for `direct_codex_strong` on `false_positive_count`: repo_ethics=0.00, direct=3.00.
- `case_large_parquet_data` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=3.00.
- `case_ml_admissions` for `direct_codex_strong` on `unexpected_missing_context_count`: repo_ethics=0.00, direct=3.00.
