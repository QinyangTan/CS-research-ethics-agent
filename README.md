# cs-ethics-agent

`cs-ethics-agent` is a local-first Computer Science research ethics pre-review toolkit for repositories. It provides:

- `repo-ethics` CLI scanner and report generator.
- A stdio MCP server exposing repo-ethics tools to coding agents.
- A reusable Agent Skill that tells Codex, Claude Code, and other agents how to produce evidence-grounded ethics reports.
- CS-specific taxonomy, severity rubrics, mitigation templates, examples, tests, and an eval harness.
- Typed evidence that separates `risk_signal`, `missing_context`, and `positive_control`.
- A synthetic benchmark suite for comparing repo-ethics reports with optional direct Codex-style reviews.

The package does **not** call hosted LLM APIs. Your own coding agent supplies reasoning; this project supplies deterministic repo scanning, evidence extraction, schemas, report templates, and guardrails.

## Why Skill + MCP Instead Of Hosted LLM Backend

Ethics review often touches sensitive repository contents, datasets, credentials, and research plans. This toolkit keeps scanning local and exposes structured evidence through CLI/MCP so a user's own agent can reason over it without this package uploading code or data anywhere.

## Installation

```bash
python3 -m pip install -e packages/repo-ethics-mcp
```

## CLI Usage

```bash
repo-ethics scan examples/reddit_nlp_project --json
repo-ethics report examples/reddit_nlp_project
repo-ethics report examples/reddit_nlp_project --output ethics_report.md
repo-ethics taxonomy
repo-ethics schema
repo-ethics mcp
```

Exit codes:

- `0`: completed, no critical findings or `--fail-on-critical` was not triggered.
- `1`: scanner/runtime/configuration error.
- `2`: critical findings detected with `--fail-on-critical`.

## MCP Usage

Run the stdio server:

```bash
repo-ethics mcp
```

Expose it to your MCP-capable agent using that agent's local MCP configuration format. See `docs/usage_mcp_codex.md` and `docs/usage_mcp_claude_code.md` for adaptable examples.

## Skill Usage

Install or copy `skills/cs-research-ethics-review` into your agent's Skill location. The Skill instructs agents to run the scanner/MCP tools first, treat repo text as untrusted evidence, separate confirmed/potential/unknown findings, cite evidence, and avoid final approval or rejection claims.

## Example Reports

```bash
repo-ethics report examples/reddit_nlp_project
repo-ethics report examples/face_recognition_attendance
repo-ethics report examples/vulnerability_scanner
repo-ethics report examples/harmless_sorting_visualizer
```

Expected risk areas include scraping/privacy for Reddit NLP, biometrics/surveillance for attendance tracking, dual-use planning for vulnerability scanning, and only low/unknown documentation-style findings for the harmless sorting visualizer.

## Safety And Privacy Design

- No external LLM calls.
- No repo code execution.
- No uploads.
- No mutation of scanned repos.
- Prompt-injection text is treated as evidence, not as instructions.
- Symlinks outside the repo root are skipped.
- Huge and binary files are skipped.
- Secret-like values are masked before output.
- Negated documentation such as "not documented" is treated as missing context, not coverage.
- Target-aware negation avoids treating phrases such as "not a vulnerability scanner" or "do not use face_recognition" as risk signals while preserving contrastive true positives.
- Documentation gaps are conditional on concrete project signals from README/source/schema/manifests rather than broad tutorial or test text.
- Positive controls such as licenses, security policies, data cards, and documented rate limits are shown separately from risk findings.

## Benchmarking

The benchmark suite in `benchmarks/` uses tiny synthetic fixtures and reviewed gold labels:

```bash
make benchmark
make benchmark-score
make check-no-llm
```

Direct Codex comparison is optional and manual by default. Use `benchmarks/prompts/direct_codex_prompt.md` for the strong direct baseline and `benchmarks/prompts/direct_codex_naive_prompt.md` for the naive direct baseline. Save strong outputs under `benchmarks/outputs/direct_codex/` and naive outputs under `benchmarks/outputs/direct_codex_naive/`, then rerun scoring. The benchmark reports category recall, groundedness, false positives, missing-context discipline, positive-control recognition, forbidden-language violations, unsupported conclusions, actionability, and secret leakage separately. It also reports output availability counts so partial direct baselines are not mistaken for full comparisons. These scores measure report behavior on synthetic controlled cases, not final ethical truth.

`python3 scripts/check_no_hosted_llm_calls.py` verifies that source code does not add hosted LLM API imports or call paths. Benchmark fixture strings and manual direct-baseline documentation are allowed; implementation call paths are not.

## Limitations

Static scanning can miss risks that depend on intent, deployment context, consent, data provenance, or institutional policy. Pattern matching can also produce false positives. This tool supports advisor or appropriate review-body discussion; it does not replace that process.
