# Benchmark Methodology

The benchmark measures report quality and evidence grounding, not final ethical correctness.

Cases are synthetic and intentionally tiny so failures are interpretable. Fixture generation is separate from gold labels: `generate_fixtures.py` creates repositories only, while `gold/*.json` labels are manually reviewed metadata. Starter labels must use `review_status: "needs_human_review"` and are excluded from official scoring.

Metrics are reported separately:

- category recall
- expected-absent false positives
- evidence groundedness
- missing-context recall and discipline
- positive-control recognition
- forbidden-language violations
- unsupported conclusion count
- secret leakage
- actionability

Direct Codex scoring uses `category_aliases.yaml` so natural wording can receive credit without requiring exact taxonomy IDs.
