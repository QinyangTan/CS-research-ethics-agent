# Ethics Pre-Review Report

## Project Summary

The repository appears to describe a class-project data store for student contact records. The README states: “Stores student contact records for a class project” and notes that privacy and retention are undocumented ([README.md](benchmarks/fixtures/case_pii_student_contacts/README.md:1)).

The only schema file defines three fields: `student_id`, `email`, and `location` ([data/schema.json](benchmarks/fixtures/case_pii_student_contacts/data/schema.json:1)).

## Risk Categories and Evidence

- **Personally identifiable information**
  - The schema includes `student_id` and `email`, both of which can identify or link to individual students.
  - Evidence: [data/schema.json](benchmarks/fixtures/case_pii_student_contacts/data/schema.json:1)

- **Location privacy**
  - The schema includes `location`, which may be sensitive depending on granularity, collection context, and whether it reflects home, classroom, device, or inferred location.
  - Evidence: [data/schema.json](benchmarks/fixtures/case_pii_student_contacts/data/schema.json:1)

- **Missing privacy and retention controls**
  - The README explicitly says privacy and retention are not documented.
  - Evidence: [README.md](benchmarks/fixtures/case_pii_student_contacts/README.md:1)

- **Student-subject vulnerability and power dynamics**
  - Because the records are for students in a class project, there may be consent, voluntariness, grading-pressure, or instructor-student power-differential concerns. The repo does not document collection context or safeguards.

- **Access control and data minimization gaps**
  - No files describe who can access the records, why each field is necessary, whether data are minimized, or whether contact/location fields are optional.

## Missing Context and Clarification Questions

- What is the purpose of collecting `student_id`, `email`, and `location`?
- Is `location` coarse or precise? Is it self-reported, inferred, device-derived, or administrative?
- Are these real student records, synthetic examples, or a schema only?
- Who can access the data, and under what authorization model?
- Is participation voluntary, and is there any effect on grades or class standing?
- What notice or consent process is used?
- How long are records retained, and how are they deleted?
- Are students able to inspect, correct, or remove their records?
- Is the data shared outside the class, published, reused, or used for model training?

## Concrete Mitigations

- Document the data purpose, collection method, retention period, deletion process, and access policy.
- Minimize fields: remove `location` unless clearly necessary; consider coarse categories rather than precise locations.
- Replace direct identifiers with pseudonymous IDs where possible; store email separately only if operationally required.
- Add a consent or notice document explaining what is collected, why, who can access it, and how long it is kept.
- Add safeguards for class power dynamics, such as alternative participation options and no grading penalty for nonparticipation.
- Define access control expectations, including least-privilege access and no public commits of real records.
- Add test or fixture guidance requiring synthetic data only.
- Add a data deletion and incident-response procedure.

## Advisor or Review-Body Discussion Questions

- Is this project collecting data from students as research subjects, course administration, or software testing?
- Does the class context create coercion or perceived coercion?
- Is `location` essential to the research or educational objective?
- Could the project achieve its goals with synthetic, anonymized, or aggregate data?
- What review, if any, is appropriate before collecting real student contact/location data?
- What commitments should be made to students about retention, reuse, and deletion?

## Limitations of This Review

This review is based only on the visible repository files. I found no implementation code, sample records, access-control configuration, consent materials, or deployment documentation. The review therefore identifies ethics risks and missing safeguards, but does not determine legal compliance, institutional approval status, final ethical approval, final rejection, or whether any specific review process is mandatory.