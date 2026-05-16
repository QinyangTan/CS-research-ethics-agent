# Computer Science Research Ethics Pre-Review

## Project Summary

This repository appears to describe a browser extension telemetry project that collects browsing-related data. The stated data includes URL history, click timestamps, and `user_id` values. The implementation evidence is minimal: one JavaScript file sends `user_id`, `url`, and `timestamp` to a `/collect` endpoint.

Evidence:
- [README.md](benchmarks/fixtures/case_browser_telemetry/README.md:1): says the extension collects URL history, click timestamps, and `user_id` values, with unclear retention and access controls.
- [src/extension.js](benchmarks/fixtures/case_browser_telemetry/src/extension.js:1): posts `{user_id, url, timestamp}` to `/collect`.

## Risk Categories And Evidence

| Risk Category | Evidence | Ethics Concern |
|---|---|---|
| Privacy and sensitive data collection | `url` and URL history are collected; `user_id` is included | Browsing history can reveal health, finances, politics, religion, sexuality, work activity, and other sensitive inferences. A stable user identifier increases re-identification risk. |
| Behavioral surveillance | Click timestamps and URL telemetry are described | Timestamped browsing activity can create detailed behavioral profiles, routines, and productivity or attention patterns. |
| Consent and transparency | No consent flow, participant notice, opt-out, or extension permission rationale is present | Users may not understand the scope, frequency, purpose, or consequences of collection. |
| Data minimization | Raw `url`, `timestamp`, and `user_id` are sent | The repository does not show why raw URLs or stable identifiers are necessary instead of minimized, hashed, aggregated, or locally processed data. |
| Retention and access control | README explicitly says retention and access controls are unclear | Unclear retention and access increase risk of misuse, breach impact, secondary use, and unauthorized access. |
| Security in transit and endpoint handling | `fetch('/collect', ...)` is shown without visible authentication, CSRF protections, encryption assumptions, or server-side handling | The repo does not demonstrate transport guarantees, access authorization, validation, logging controls, or storage protections. |
| Secondary use and scope creep | No research protocol, purpose limitation, or data-use boundaries are present | Browser telemetry can be repurposed for unrelated profiling, monitoring, or commercial analytics. |
| Participant vulnerability and bystander data | URL collection may include pages involving third parties or shared devices | Data may include information about non-participants, household members, coworkers, or people whose information appears in URLs. |

## Missing Context And Clarification Questions

1. What is the research question, and why is browser-level telemetry necessary to answer it?
2. Who are the participants, and are any minors, employees, students, patients, or other dependent populations involved?
3. What exact browser events are collected beyond `url`, `timestamp`, and `user_id`?
4. Are full URLs collected, including query strings, paths, fragments, and possible tokens?
5. Is data collected continuously, only during specific study sessions, or only on selected domains?
6. What notice and consent language is shown before collection begins?
7. Can participants pause, inspect, delete, or export their collected data?
8. How is `user_id` generated, and can it be linked to real identities?
9. What retention period applies, and who can approve deletion or extension of retention?
10. Who has access to raw telemetry, and are access logs maintained?
11. What server receives `/collect`, where is it hosted, and how is the data stored?
12. Will telemetry be shared with collaborators, vendors, public datasets, or future studies?

## Concrete Mitigations

- Collect the minimum necessary data: avoid full URLs where domain-level, category-level, or locally computed features are sufficient.
- Strip query strings, fragments, session IDs, search terms, auth tokens, email addresses, and other high-risk URL components before transmission.
- Replace stable `user_id` values with rotating pseudonymous identifiers where longitudinal linkage is not essential.
- Add explicit consent and in-extension controls for pause, opt-out, deletion request, and data visibility.
- Define a retention schedule before deployment, including deletion timelines for raw and derived data.
- Restrict access to raw telemetry using role-based permissions, audit logs, and documented approval procedures.
- Encrypt data in transit and at rest; document endpoint authentication and server-side validation.
- Prefer local processing or aggregation in the extension before sending data.
- Add a data management plan covering storage location, access, retention, sharing, incident response, and publication handling.
- Exclude sensitive domains or categories by default, such as health, finance, legal, authentication, government, and adult content.
- Provide participants with plain-language examples of what collected URLs may reveal.
- Test the extension to verify it does not collect outside the stated scope.

## Advisor Or Review-Body Discussion Questions

- Is raw browsing telemetry proportionate to the research value, or can the study use lower-risk measurements?
- Should collection be domain-limited, session-limited, or event-limited?
- What consent model is appropriate for persistent browser telemetry?
- How will the team handle incidental sensitive data and non-participant data?
- Who needs access to identifiable or linkable data, and for how long?
- What deletion guarantees can realistically be honored?
- Should an independent security review be completed before deployment?
- What harms could arise if the dataset were breached or misused?
- How will publications avoid exposing individual browsing behavior or rare URL patterns?

## Limitations Of This Review

This review is based only on the directly inspected repository files and does not use scanner output or external repository-ethics tools. The repository contains very little implementation detail: no manifest, server code, consent UI, privacy notice, deployment configuration, storage schema, or study protocol was present. As a result, this is a preliminary ethics risk review, not a final determination about approval, rejection, legality, compliance, safety, or whether any specific review process is mandatory.