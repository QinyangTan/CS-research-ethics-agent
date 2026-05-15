**Project Summary**

This repository appears to describe a classroom attendance system that identifies students using facial recognition. The implementation imports `face_recognition` and indicates that it computes face embeddings for attendance tracking in [main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/src%202/main.py:1). The data schema stores a `student_id` linked to a `face_embedding` in [schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/data%202/schema.json:1). The README explicitly states that consent, retention, and access controls are not documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1).

**Potential Ethics Issues**

- **Biometric privacy risk:** Face embeddings are biometric identifiers. Even if they are not raw images, they can still be sensitive and difficult or impossible for students to change if compromised. See [schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/data%202/schema.json:1).

- **Student surveillance and coercion:** Attendance tracking in a classroom creates an institutional monitoring context where students may not feel free to refuse participation. This is especially sensitive if students are minors or if attendance affects grades, discipline, funding, or immigration/visa status. See [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1).

- **Missing consent process:** The README directly notes that consent is not documented. For biometric processing, this is a major governance gap. Consent should be informed, specific, revocable, and paired with a non-biometric alternative.

- **No retention or deletion policy:** The README notes that retention is undocumented. Biometric records should have explicit expiration, deletion triggers, and procedures for withdrawal.

- **No access controls documented:** The README also states that access controls are not documented. Linking `student_id` to `face_embedding` creates a sensitive identifiable dataset, so unauthorized access could expose biometric information.

- **Bias and differential error rates:** Face recognition systems can perform unevenly across demographics, lighting conditions, disabilities, religious dress, hairstyles, age groups, and skin tones. False absences could cause academic or disciplinary harm.

- **Lack of accountability and appeal:** The repository does not document how recognition errors are detected, corrected, audited, or appealed.

- **Function creep:** A face attendance system could be repurposed for broader location tracking, behavior monitoring, discipline, or law enforcement requests unless use limits are explicit.

**Suggested Mitigations**

- Add a research ethics protocol covering purpose, population, consent, risks, benefits, and withdrawal.
- Require opt-in consent and provide an equal non-biometric attendance alternative.
- Minimize stored data: avoid retaining face embeddings unless strictly necessary; consider local/on-device matching or ephemeral templates.
- Add encryption at rest and in transit, strict role-based access controls, audit logs, and key management.
- Define a retention policy with automatic deletion after the course, study, or shortest operational period.
- Separate `student_id` from biometric templates using pseudonymous identifiers where possible.
- Conduct demographic performance testing and report false positive/false negative rates across relevant student groups.
- Add a human review and correction process before any attendance penalty is applied.
- Document prohibited secondary uses, especially disciplinary surveillance, location tracking outside attendance, and sharing with third parties.
- Add incident response procedures for biometric data exposure.

**Questions for the Researcher**

1. Are students minors, adults, or a mixed population?
2. Is participation voluntary, and is there a non-biometric attendance option?
3. What exact consent language will students receive?
4. How long are face embeddings retained, and who can delete them?
5. Who has access to the biometric database?
6. Are embeddings encrypted and stored separately from student identities?
7. What happens when the system misidentifies a student or marks them absent incorrectly?
8. Will attendance results affect grades, discipline, funding, or other student outcomes?
9. Has the system been evaluated for demographic bias and classroom-specific conditions?
10. Are there written limits preventing reuse for surveillance beyond attendance?