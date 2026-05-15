# Benchmark Methodology

The benchmark measures report quality and evidence grounding, not final ethical correctness.

Cases are synthetic and intentionally tiny so failures are interpretable. Fixture generation is separate from gold labels: `generate_fixtures.py` creates repositories only, while `gold/*.json` labels are manually reviewed metadata. Starter labels must use `review_status: "needs_human_review"` and are excluded from official scoring.

Metrics are reported separately:

- category recall
- expected-absent false positives
- evidence groundedness
- missing-context recall and discipline
- positive-control recognition
- unexpected missing-context count
- unexpected positive-control count
- forbidden-language violations
- unsupported conclusion count
- secret leakage
- actionability

Unexpected missing-context and positive-control counts measure extra caution/noise beyond the reviewed labels. They are not counted as risk false positives. Reviewers should inspect them separately from category recall and expected-absent false positives because an extra unknown or safeguard category may be useful in one case and distracting in another.

Direct Codex scoring uses `category_aliases.yaml` so natural wording can receive credit without requiring exact taxonomy IDs.

Some aliases intentionally overlap. For example, responsible-disclosure phrases may count toward both `security_dual_use` and `vulnerability_disclosure` when a reviewed gold label expects both. This reflects that disclosure planning can be both dual-use context and disclosure-specific evidence; scores should be interpreted per category rather than as mutually exclusive classes.

Direct Markdown scoring is section-aware. Risk/evidence sections are used for risk category recall, missing-context/question sections are used for missing-context recall, and safeguard/control sections are used for positive-control recognition. If a direct report has no recognizable sections, fallback scoring is more conservative and records `markdown_scoring_mode: fallback_markdown`.

Scoring reports output availability counts for each system. Direct baselines are manual and may cover fewer cases than repo-ethics, so aggregate metrics should be compared only with that coverage in mind.
