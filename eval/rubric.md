# Evaluation Rubric

This lightweight benchmark checks whether the scanner finds expected categories in the example repositories and avoids explicitly absent categories.

- Recall: expected categories present in generated findings.
- False positives: expected absent categories that appear in generated findings.
- Severity guard: harmless sorting visualizer should not produce high or critical findings.

This is not a complete academic benchmark. It is intended to make scanner behavior auditable and easier to improve.

