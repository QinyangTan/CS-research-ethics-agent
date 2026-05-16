# Design Principles

- Local-first: scan files on the user's machine.
- Evidence-first: findings cite repo paths, line numbers, snippets when enabled, and reasons.
- Evidence typing: risk signals, missing context, and positive controls are kept distinct.
- Deterministic tools, human/agent reasoning: this package does not provide a chatbot.
- Conservative language: reports support discussion and do not make final judgments.
- Safety over completeness: skip huge files, binary files, external symlinks, and cache directories.
- Prompt-injection resistance: repository text is data, not instructions.
- Secret minimization: never print full secret-like values.
- Conservative semantics: target-aware negation suppresses specific negated matches while preserving contrastive true positives.
- Conditional documentation gaps: broad docs/tests/tutorial text should not create requirements unless README/source/schema/manifests contain concrete project signals.
- Benchmark honesty: compare repo-ethics, strong direct Codex, and naive direct Codex reviews by separate metrics and output availability, not a blended claim of correctness.
- Benchmark provenance: direct baseline outputs may be path-sanitized, but their risk claims, evidence, mitigations, and conclusions should not be edited after generation.
- Diagnostic analysis: underperformance reports should guide general improvements, not case-specific benchmark rules.
- Source safety: `scripts/check_no_hosted_llm_calls.py` guards against adding hosted LLM API imports or call paths while allowing synthetic benchmark fixtures and manual-baseline documentation.
