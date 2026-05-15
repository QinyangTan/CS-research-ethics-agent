# Ethics Pre-Review: Surveillance Tracking Fixture

## Project Summary

The repository appears to describe a minimal multi-camera person-tracking demo. The README states that it “tracks people across cameras” and explicitly notes that “consent and deployment limits are not documented” in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/README.md:1). The implementation is only a stub: [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/src/main.py:1) defines `track_people_across_cameras(frames)` and returns an empty list.

## Risk Categories And Evidence

**Surveillance and persistent tracking risk**

The stated purpose is cross-camera people tracking, which can enable persistent identification or movement reconstruction across physical spaces. Evidence: [README.md:1](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/README.md:1).

**Consent and autonomy risk**

The repository itself says consent is not documented. That is a major missing safeguard for any system observing or tracking people in camera footage. Evidence: [README.md:1](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/README.md:1).

**Deployment-boundary risk**

The README says deployment limits are not documented. Without scope limits, the same demo could be used in sensitive contexts such as workplaces, campuses, public spaces, protests, hospitals, or shelters. Evidence: [README.md:1](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/README.md:1).

**Privacy and re-identification risk**

Even though the code is a stub, the intended function name `track_people_across_cameras` implies linking observations of people across multiple video feeds. That can create sensitive behavioral data, including location, route, association, and time-pattern information. Evidence: [src/main.py:1](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/src/main.py:1).

**Missing data governance**

No files describe data sources, retention, access controls, anonymization, deletion, audit logs, or security handling for camera frames or tracking outputs.

## Missing Context And Clarification Questions

1. What camera footage will be used: synthetic, public benchmark data, volunteer-collected footage, institutional cameras, or public-space surveillance video?
2. Are people in the footage identifiable, and are faces, clothing, gait, or other biometric/behavioral signals used?
3. Were participants notified, and what consent or opt-out mechanism exists?
4. What are the intended and prohibited deployment contexts?
5. Will the system store raw frames, embeddings, track IDs, timestamps, or camera-location metadata?
6. Who can access the footage and tracking results?
7. How long will data and derived tracking records be retained?
8. What evaluation metrics are planned, and do they account for demographic performance differences or false identity linking harms?
9. Is the goal purely research benchmarking, live deployment, security monitoring, commercial analytics, or something else?
10. What misuse scenarios have been considered, especially stalking, worker monitoring, protest monitoring, or discriminatory enforcement?

## Concrete Mitigations

- Add a clear research-purpose statement and explicit non-deployment boundary.
- Document permitted datasets and prohibit use on non-consenting or sensitive populations unless separately reviewed.
- Use synthetic, staged, or consented datasets where possible.
- Minimize data collection: avoid storing raw video unless necessary.
- If tracking outputs are stored, separate them from direct identifiers and limit retention.
- Add access controls, audit logging, encryption-at-rest, and deletion procedures for any video or derived records.
- Define prohibited use cases, including covert monitoring, law-enforcement targeting, employment discipline, protest surveillance, and tracking in sensitive facilities.
- Add a consent and notice plan for any newly collected footage.
- Include a model card or datasheet covering data provenance, intended use, known limitations, and failure modes.
- Evaluate false matches and missed matches, including whether errors disproportionately affect particular groups or environments.
- Require an internal review checkpoint before connecting the code to live cameras or real-world surveillance infrastructure.

## Advisor Or Review-Body Discussion Questions

- Is cross-camera person tracking necessary for the research question, or could a less privacy-invasive method answer it?
- What human-subjects, privacy, or institutional review process is appropriate for the actual data source and deployment context?
- What contexts should be explicitly out of scope?
- How will participants or bystanders be informed, and what practical opt-out exists?
- What would happen if the system incorrectly links two people across cameras?
- Who benefits from the system, and who bears the risk?
- What safeguards prevent repurposing the demo into operational surveillance?
- Should publication or release exclude trained weights, deployment scripts, or live-camera integration code?

## Limitations Of This Review

This review is based only on direct inspection of the repository files. The repository contains almost no implementation, no dataset, no experiment description, and no governance documentation. Because of that, the review identifies plausible risks from the stated project purpose, but it cannot determine actual data practices, deployment plans, legal status, institutional obligations, or whether any external review is required.