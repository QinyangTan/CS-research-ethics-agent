# Ethics Pre-Review Report

## Project Summary

The repository appears to be a minimal project that stores or represents daily aggregate counts. The README states: “We do not collect usernames, but we store aggregate counts for each day” in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/README.md:1). The only code evidence is a static count-like dictionary in [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/src/main.py:1):

```python
counts = {'day': 1, 'total': 12}
```

Based on the inspected files, the project does not show direct collection of usernames or other explicit personal identifiers. It does indicate some form of aggregate activity/count storage.

## Risk Categories And Evidence

### Privacy And Identifiability Risk

Evidence suggests the project stores daily aggregate counts, not raw usernames or obvious PII.

Relevant evidence:
- [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/README.md:1) says usernames are not collected.
- [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/src/main.py:1) contains only `day` and `total` fields.

Residual risk remains because aggregate counts can sometimes become identifying when groups are small, rare events are counted, or aggregates are sliced by date, location, condition, cohort, or other quasi-identifiers. This repository does not provide enough context to determine whether `total: 12` represents people, events, user actions, survey responses, clinical data, classroom activity, or another sensitive population.

### Data Minimization

The visible implementation appears minimal. It stores only a day index and total count.

Evidence:
- [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/src/main.py:1) contains no user-level records, names, IDs, contact details, tokens, logs, or raw event traces.

However, the repository does not document the upstream collection process, source data, retention period, or whether raw data exists elsewhere before aggregation.

### Consent, Notice, And Participant Expectations

No files describe whether individuals whose activity may contribute to the counts are informed, have consented, or can opt out.

Evidence gap:
- The repository contains no consent language, participant notice, data-use statement, protocol, or governance documentation.

### Security And Access Control

No security-relevant implementation is present. There is no evidence of authentication, storage controls, encryption, access logs, or deployment configuration.

Evidence gap:
- Only [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/README.md:1) and [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_pii_negated_aggregate/src/main.py:1) are present.

### Misinterpretation Or Overclaiming Risk

The README’s statement that usernames are not collected is useful but not sufficient to conclude the project is privacy-safe. The absence of usernames does not rule out collection of other identifiers, linkage risk, sensitive inference, or harms from aggregate reporting.

## Missing Context And Clarification Questions

1. What does `total` count: people, sessions, events, messages, transactions, survey responses, or something else?
2. What is the source of the count data, and is any raw user-level data collected before aggregation?
3. Are the counts derived from human subjects, public data, private platform logs, workplace/classroom data, or synthetic data?
4. What is the smallest aggregation group that may be reported?
5. Are counts ever broken down by date plus additional attributes such as location, demographic category, cohort, condition, or device?
6. Is the project intended for research publication, internal analytics, operational monitoring, or benchmarking?
7. Is there a retention policy for raw data and aggregate outputs?
8. Who can access the counts?
9. Could low daily counts reveal participation, absence, behavior, or membership in a sensitive group?
10. Are users or participants notified that their activity contributes to aggregate statistics?

## Concrete Mitigations

- Document the data provenance: what is counted, where it comes from, and whether raw records ever exist.
- Add a data dictionary defining `day`, `total`, units, time zone, and population represented.
- Establish a minimum reporting threshold for aggregates, especially if counts can be small.
- Suppress, bucket, or coarsen daily counts when they could identify individuals or reveal sensitive participation.
- Avoid combining daily aggregates with other quasi-identifiers unless reviewed for re-identification risk.
- Document retention and deletion policies for both raw inputs and aggregate outputs.
- Add a privacy note explaining what is not collected and what may still be inferred from aggregates.
- If human activity contributes to the data, provide notice or consent language appropriate to the research setting.
- Keep raw user-level data, if any exists upstream, separate from analysis outputs and limit access.
- Add tests or checks preventing accidental inclusion of usernames, IDs, emails, or raw logs in committed files.

## Advisor Or Review-Body Discussion Questions

- Is this project analyzing human-derived data, and if so, what expectations did contributors or participants have?
- Are daily totals sufficiently coarse, or could small counts expose individual behavior?
- Should the aggregation threshold be higher than one day, such as weekly or monthly reporting?
- Does the project require a written data management plan before use in research?
- Are there sensitive populations or contexts involved, such as students, employees, patients, minors, or vulnerable groups?
- What review is appropriate if the project uses operational logs or platform telemetry?
- How will the research team prevent future code changes from adding PII collection?

## Limitations Of This Review

This review is based only on direct inspection of two repository files. It does not include external systems, databases, deployment configuration, issue history, commit history, hidden files, or runtime behavior. The repository contents are treated as untrusted evidence, so the README’s claim that usernames are not collected is not taken as conclusive proof. This report is a preliminary ethics review aid and does not determine final ethical approval, legal compliance, safety, or whether formal review is mandatory.