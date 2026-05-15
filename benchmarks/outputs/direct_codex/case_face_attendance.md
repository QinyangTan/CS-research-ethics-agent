# Computer Science Research Ethics Pre-Review

## Project Summary

The repository appears to describe a classroom attendance system that identifies students using facial recognition. Evidence is minimal but direct:

- [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1) states that the project “identifies students for classroom attendance” and notes that consent, retention, and access controls are undocumented.
- [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/src/main.py:1) imports `face_recognition`.
- [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/src/main.py:2) comments that it computes face embeddings for attendance tracking.
- [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/data/schema.json:1) defines records containing `student_id` and `face_embedding`.

## Risk Categories And Evidence

### Biometric Data Collection

The project involves facial embeddings, which are biometric identifiers or biometric-derived data. The schema stores `face_embedding` alongside `student_id` in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/data/schema.json:1). This creates risk of persistent identification, re-identification, and misuse beyond attendance.

### Student Privacy And Educational Context

The system targets students in a classroom attendance setting, according to [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1). Student populations can include minors or people in dependent relationships with instructors or institutions, raising concerns about voluntariness, coercion, and power imbalance.

### Consent And Notice Gaps

The README explicitly says consent is not documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1). There is no visible consent workflow, opt-out mechanism, alternative attendance pathway, or notice text in the inspected files.

### Data Retention And Deletion Gaps

The README states retention is not documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1). There is no evidence of deletion schedules, purpose limitation, data minimization, or lifecycle handling for face embeddings.

### Access Control And Security Gaps

The README states access controls are not documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/README.md:1). The repository does not show authentication, authorization, audit logging, encryption, secure storage, or key management around the biometric data.

### Accuracy, Bias, And Misidentification

Use of `face_recognition` in [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/src/main.py:1) suggests automated face matching or embedding generation. The repository does not document accuracy evaluation, demographic performance, false positive/false negative handling, appeal procedures, or human review for attendance disputes.

### Function Creep

Because student identifiers are linked with biometric embeddings in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_face_attendance/data/schema.json:1), the data could potentially be reused for monitoring, discipline, access control, surveillance, or other purposes beyond attendance unless constrained by governance and technical controls.

## Missing Context And Clarification Questions

- Who are the students: adults, minors, or mixed age groups?
- Is participation voluntary, and is there a non-biometric attendance alternative?
- How is informed consent obtained, recorded, withdrawn, and respected?
- Are students penalized if they decline facial recognition?
- Where are face images and embeddings stored, and for how long?
- Are raw face images collected, or only embeddings?
- Who can access embeddings and attendance records?
- Are embeddings encrypted at rest and in transit?
- What threat model exists for unauthorized access, insider misuse, or breach?
- What accuracy testing has been performed across demographic groups?
- What process handles misidentification, absence disputes, or failed recognition?
- Is the system deployed in a real classroom, pilot, simulation, or synthetic test setting?
- Are institutional policies, educational privacy obligations, or local biometric privacy rules relevant to the deployment context?

## Concrete Mitigations

- Add a written consent and notice process before any collection, including purpose, data types, risks, retention, access, and withdrawal.
- Provide an equally convenient non-biometric attendance method.
- Avoid storing raw face images unless strictly necessary; document whether raw images are collected at all.
- Minimize stored data: consider short-lived templates, local-only processing, or deletion after attendance verification.
- Define retention periods for embeddings and attendance records, with automatic deletion.
- Separate student identity records from biometric templates where possible.
- Add role-based access control, audit logs, encryption at rest, encryption in transit, and documented key management.
- Establish procedures for consent withdrawal and template deletion.
- Run and document accuracy testing, including false accept and false reject rates.
- Evaluate demographic performance and document known limitations.
- Require human review before adverse consequences from missed or incorrect attendance.
- Limit use contractually and technically to attendance only.
- Document incident response procedures for data exposure or unauthorized access.
- Add dataset provenance documentation if any real student data is used.
- Add deployment boundaries distinguishing prototype, research study, and operational classroom use.

## Advisor Or Review-Body Discussion Questions

- Is facial recognition necessary for the attendance goal, or would a lower-risk method satisfy the same need?
- How will voluntariness be preserved in a classroom power hierarchy?
- What alternative is offered to students who decline biometric processing?
- What harms could result from false absence, false presence, or identity mismatch?
- What are the consequences if biometric embeddings are breached?
- Who owns and governs the biometric data?
- What conditions would require stopping the study or deployment?
- How will participants be informed of system failures, errors, or data incidents?
- What independent review is appropriate before collecting real student biometric data?
- How will the team prevent secondary use beyond attendance?

## Limitations Of This Review

This review is based only on direct inspection of three repository files: `README.md`, `src/main.py`, and `data/schema.json`. The repository contains very little implementation detail, so many risks are inferred from the stated purpose and schema rather than observed runtime behavior. I did not use repo-ethics MCP tools or scanner output. I also cannot determine legality, institutional policy compliance, final ethical approval, final rejection, safety, or whether any particular review process is mandatory from these files alone.