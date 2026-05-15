# Computer Science Research Ethics Pre-Review

## Project Summary

The repository appears to describe a survey application collecting participant responses with demographic fields. Evidence is limited to [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_survey_app/README.md:1) and [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_survey_app/data/schema.json:1).

The documented schema includes:

- `participant_id`
- `gender`
- `income`

The README states that consent and data access controls are not documented.

## Risk Categories and Evidence

### Human Subjects / Participant Data Risk

The project involves survey participants and demographic data. The README explicitly says “Participants submit survey responses with demographic fields” in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_survey_app/README.md:1).

This suggests the project may involve people as data subjects, but the repo does not provide enough context to determine recruitment methods, study purpose, participant expectations, or review status.

### Privacy and Re-Identification Risk

The schema contains `participant_id`, `gender`, and `income` in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_survey_app/data/schema.json:1).

Even if names are not collected, demographic attributes combined with a participant identifier can increase re-identification risk, especially for small populations or narrowly sampled communities.

### Sensitive Demographic and Socioeconomic Data

The schema collects `gender` and `income`, both of which can be sensitive depending on context. Income in particular can expose socioeconomic status. Gender data may also create risk if options are restrictive, mishandled, or linked to identity.

### Consent and Transparency Gaps

The README states that “Consent and data access controls are not documented” in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_survey_app/README.md:1).

There is no visible consent language, participant information sheet, withdrawal process, data use statement, or explanation of whether responses are anonymous, pseudonymous, or identifiable.

### Data Governance and Access Control Gaps

The repository does not document who can access submitted survey data, how data is stored, retention duration, deletion procedures, encryption, audit logging, or sharing rules.

## Missing Context and Clarification Questions

- What is the research purpose of the survey?
- Who are the participants, and how are they recruited?
- Are participants adults, students, employees, patients, minors, or members of a vulnerable or dependent population?
- Is `participant_id` directly identifying, pseudonymous, randomly generated, or linked to an external identity table?
- What survey responses are collected beyond the schema shown here?
- Is income collected as a broad range, exact value, household income, personal income, or another measure?
- What gender options are offered, and can participants decline to answer?
- What consent language is shown before participation?
- Can participants withdraw or request deletion of their data?
- Who has access to raw survey data?
- Where is data stored, and is it encrypted in transit and at rest?
- How long is data retained?
- Will the dataset be shared publicly, with collaborators, or used in publications?
- Are results reported only in aggregate form?
- What safeguards prevent small-cell disclosure in demographic breakdowns?

## Concrete Mitigations

- Add a participant-facing consent or information document describing purpose, data collected, risks, benefits, voluntary participation, withdrawal, contact information, and data use.
- Minimize demographic collection to fields necessary for the research question.
- Make sensitive demographic fields optional where possible, including “prefer not to answer” choices.
- Replace `participant_id` with a random study ID unless a persistent identifier is strictly needed.
- Store any identity linkage table separately from survey responses, with tighter access controls.
- Define access controls for raw data, including authorized roles and logging.
- Document retention and deletion timelines.
- Use encryption in transit and at rest for survey submissions and stored data.
- Aggregate or suppress small demographic cells before analysis or publication.
- Document whether data will be shared, and under what anonymization or data-use agreement conditions.
- Add a data management plan covering storage, access, retention, sharing, and deletion.
- Include a risk review focused on re-identification from demographic combinations.

## Advisor or Review-Body Discussion Questions

- Is collecting gender and income necessary for the stated research goals?
- Is the participant population likely to make demographic combinations identifiable?
- Does the study need identifiable, pseudonymous, or anonymous data?
- What consent process is appropriate for this survey context?
- What protections are needed if participants are students, employees, minors, or otherwise dependent on the researchers?
- Should raw data access be limited to named researchers?
- Are there publication plans that could expose small groups through demographic subgroup analysis?
- Is a formal institutional or organizational review appropriate for this study context?

## Limitations of This Review

This review is based only on the repository files directly inspected. The repository contains minimal documentation and no application code, deployment configuration, consent materials, survey questions, storage implementation, or access-control implementation.

This is a pre-review risk assessment, not a determination of ethical approval, legal compliance, safety, or whether any specific review process is mandatory.