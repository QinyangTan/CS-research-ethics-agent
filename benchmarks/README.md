# CS Ethics Agent Benchmark

This benchmark compares the local repo-ethics toolchain against manually collected direct Codex-style reviews. It does not call hosted LLM APIs by default.

The fixtures are small synthetic repositories. They isolate ethics signals such as scraping, personal data, biometrics, security dual use, prompt injection, dataset release, missing documentation, and positive controls. They are not real studies and do not establish final ethical truth.

## Run

```bash
python3 benchmarks/scripts/generate_fixtures.py
python3 benchmarks/scripts/run_repo_ethics_benchmark.py
python3 benchmarks/scripts/score_reports.py
```

Direct Codex baseline outputs are optional. Use `benchmarks/prompts/direct_codex_prompt.md`, save outputs as `benchmarks/outputs/direct_codex/<case_id>.md`, then rerun scoring.

Two manual direct baselines are supported:

- Strong direct baseline: `benchmarks/prompts/direct_codex_prompt.md` -> `benchmarks/outputs/direct_codex/<case_id>.md`
- Naive direct baseline: `benchmarks/prompts/direct_codex_naive_prompt.md` -> `benchmarks/outputs/direct_codex_naive/<case_id>.md`

The helper prints collection instructions without running Codex by default:

```bash
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline strong
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline naive
```

If `--direct-codex-command` is supplied, that evaluator-provided command is executed locally; review it carefully before use.

Gold labels live in `benchmarks/gold/*.json`. Official scoring includes only labels with `review_status: "reviewed"` unless `--include-unreviewed` is passed.

## Metrics

Scores are reported as separate diagnostics, not as one blended grade. The benchmark tracks category recall, evidence groundedness, missing-context recall, positive-control recognition, expected-absent risk false positives, forbidden-language violations, unsupported conclusions, actionability, and secret leakage.

It also reports `unexpected_missing_context_count` and `unexpected_positive_control_count`. These count missing-context or safeguard categories that a system surfaced beyond the gold labels. They are not treated as risk false positives; they help reviewers distinguish useful caution from noisy extra categories.

## Hypothesis

Repo-ethics is designed to emphasize deterministic evidence grounding, forbidden-language avoidance, positive-control recognition, and prompt-injection resistance. Direct Codex may produce richer prose or identify unusual risks outside the scanner taxonomy. These scores measure report behavior on synthetic controlled cases, not final ethical truth.

Direct Markdown scoring is section-aware. Reports with recognizable risk, evidence, missing-context, question, safeguard, or mitigation sections receive `sectioned_markdown`; unstructured Markdown uses conservative `fallback_markdown`. Repo-ethics JSON output uses `structured_json`.
