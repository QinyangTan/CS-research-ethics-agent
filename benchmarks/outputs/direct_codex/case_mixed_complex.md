# Repository Ethics Pre-Review

## Project Summary

This appears to be a Reddit NLP project. The repository evidence indicates collection of Reddit-related data including usernames, timestamps, and post text, with an intent to publicly release the dataset.

Evidence:
- [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1) says the project “collects usernames and post timestamps,” does not document platform terms or retention, and plans public dataset release.
- [data/posts.jsonl](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/data/posts.jsonl:1) contains `username`, `timestamp`, and `post_text` fields.
- [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/src/main.py:1) imports `praw`, suggesting Reddit API access.

## Risk Categories And Evidence

**Privacy and identifiability risk**

The dataset includes usernames, timestamps, and post text. Even if Reddit posts are public, this combination can be identifying or re-identifying, especially if exact text or timestamps are released.

Evidence:
- `username`, `timestamp`, and `post_text` appear together in [data/posts.jsonl](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/data/posts.jsonl:1).
- README states usernames and timestamps are collected and the dataset will be publicly released: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1).

**Consent and reasonable expectations risk**

The repository does not document whether users consented, whether data comes from public or restricted communities, whether deleted/edited posts are respected, or whether users can opt out.

Evidence:
- README explicitly says platform terms and retention are not documented: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1).
- No consent, notice, opt-out, or deletion policy was found in the inspected files.

**Platform governance and terms risk**

Use of `praw` implies Reddit API interaction, but the repository lacks documentation of API terms, redistribution permissions, data retention constraints, or rate/collection limits.

Evidence:
- `import praw` in [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/src/main.py:1).
- README says platform terms are not documented: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1).

**Public release and downstream misuse risk**

Publishing raw usernames, timestamps, and text could enable profiling, harassment, deanonymization, or unwanted aggregation across contexts.

Evidence:
- README states the dataset will be released publicly: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1).
- Dataset schema includes direct or quasi-identifiers: [data/posts.jsonl](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/data/posts.jsonl:1).

**Data minimization and retention risk**

The repository does not explain why usernames and exact timestamps are necessary, how long raw data will be kept, or whether public release can use less identifying fields.

Evidence:
- README says retention is not documented: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_mixed_complex/README.md:1).

## Missing Context And Clarification Questions

- What research question requires usernames and exact timestamps?
- Are posts from public subreddits only, or from restricted/private communities?
- Will deleted or edited Reddit content be removed from the dataset?
- Will the public release include raw text, usernames, exact timestamps, post IDs, subreddit names, or URLs?
- What Reddit API/platform terms apply to collection, storage, and redistribution?
- Is there a data retention schedule for raw and processed data?
- Is there an opt-out or takedown process?
- Are vulnerable populations, sensitive topics, minors, health, political activity, or support communities included?
- Will models or analyses infer sensitive attributes or produce user-level profiles?

## Concrete Mitigations

- Remove direct usernames from public release, or replace them with salted, non-reversible study-specific IDs.
- Coarsen timestamps, for example to day/week/month if exact timing is not necessary.
- Avoid releasing raw post text where possible; consider derived features, aggregate statistics, or limited excerpts with privacy review.
- Document collection scope, inclusion/exclusion criteria, platform-term review, and API constraints.
- Add a retention and deletion policy, including handling of deleted/edited Reddit content.
- Create a takedown or opt-out mechanism for affected users.
- Conduct a re-identification risk review before public release.
- Exclude or separately review sensitive communities and vulnerable-population contexts.
- Add a dataset card describing provenance, fields, intended uses, prohibited uses, known risks, and contact process.

## Advisor Or Review-Body Discussion Questions

- Is public release of usernames, timestamps, and post text necessary for the research contribution?
- Could the same research be done with less identifiable data?
- What obligations arise from Reddit’s current API/data redistribution terms?
- How will the team handle user deletion, edits, and requests for removal?
- Does the dataset include sensitive communities or topics that increase risk?
- What controls will limit downstream misuse after public release?
- Should the project use an access-controlled release instead of fully public distribution?

## Limitations Of This Review

This review is based only on direct inspection of the repository files available in the workspace. The repository is very small: `README.md`, `src/main.py`, and `data/posts.jsonl`. I did not use repo-ethics MCP tools or scanner output. The sandbox is read-only, so I produced the Markdown report here rather than writing it into the repository. This is an ethics pre-review, not a final determination of approval, rejection, legality, compliance, safety, or IRB requirement.