# Ethics Pre-Review Report

## Project Summary

The repository appears to describe a citizen-science IoT sensor project. The available documentation says sensors upload GPS location and exact timestamps, with consent and retention unspecified. The data schema includes:

- `gps`: latitude/longitude
- `timestamp`: datetime
- `device_id`: string

Evidence:
- [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/README.md:1)
- [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/data/schema.json:1)

## Risk Categories and Evidence

### Location Privacy

The schema includes precise GPS coordinates. Fine-grained location data can reveal home, workplace, travel routines, visits to sensitive places, and participation patterns.

Evidence: `gps: latlon` in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/data/schema.json:1)

### Temporal Tracking

Exact timestamps combined with GPS enable movement reconstruction and behavioral profiling over time.

Evidence: README says uploads include “exact timestamps” in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/README.md:1)

### Persistent Device Linkability

The `device_id` field may allow repeated observations from the same sensor or participant to be linked. Even if no name is stored, persistent identifiers can support re-identification when combined with location and time.

Evidence: `device_id: string` in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/data/schema.json:1)

### Consent and Participant Expectations

The README explicitly says consent is not specified. For citizen-science sensing, contributors may not understand the sensitivity of precise location traces or downstream reuse.

Evidence: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/README.md:1)

### Data Retention and Secondary Use

Retention is not specified. Lack of retention limits increases risk from breach, future misuse, and analysis beyond the original project purpose.

Evidence: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_iot_sensor_location/README.md:1)

### Data Security

The repository does not describe access controls, encryption, storage location, audit logging, or incident response for sensitive location data.

Evidence: no security or governance files are present; repository contains only `README.md` and `data/schema.json`.

## Missing Context and Clarification Questions

- Who are the participants or device owners?
- Are sensors attached to people, homes, vehicles, public infrastructure, or shared devices?
- Is participation opt-in, and what information is provided before data collection?
- Can participants pause collection, review records, delete records, or withdraw?
- What location precision is actually collected and stored?
- Are exact timestamps necessary, or would coarser time windows suffice?
- Is `device_id` stable over time, pseudonymous, rotating, hashed, or directly assigned?
- Who can access raw GPS/timestamp/device records?
- How long is raw data retained?
- Will data be shared publicly, with researchers, with agencies, or with commercial partners?
- Are minors, workers, vulnerable communities, private homes, or sensitive locations involved?
- What is the scientific purpose requiring precise spatiotemporal traces?

## Concrete Mitigations

- Define an explicit consent flow that explains precise location collection, timestamp collection, retention, sharing, and withdrawal.
- Minimize GPS precision where possible, for example spatial binning, geohashing at reduced precision, or collecting only region-level location.
- Minimize timestamp precision where possible, such as hourly or daily buckets if exact times are not required.
- Replace stable `device_id` values with rotating pseudonyms or separate linkage keys from analytical datasets.
- Establish a retention schedule, including deletion of raw GPS traces after the shortest feasible period.
- Restrict raw data access to named roles with logging and review.
- Encrypt data in transit and at rest.
- Separate raw data from derived aggregates.
- Publish only aggregated outputs with thresholds that reduce singling-out risk.
- Add a data management plan covering collection purpose, access, retention, deletion, breach response, and sharing.
- Add participant-facing documentation in plain language.
- Conduct a re-identification risk review before any data release.

## Advisor or Review-Body Discussion Questions

- Is precise GPS plus exact timestamp necessary for the research question?
- Could the study achieve its goals using aggregated, delayed, or perturbed location data?
- What participant population is involved, and are there heightened risks from location exposure?
- What consent model is appropriate for passive IoT sensing?
- What withdrawal and deletion rights should participants have?
- Who will have access to raw traces, and why?
- What safeguards are needed before sharing data outside the project team?
- What harms could result if the data were breached or linked to external datasets?
- Should the project separate operational device management from research analysis data?
- What retention period is justified by the research design?

## Limitations of This Review

This review is based only on the repository files available in the working directory. The repository contains minimal documentation and no implementation code, consent materials, deployment description, data samples, access-control configuration, or data management plan. As a result, this is a preliminary ethics risk review, not a final determination about approval, rejection, legality, compliance, safety, or review-body requirements.