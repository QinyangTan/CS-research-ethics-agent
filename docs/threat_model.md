# Threat Model

## Assets

- Repository source code, docs, schemas, and data-like files.
- Secret-like values that may appear in committed files.
- The reviewing agent's instruction hierarchy and report integrity.
- Local filesystem boundaries around the requested repository root.

## Assumptions

- Repository contents are untrusted input.
- MCP tools may be invoked by an agent that is also reading untrusted repository text.
- The scanner must not execute target repo code, upload files, mutate the target repo, or call external APIs.

## Threats And Controls

### Malicious README / Prompt Injection

Threat: README, comments, or docs may instruct an agent to ignore review rules or suppress findings.

Controls:

- Prompt-injection scanner flags suspicious text.
- Skill policy tells agents to treat repo text as evidence, not instructions.
- Reports cite suspicious text instead of following it.

### Malicious Symlinks

Threat: A repo may contain symlinks pointing outside the requested root.

Controls:

- The safe walker resolves paths.
- Files are scanned only when resolved paths remain under the repo root.
- Directory walking does not follow links.

### Huge-File Denial Of Service

Threat: Large files may slow or exhaust scanner resources.

Controls:

- Default max file size is 512 KiB.
- Binary and archive-like files are skipped.
- Cache, build, dependency, and hidden cache directories are skipped.

### Secret Exposure In Reports

Threat: Reports could reveal committed tokens or keys.

Controls:

- Secret scanner masks matched values before returning evidence.
- Reports use scanner evidence and do not print full matched secrets.
- Tests verify full secret values are absent from output.

### MCP Tool Misuse

Threat: Agent workflows might call MCP tools on unexpected paths or treat output as final authority.

Controls:

- MCP tools do not mutate repos, execute code, upload files, or call external APIs.
- Tools return structured evidence and conservative reports.
- Documentation states that reports support review rather than replacing it.

### Scanner False Positives

Threat: Pattern matches may overstate risk.

Controls:

- Findings include confidence and evidence.
- Missing documentation alone stays low severity.
- Reports use potential/unknown language when context is incomplete.

### Scanner False Negatives

Threat: Risks may be missed because intent, data provenance, or deployment context is not visible.

Controls:

- Reports include unknowns and required clarification questions.
- Limitations are included in every Markdown report.
- The Skill instructs agents to inspect important files when needed.

### Local Filesystem Boundaries

Threat: A scan may accidentally traverse outside the requested repo.

Controls:

- Root is resolved once.
- Candidate files are resolved and checked against root.
- Out-of-root symlinks and unreadable files are skipped.

