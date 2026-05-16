# Benchmark Results

`benchmarks/results/` contains deterministic scoring outputs produced by `benchmarks/scripts/score_reports.py`.

- `results.json` stores per-case rows and aggregate metrics for each available system.
- `summary.md` is a human-readable rendering of the same metrics.
- `output_availability` shows how many reviewed cases have outputs for each system.
- `scoring_mode_counts` shows how many outputs were scored as `structured_json`, `sectioned_markdown`, or `fallback_markdown`.
- `underperformance_analysis.md` and `underperformance_analysis.json`, when generated, identify metric-specific improvement opportunities.
- `direct_output_provenance.md` documents prompt usage, path-only sanitization, and direct-baseline handling rules.

Metrics are intentionally separate rather than blended. Category recall, expected-absent false positives, evidence-groundedness, missing-context recall, positive-control recognition, extra missing-context categories, extra positive-control categories, language discipline, actionability, and secret leakage describe different report behaviors.

`unexpected_missing_context_count` and `unexpected_positive_control_count` are diagnostic noise/caution metrics. They count categories surfaced beyond the reviewed gold labels for missing context or safeguards. They are not risk false positives, but high values should be reviewed to decide whether they reflect useful caution or noisy reporting.

The benchmark is synthetic. Fixtures are small controlled repositories, not real studies. These scores measure report behavior on synthetic controlled cases, not final ethical truth.

## Direct Codex Outputs

Manual direct baselines can be added before scoring:

- Naive direct baseline: save Markdown to `benchmarks/outputs/direct_codex_naive/<case_id>.md`.
- Strong direct baseline: save Markdown to `benchmarks/outputs/direct_codex/<case_id>.md`.

Then run:

```bash
python3 benchmarks/scripts/score_reports.py
python3 benchmarks/scripts/summarize_results.py
python3 benchmarks/scripts/write_direct_comparison_report.py
```

Compare `repo_ethics`, `direct_codex_strong`, and `direct_codex_naive` by individual metrics and output availability. Avoid broad claims from partial direct-output coverage.

Path-only sanitization is allowed for benchmark output artifacts to remove local absolute repository prefixes. Do not edit direct baseline risk claims, evidence descriptions, mitigations, or conclusions after generation.

## Underperformance Analysis

`underperformance_analysis.*` groups metric gaps into root-cause buckets and repeated improvement themes. Use these diagnostics to identify general follow-up areas such as scanner precision, report templates, taxonomy aliases, or mitigation/question knowledge-base coverage. Do not use them to create case-specific production rules for individual benchmark fixtures.
