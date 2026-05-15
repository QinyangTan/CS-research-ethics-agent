**Project Summary**

This repository appears to be a minimal multi-camera person-tracking demo. The README states that it “tracks people across cameras,” while explicitly noting that consent and deployment limits are not documented: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/README.md:1). The implementation is currently only a stub function, `track_people_across_cameras(frames)`, returning an empty list: [main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_surveillance_tracking/src%202/main.py:1).

**Potential Ethics Issues**

- **Surveillance and privacy risk:** Multi-camera person tracking can enable persistent monitoring of individuals across spaces, creating high privacy risk even if no face recognition is used.
- **Consent gap:** The README directly says consent is not documented, which is a major issue for research involving identifiable or trackable people.
- **Deployment ambiguity:** The README also says deployment limits are not documented, leaving unclear whether the system is intended for lab demos, public spaces, workplaces, campuses, law enforcement, or commercial surveillance.
- **Identifiability and re-identification:** Cross-camera tracking can re-identify people by gait, clothing, location patterns, or trajectory even without names or biometric labels.
- **Misuse potential:** The project could be adapted for covert monitoring, protest surveillance, employee tracking, stalking, or discriminatory enforcement.
- **Bias and disparate impact:** Person tracking systems may perform unevenly across skin tones, body types, clothing, mobility aids, lighting conditions, and camera angles.
- **Data governance missing:** There is no documentation about dataset source, retention period, anonymization, access controls, storage security, or deletion.
- **Accountability missing:** No stated process for audit, human review, error handling, appeal, or incident response if tracking results are wrong or harmful.

**Suggested Mitigations**

- Add a research ethics section documenting intended use, prohibited use, deployment boundaries, and whether the system is only for controlled research environments.
- Require informed consent for any collected footage unless an IRB or equivalent ethics board explicitly approves a waiver.
- Avoid public-space or workplace deployment unless legally reviewed and ethically approved.
- Minimize data: process locally where possible, avoid storing raw video, blur faces/bodies when identity is not required, and retain only aggregate metrics.
- Add access controls, logging, encryption, retention limits, and deletion procedures for any video or tracking outputs.
- Document datasets, collection context, subject consent status, demographics if available, and known performance limitations.
- Evaluate tracking accuracy and failure modes across demographic groups and environmental conditions.
- Add misuse restrictions to the README, especially prohibiting covert surveillance, law-enforcement targeting, immigration enforcement, stalking, and employment discipline without due process.
- Include an ethics review checklist before any real-world data collection or deployment.

**Questions For The Researcher**

1. What is the intended research purpose: algorithm benchmarking, safety analysis, crowd analytics, or operational surveillance?
2. Will the system use real people, synthetic data, public datasets, or newly collected video?
3. If real footage is used, how will consent be obtained and documented?
4. Where are cameras located, and are subjects aware they are being tracked across cameras?
5. Will raw video, embeddings, trajectories, or IDs be stored? For how long?
6. Could the system identify or single out a person over time, even without names?
7. Who can access the footage and tracking outputs?
8. What deployments are explicitly prohibited?
9. Has the project gone through IRB, ethics board, legal, or privacy review?
10. How will bias, false matches, and downstream harms be measured and mitigated?