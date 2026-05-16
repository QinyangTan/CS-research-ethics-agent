# Direct Codex vs Repo-Ethics Benchmark Report

**Current empirical status:** Complete direct comparison  
**Direct baseline coverage:** 42/42 strong, 42/42 naive

## Setup

- Repository: `QinyangTan/CS-research-ethics-agent`
- Benchmark run timestamp: 2026-05-16 13:54:02
- Benchmark version: `0.1.0`
- Reviewed synthetic cases: 42
- Systems requested: `repo_ethics`, `direct_codex_strong`, `direct_codex_naive`
- Prompts:
  - Strong direct baseline: `benchmarks/prompts/direct_codex_prompt.md`
  - Naive direct baseline: `benchmarks/prompts/direct_codex_naive_prompt.md`
- Commands run:
  - `python3 -m pip install -e packages/repo-ethics-mcp`
  - `pytest`
  - `python3 scripts/check_no_hosted_llm_calls.py`
  - `python3 benchmarks/scripts/generate_fixtures.py`
  - `python3 benchmarks/scripts/run_repo_ethics_benchmark.py`
  - `python3 benchmarks/scripts/sanitize_benchmark_outputs.py --check`
  - `python3 benchmarks/scripts/score_reports.py`
  - `python3 benchmarks/scripts/summarize_results.py`
  - `python3 benchmarks/scripts/analyze_underperformance.py`
  - `python3 benchmarks/scripts/write_direct_comparison_report.py`

## Output Availability

| System | Outputs Available | Reviewed Cases | Coverage |
|---|---:|---:|---:|
| `repo_ethics` | 42 | 42 | 100.00% |
| `direct_codex_strong` | 42 | 42 | 100.00% |
| `direct_codex_naive` | 42 | 42 | 100.00% |

## Empirical Answer

Complete direct comparison. Results were mixed by metric on these reviewed synthetic cases.

## What Can Be Concluded From This Run

This run can compare systems on overlapping reviewed synthetic cases.

The comparison is metric-specific: higher recall or groundedness on one metric does not imply overall ethical correctness.

The benchmark infrastructure is now populated with direct baseline outputs for the available coverage.

## Aggregate Metrics

These aggregate metrics include all scored outputs for each system. Compare them alongside output coverage and overlapping case counts.

| System | Category Recall | Evidence Groundedness | Missing Context Recall | Positive Control Recall | False Positives | Extra Missing Context | Extra Positive Controls | Forbidden Violations | Overclaims | Secret Leaks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `repo_ethics` | 1.00 | 1.00 | 0.95 | 0.96 | 0.00 | 1.57 | 0.24 | 0.00 | 0.00 | 0.00 |
| `direct_codex_strong` | 0.79 | 1.00 | 0.52 | 0.83 | 0.50 | 2.24 | 0.00 | 0.00 | 0.02 | 0.00 |
| `direct_codex_naive` | 0.86 | 0.60 | 0.54 | 0.83 | 0.55 | 1.69 | 0.00 | 0.00 | 0.00 | 0.00 |

## Scoring Mode Counts

| System | structured_json | sectioned_markdown | fallback_markdown |
|---|---:|---:|---:|
| `repo_ethics` | 42 | 0 | 0 |
| `direct_codex_strong` | 0 | 42 | 0 |
| `direct_codex_naive` | 0 | 42 | 0 |

## Metric-by-Metric Interpretation

- Category recall measures expected risk categories found.
- Evidence groundedness measures expected repository-path citation.
- Missing-context recall and positive-control recall measure expected non-risk categories found.
- False positives refer to expected-absent risk categories only.
- Extra missing-context and positive-control categories are diagnostic. They are not counted as risk false positives, but high values may indicate over-cautious or noisy reporting.
- Forbidden-language violations, unsupported conclusions, and secret leakage are report-discipline checks.

## Overlapping Case Comparison

Higher is better for recall, groundedness, must-mention recall, and actionability. Lower is better for false positives, extra missing context, extra positive controls, forbidden violations, overclaims, secret leaks, and must-not violations.

### repo_ethics vs direct_codex_strong

| Metric | repo_ethics higher/better | direct_codex_strong higher/better | tied | overlapping cases |
|---|---:|---:|---:|---:|
| Category Recall | 11 | 0 | 31 | 42 |
| Evidence Groundedness | 0 | 0 | 42 | 42 |
| Missing Context Recall | 19 | 0 | 23 | 42 |
| Positive Control Recall | 7 | 0 | 35 | 42 |
| False Positives | 14 | 0 | 28 | 42 |
| Extra Missing Context | 22 | 8 | 12 | 42 |
| Extra Positive Controls | 0 | 8 | 34 | 42 |
| Forbidden Violations | 0 | 0 | 42 | 42 |
| Overclaims | 1 | 0 | 41 | 42 |
| Secret Leaks | 0 | 0 | 42 | 42 |
| Must Mention Recall | 6 | 9 | 27 | 42 |
| Must-not Violations | 0 | 0 | 42 | 42 |
| Actionability | 29 | 0 | 13 | 42 |

### repo_ethics vs direct_codex_naive

| Metric | repo_ethics higher/better | direct_codex_naive higher/better | tied | overlapping cases |
|---|---:|---:|---:|---:|
| Category Recall | 7 | 0 | 35 | 42 |
| Evidence Groundedness | 26 | 0 | 16 | 42 |
| Missing Context Recall | 19 | 0 | 23 | 42 |
| Positive Control Recall | 7 | 0 | 35 | 42 |
| False Positives | 17 | 0 | 25 | 42 |
| Extra Missing Context | 12 | 17 | 13 | 42 |
| Extra Positive Controls | 0 | 8 | 34 | 42 |
| Forbidden Violations | 0 | 0 | 42 | 42 |
| Overclaims | 0 | 0 | 42 | 42 |
| Secret Leaks | 0 | 0 | 42 | 42 |
| Must Mention Recall | 5 | 8 | 29 | 42 |
| Must-not Violations | 0 | 0 | 42 | 42 |
| Actionability | 30 | 0 | 12 | 42 |

## Where Repo-Ethics Performed Better

- Against `direct_codex_strong`, `repo_ethics` had the better directional score on: Category Recall (11/42); Missing Context Recall (19/42); Positive Control Recall (7/42); False Positives (14/42); Extra Missing Context (22/42); Overclaims (1/42); Must Mention Recall (6/42); Actionability (29/42).
- Against `direct_codex_naive`, `repo_ethics` had the better directional score on: Category Recall (7/42); Evidence Groundedness (26/42); Missing Context Recall (19/42); Positive Control Recall (7/42); False Positives (17/42); Extra Missing Context (12/42); Must Mention Recall (5/42); Actionability (30/42).

## Where Direct Codex Performed Better

- Against `direct_codex_strong`, `direct_codex_strong` had the better directional score on: Extra Missing Context (8/42); Extra Positive Controls (8/42); Must Mention Recall (9/42).
- Against `direct_codex_naive`, `direct_codex_naive` had the better directional score on: Extra Missing Context (17/42); Extra Positive Controls (8/42); Must Mention Recall (8/42).

## Inconclusive or Mixed Results

- Direct output coverage is complete in this run.
- The fixtures are synthetic and intentionally small.
- Direct Markdown scoring is heuristic and depends on taxonomy aliases.
- The benchmark does not use an LLM-as-judge.
- These scores measure report behavior on controlled cases, not final ethical truth.

## Case-Level Highlights

| Case ID | repo_ethics recall | strong direct recall | naive direct recall | notes |
|---|---:|---:|---:|---|
| `case_scraping_missing_controls` | 1.00 | 0.75 | 1.0 | Repo-ethics row available. |
| `case_scraping_with_controls` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_negated_scraping` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_pii_student_contacts` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_pii_negated_aggregate` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_dataset_public_release` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_dataset_no_public_release` | 1.00 | 0.0 | 0.0 | Repo-ethics row available. |
| `case_dataset_with_data_card` | 1.00 | 0.0 | 0.0 | Repo-ethics row available. |

## Improvement Opportunities

These lists are diagnostic under this scoring rubric and require manual review before changing scanner logic.

### Repo-Ethics Improvement Opportunities

- `case_dataset_no_public_release` on `unexpected_missing_context_count` against `direct_codex_strong` (repo_ethics=2.00, direct=1.00).
- `case_dataset_with_data_card` on `unexpected_missing_context_count` against `direct_codex_strong` (repo_ethics=3.00, direct=2.00).
- `case_malware_analysis_safe_lab` on `unexpected_missing_context_count` against `direct_codex_strong` (repo_ethics=2.00, direct=1.00).
- `case_missing_license_only` on `unexpected_missing_context_count` against `direct_codex_strong` (repo_ethics=1.00, direct=0.00).
- `case_negated_scraping` on `unexpected_missing_context_count` against `direct_codex_strong` (repo_ethics=2.00, direct=1.00).

### Direct Baseline Weaknesses

- `case_browser_telemetry` on `category_recall` against `direct_codex_strong` (repo_ethics=1.00, direct=0.50).
- `case_dataset_no_public_release` on `category_recall` against `direct_codex_strong` (repo_ethics=1.00, direct=0.00).
- `case_dataset_with_data_card` on `category_recall` against `direct_codex_strong` (repo_ethics=1.00, direct=0.00).
- `case_face_attendance` on `category_recall` against `direct_codex_strong` (repo_ethics=1.00, direct=0.00).
- `case_iot_sensor_location` on `category_recall` against `direct_codex_strong` (repo_ethics=1.00, direct=0.00).

## Conclusion

Results were mixed on this benchmark.

Use the aggregate metrics and overlapping case comparison tables above to identify which system was higher or lower on each metric in this run.

These findings are limited to the reviewed synthetic cases and should be validated on real, permissioned repositories before drawing broader conclusions.
