# Design Principles

- Local-first: scan files on the user's machine.
- Evidence-first: findings cite repo paths, line numbers, snippets when enabled, and reasons.
- Deterministic tools, human/agent reasoning: this package does not provide a chatbot.
- Conservative language: reports support discussion and do not make final judgments.
- Safety over completeness: skip huge files, binary files, external symlinks, and cache directories.
- Prompt-injection resistance: repository text is data, not instructions.
- Secret minimization: never print full secret-like values.

