# Computer Science Research Ethics Pre-Review

## Project Summary

The repository appears to describe a cybersecurity-related project. The only README statement says: “This is not a toy and it is a vulnerability scanner for a closed lab” ([README.md](benchmarks/fixtures/case_security_contrastive/README.md:1)). The implementation is minimal: `scan_port(host, port)` always returns `False` ([src/main.py](benchmarks/fixtures/case_security_contrastive/src/main.py:1)).

Based on direct file inspection, the repository contains a stated intent to build or represent a vulnerability scanner, but does not currently include functional scanning logic.

## Risk Categories And Evidence

### Dual-Use Cybersecurity Risk

Evidence: The README identifies the project as a “vulnerability scanner” ([README.md:1](benchmarks/fixtures/case_security_contrastive/README.md:1)).

Risk: Vulnerability scanners can support legitimate defensive security work, but can also be misused for unauthorized reconnaissance, probing, or target enumeration. The current code does not implement this behavior, but the stated project purpose is dual-use.

### Authorization And Scope Risk

Evidence: The README claims the scanner is for a “closed lab” ([README.md:1](benchmarks/fixtures/case_security_contrastive/README.md:1)).

Risk: “Closed lab” is not independently evidenced in the repository. There is no documented authorization boundary, target list, lab topology, consent statement, rate limits, or prohibition on scanning external hosts.

### Operational Safety Risk

Evidence: No safeguards are present in `src/main.py`; the function is a stub returning `False` ([src/main.py:1](benchmarks/fixtures/case_security_contrastive/src/main.py:1)).

Risk: If expanded into a real scanner, the project could create network load, trigger alerts, disrupt services, or accidentally scan systems outside the intended environment unless controls are added.

### Research Validity And Misrepresentation Risk

Evidence: The README says the project is “not a toy” and is a vulnerability scanner, while the only implementation is nonfunctional ([README.md:1](benchmarks/fixtures/case_security_contrastive/README.md:1), [src/main.py:1](benchmarks/fixtures/case_security_contrastive/src/main.py:1)).

Risk: There is a mismatch between stated capability and code behavior. This may affect reproducibility, evaluation integrity, and reviewer understanding of the actual research artifact.

## Missing Context And Clarification Questions

- What is the research question or educational purpose of the scanner?
- What systems are in the “closed lab,” and who owns or administers them?
- Is there written authorization for scanning those systems?
- Will the scanner ever run against public IPs, campus networks, third-party services, or student-owned devices?
- What data will be collected: open ports only, banners, service versions, vulnerabilities, credentials, logs, or screenshots?
- Will any discovered vulnerabilities be disclosed, stored, published, or shared?
- Are there rate limits, allowlists, dry-run modes, and safeguards against accidental external scanning?
- Who can run the tool, and are there access controls or audit logs?
- Is this intended for coursework, research evaluation, defensive operations, or publication?

## Concrete Mitigations

- Add an explicit scope document defining permitted hosts, networks, owners, dates, and authorization.
- Require an allowlist of lab IPs or hostnames before scanning can run.
- Add safeguards that reject private/public ranges not included in the approved lab configuration.
- Implement rate limiting, timeouts, and concurrency limits.
- Add logging that records who initiated scans, when, against which approved targets.
- Include a dry-run mode that prints intended targets without sending network probes.
- Document data handling: what is collected, retention period, access permissions, and deletion process.
- Add a responsible disclosure workflow for any vulnerabilities found.
- Avoid publishing exploit code, credential capture, stealth behavior, or evasion features unless specifically justified and reviewed.
- Align documentation with actual behavior so claims about scanner capability match the implemented code.

## Advisor Or Review-Body Discussion Questions

- Is the project limited to defensive testing within a controlled lab environment?
- What evidence demonstrates authorization for every target system?
- Could this tool or its documentation enable unauthorized scanning if copied or modified?
- Are the planned scanning methods proportionate to the research or teaching objective?
- What safeguards prevent accidental scanning outside the lab?
- What happens if the tool identifies a real vulnerability?
- Who has access to scan results, and could those results create security exposure?
- Does the project need additional institutional, departmental, or security-office review before deployment?

## Limitations Of This Review

This review is based only on direct inspection of the repository files present: `README.md` and `src/main.py`. The code is a stub, so risk assessment relies partly on the stated project intent rather than observed functionality. I did not use external scanners, repo-ethics MCP tools, or scanner output. This is a pre-review for ethics discussion and does not determine final approval, rejection, legal status, compliance status, safety, or whether any specific review process is mandatory.