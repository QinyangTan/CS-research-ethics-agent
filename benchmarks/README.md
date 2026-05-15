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

Gold labels live in `benchmarks/gold/*.json`. Official scoring includes only labels with `review_status: "reviewed"` unless `--include-unreviewed` is passed.

## Hypothesis

Repo-ethics should be strongest on deterministic evidence grounding, forbidden-language avoidance, positive-control recognition, and prompt-injection resistance. Direct Codex may produce richer prose or identify unusual risks outside the scanner taxonomy.
