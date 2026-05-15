**Computer Science Research Ethics Pre-Review**

**Project Summary**

The repository appears to describe a project that collects Reddit posts for NLP classification. The implementation is minimal: it initializes a PRAW Reddit client in [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/src/main.py:1), and the dataset schema includes `username`, `timestamp`, and `post_text` in [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/data/schema.json:1).

The README explicitly states that platform terms, consent assumptions, data retention, and dataset release limits are not documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/README.md:1).

**Risk Categories And Evidence**

- **Human-subjects and consent uncertainty:** The project collects Reddit posts, but no consent model or public/private boundary analysis is documented. Evidence: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/README.md:1).
- **Privacy and identifiability risk:** The schema stores `username`, `timestamp`, and `post_text`, which can directly or indirectly identify users, especially when combined. Evidence: [data/schema.json](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/data/schema.json:1).
- **Platform governance risk:** The project uses PRAW to access Reddit but does not document Reddit API/platform terms, rate limits, redistribution limits, deletion handling, or user-content policy obligations. Evidence: [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/src/main.py:1), [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/README.md:1).
- **Data retention and release risk:** The README states retention and dataset release limits are not documented. Evidence: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/README.md:1).
- **Security and credential handling risk:** The code contains placeholder credentials directly in source. Even though they are `demo` values, the pattern suggests no documented secret-management practice. Evidence: [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_missing_controls/src/main.py:2).
- **Downstream misuse and harm risk:** NLP classification of Reddit posts could infer sensitive attributes, stigmatize communities, or enable profiling depending on labels and use case. The repository does not describe the classification task, target communities, labeling policy, or deployment boundary.

**Missing Context And Clarification Questions**

- What subreddits, users, time ranges, and post types are collected?
- Are private, quarantined, deleted, edited, or restricted communities excluded?
- What is the classification objective, and could it involve sensitive traits, mental health, politics, identity, or vulnerability?
- Will usernames be stored, transformed, hashed, or removed before analysis?
- Will raw text be redistributed, or only derived features/model outputs?
- How are user deletions, edits, opt-outs, and takedown requests handled?
- What access controls protect collected data?
- Who can access the dataset, and for how long?
- Is the work exploratory, internal-only, publication-oriented, or intended for deployment?

**Concrete Mitigations**

- Add a data-management plan covering collection scope, minimization, retention period, deletion process, access controls, and release policy.
- Avoid storing usernames unless necessary; prefer post IDs or irreversible internal IDs, and document the residual re-identification risk.
- Strip or redact direct identifiers and high-risk personal details from `post_text` where feasible.
- Document Reddit API/platform-term review, including redistribution limits and deletion/edit synchronization.
- Define exclusion rules for sensitive communities or vulnerable populations.
- Add a release policy that avoids publishing raw Reddit text unless clearly justified and reviewed.
- Store credentials through environment variables or a secret manager rather than source files.
- Add logging and rate-limit controls that avoid excessive collection.
- Create a review checklist before dataset publication or model release, including privacy, representational harm, and misuse analysis.

**Advisor Or Review-Body Discussion Questions**

- Does the project’s collection and analysis plan require additional institutional review or advisor signoff given the population, content, and intended publication?
- Is collecting usernames necessary for the research question?
- Is raw text necessary, or would derived features or aggregate statistics be sufficient?
- What harms could arise if users, communities, or sensitive attributes are inferred from the dataset?
- What dataset-sharing approach balances reproducibility with privacy and platform obligations?
- Should the project exclude certain communities or topics from collection?

**Limitations Of This Review**

This review is based only on direct inspection of the repository files. The repository contains very little code and no full scraper, dataset, labeling protocol, model code, consent analysis, or release plan. I did not use repo-ethics MCP tools, scanner output, or external legal/platform review. This is a pre-review identifying issues and questions; it is not final ethical approval, rejection, legal advice, compliance determination, safety certification, or a determination that IRB review is mandatory.