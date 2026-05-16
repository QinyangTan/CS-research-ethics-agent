# Report Language Policy

Forbidden wording:

- This is ethical.
- This is unethical.
- This violates IRB.
- This requires IRB approval.
- This is illegal.
- This is compliant.
- This is safe.

Preferred wording:

- This may raise a potential risk.
- This should be reviewed with an advisor or appropriate review body.
- The available repository evidence is insufficient to determine...
- This depends on missing context.
- Positive controls were detected, but they do not remove the need to review remaining risk signals and missing context.

Evidence type policy:

- Use `risk_signal` evidence for confirmed and potential findings.
- Treat `missing_context` as clarification questions.
- Do not present `positive_control` evidence as a risk.
- Do not count negated documentation as coverage.
- Preserve target-aware nuance: unrelated negation should not hide a later true risk signal.
- Benchmark summaries should say they measure report behavior on synthetic controlled cases, not final ethical truth.
- Benchmark comparisons should name the specific metric being compared and should note when direct-baseline output coverage is partial.
- Path-only sanitization of direct baseline outputs is allowed; changing risk claims, evidence descriptions, mitigations, or conclusions after generation is not.
