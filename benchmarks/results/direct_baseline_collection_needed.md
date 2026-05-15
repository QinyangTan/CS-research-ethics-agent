# Direct Baseline Collection Needed

Direct Codex baseline outputs were not collected for all reviewed cases in this run, so direct comparison is incomplete.

A direct comparison requires Markdown outputs in:

- Strong direct baseline: `benchmarks/outputs/direct_codex/<case_id>.md`
- Naive direct baseline: `benchmarks/outputs/direct_codex_naive/<case_id>.md`

Use the reviewed cases listed in `benchmarks/cases/cs_ethics_cases.jsonl`. For each case, review the corresponding fixture under `benchmarks/fixtures/<case_id>/` using only the appropriate direct prompt. Do not use repo-ethics scanner output or MCP tools to create direct baseline outputs.

Helpful commands:

```bash
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline naive
python3 benchmarks/scripts/run_direct_codex_placeholder.py --baseline strong
python3 benchmarks/scripts/score_reports.py
python3 benchmarks/scripts/summarize_results.py
```

The placeholder commands print collection instructions by default. They do not run Codex unless an explicit `--direct-codex-command` template is supplied.

No superiority claim can be made until direct outputs are collected and scored against the same reviewed cases.
