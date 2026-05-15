# Evaluation Rubric

This lightweight benchmark checks whether the scanner finds expected categories in the example repositories and avoids explicitly absent categories.

- Recall: expected categories present in generated findings.
- False positives: expected absent categories that appear in risk findings or `risk_signal` evidence.
- Missing context: expected categories present as `missing_context` evidence.
- Positive controls: helpful safeguards reported separately and never counted as false positives.
- Severity guard: harmless sorting visualizer should not produce high or critical findings.

This is not a complete academic benchmark. It is intended to make scanner behavior auditable and easier to improve.
