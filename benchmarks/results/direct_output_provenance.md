# Direct Output Provenance

Direct baseline outputs are Markdown reviews generated for the synthetic benchmark fixtures using:

- Strong direct prompt: `benchmarks/prompts/direct_codex_prompt.md`
- Naive direct prompt: `benchmarks/prompts/direct_codex_naive_prompt.md`

Outputs are stored in:

- `benchmarks/outputs/direct_codex/<case_id>.md`
- `benchmarks/outputs/direct_codex_naive/<case_id>.md`

Direct outputs should be generated without using repo_ethics outputs, MCP scanner outputs, gold labels, or previous score results. The direct baseline is meant to reflect direct repository review from the prompt and fixture only.

Path-only sanitization is allowed after generation to remove local absolute repository prefixes from Markdown or JSON benchmark artifacts. Editing risk claims, adding evidence, changing mitigations, or changing conclusions is not allowed after baseline generation.

The current benchmark expects complete coverage for reviewed cases before treating direct comparisons as complete. Coverage is recorded in `benchmarks/results/results.json` and summarized in `benchmarks/results/direct_comparison_report.md`.

Limitations:

- Direct outputs are model-generated Markdown and can vary by prompt, model, and local tool environment.
- Direct Markdown scoring is heuristic and depends on section detection and category aliases.
- Synthetic benchmark results do not prove final ethical correctness.
- Results should be interpreted as report-quality and evidence-grounding diagnostics, not as a replacement for expert review.
