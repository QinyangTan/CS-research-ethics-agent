# Limitations

- Static pattern scanning can miss contextual risks.
- Pattern scanning can produce false positives.
- Missing documentation does not prove a risk exists.
- Negation handling uses transparent clause-level and target-adjacent heuristics. It improves common cases but is not full natural-language understanding.
- Documentation requirements are inferred from likely project signal sources, so unusual repositories may need manual review of docs that the scanner treats as coverage rather than signal.
- The benchmark is synthetic and intentionally tiny. It supports regression testing and comparison of report discipline, but it does not prove final ethical correctness.
- Direct-Codex baseline outputs are manually collected and may cover only a subset of benchmark cases. Use output availability and per-metric results before interpreting comparisons.
- Section-aware Markdown scoring is a heuristic for direct outputs. `fallback_markdown` rows should be interpreted more cautiously than `sectioned_markdown` rows.
- The tool cannot determine consent, institutional policy, or deployment facts from code alone.
- The tool does not execute code, inspect remote services, or call external APIs.
- Reports should be reviewed with an advisor or appropriate review body when the project affects people, sensitive data, public release, security research, biometrics, or deployment.
