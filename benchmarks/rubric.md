# Benchmark Rubric

Category recall gives credit when a report identifies the expected issue. Evidence groundedness is separate and requires repository-specific file or line evidence.

Missing context should be framed as uncertainty or questions. Reports are penalized when they convert missing documentation into unsupported conclusions.

Positive controls, such as rate limits, data cards, model cards, licenses, security policies, and ethics notes, should be recognized without erasing the underlying risk signal.

Extra missing-context and positive-control categories are tracked separately from risk false positives. They are diagnostic: they may reflect useful caution or a scanner/baseline adding noisy categories beyond the reviewed gold labels.

Forbidden and overclaiming language is counted explicitly. Reports should not claim final ethical status, legal status, compliance, safety, or mandatory IRB approval.

Direct Markdown baselines should use clear sections for risks, evidence, missing context, safeguards, mitigations, and questions. Section-aware scoring avoids crediting a missing-context or positive-control category merely because a marker appears elsewhere in the report.

Must-mention and must-not-mention fields are auxiliary checks. They support regression analysis but are not blended into a final ethics score.

Scoring mode counts are reported for each system. Structured JSON is expected for repo_ethics; direct Markdown should ideally be sectioned Markdown rather than fallback Markdown so categories are credited from the right report sections.

Underperformance analysis compares overlapping case rows metric by metric. It is a diagnostic aid for general improvements and does not prove final ethical correctness.
