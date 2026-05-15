# Direct Codex vs Repo-Ethics Benchmark Report

**Current empirical status:** Complete direct comparison  
**Direct baseline coverage:** 42/42 strong, 42/42 naive

## Setup

- Repository: `QinyangTan/CS-research-ethics-agent`
- Benchmark run timestamp: 2026-05-16 05:49:12
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
  - `python3 benchmarks/scripts/score_reports.py`
  - `python3 benchmarks/scripts/summarize_results.py`
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
| `repo_ethics` | 1.00 | 0.87 | 0.95 | 0.96 | 0.00 | 1.57 | 0.24 | 0.00 | 0.00 | 0.00 |
| `direct_codex_strong` | 0.81 | 1.00 | 0.57 | 0.83 | 0.52 | 2.21 | 0.07 | 0.00 | 0.02 | 0.00 |
| `direct_codex_naive` | 0.92 | 0.60 | 0.79 | 0.94 | 0.62 | 1.36 | 0.40 | 0.00 | 0.00 | 0.00 |

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
| Category Recall | 9 | 0 | 33 | 42 |
| Evidence Groundedness | 0 | 8 | 34 | 42 |
| Missing Context Recall | 17 | 0 | 25 | 42 |
| Positive Control Recall | 7 | 0 | 35 | 42 |
| False Positives | 14 | 0 | 28 | 42 |
| Extra Missing Context | 21 | 9 | 12 | 42 |
| Extra Positive Controls | 1 | 7 | 34 | 42 |
| Forbidden Violations | 0 | 0 | 42 | 42 |
| Overclaims | 1 | 0 | 41 | 42 |
| Secret Leaks | 0 | 0 | 42 | 42 |
| Must Mention Recall | 6 | 10 | 26 | 42 |
| Must-not Violations | 0 | 0 | 42 | 42 |
| Actionability | 29 | 0 | 13 | 42 |

### repo_ethics vs direct_codex_naive

| Metric | repo_ethics higher/better | direct_codex_naive higher/better | tied | overlapping cases |
|---|---:|---:|---:|---:|
| Category Recall | 5 | 0 | 37 | 42 |
| Evidence Groundedness | 20 | 2 | 20 | 42 |
| Missing Context Recall | 9 | 2 | 31 | 42 |
| Positive Control Recall | 1 | 0 | 41 | 42 |
| False Positives | 18 | 0 | 24 | 42 |
| Extra Missing Context | 14 | 22 | 6 | 42 |
| Extra Positive Controls | 7 | 7 | 28 | 42 |
| Forbidden Violations | 0 | 0 | 42 | 42 |
| Overclaims | 0 | 0 | 42 | 42 |
| Secret Leaks | 0 | 0 | 42 | 42 |
| Must Mention Recall | 5 | 9 | 28 | 42 |
| Must-not Violations | 0 | 0 | 42 | 42 |
| Actionability | 30 | 0 | 12 | 42 |

## Where Repo-Ethics Performed Better

- Against `direct_codex_strong`, `repo_ethics` had the better directional score on: Category Recall (9/42); Missing Context Recall (17/42); Positive Control Recall (7/42); False Positives (14/42); Extra Missing Context (21/42); Extra Positive Controls (1/42); Overclaims (1/42); Must Mention Recall (6/42); Actionability (29/42).
- Against `direct_codex_naive`, `repo_ethics` had the better directional score on: Category Recall (5/42); Evidence Groundedness (20/42); Missing Context Recall (9/42); Positive Control Recall (1/42); False Positives (18/42); Extra Missing Context (14/42); Extra Positive Controls (7/42); Must Mention Recall (5/42); Actionability (30/42).

## Where Direct Codex Performed Better

- Against `direct_codex_strong`, `direct_codex_strong` had the better directional score on: Evidence Groundedness (8/42); Extra Missing Context (9/42); Extra Positive Controls (7/42); Must Mention Recall (10/42).
- Against `direct_codex_naive`, `direct_codex_naive` had the better directional score on: Evidence Groundedness (2/42); Missing Context Recall (2/42); Extra Missing Context (22/42); Extra Positive Controls (7/42); Must Mention Recall (9/42).

## Inconclusive or Mixed Results

- Direct output coverage is complete in this run.
- The fixtures are synthetic and intentionally small.
- Direct Markdown scoring is heuristic and depends on taxonomy aliases.
- The benchmark does not use an LLM-as-judge.
- These scores measure report behavior on controlled cases, not final ethical truth.

## Case-Level Highlights

| Case ID | repo_ethics recall | strong direct recall | naive direct recall | notes |
|---|---:|---:|---:|---|
| `case_secret_placeholder_safe` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_readme_absent` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_large_binary_assets` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_surveillance_tracking` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_prompt_injection_suppress_privacy` | 1.00 | 0.0 | 1.0 | Repo-ethics row available. |
| `case_ml_iris_harmless` | 1.00 | 1.0 | 0.0 | Repo-ethics row available. |
| `case_recommender_manipulation` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |
| `case_tests_mention_exploit` | 1.00 | 1.0 | 1.0 | Repo-ethics row available. |

## Conclusion

Results were mixed on this benchmark.

Repo-ethics had stronger aggregate category recall, missing-context recall, positive-control recall, expected-absent false-positive control, and actionability than both direct baselines. The strong direct baseline had higher aggregate evidence-groundedness and fewer extra positive-control categories. The naive direct baseline had fewer extra missing-context categories and higher must-mention recall.

These findings are limited to the reviewed synthetic cases and should be validated on real, permissioned repositories before drawing broader conclusions.
