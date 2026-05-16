**Project Summary**

This appears to be a minimal Reddit scraping project for NLP classification. The README states that it collects Reddit posts, while also noting that platform terms, consent assumptions, retention, and release limits are not documented: [README.md](benchmarks/fixtures/case_scraping_missing_controls/README.md:1). The code initializes a PRAW Reddit client with demo credentials and a generic user agent: [src 2/main.py](benchmarks/fixtures/case_scraping_missing_controls/src%202/main.py:1). The data schema stores `username`, `timestamp`, and `post_text`: [data 2/schema.json](benchmarks/fixtures/case_scraping_missing_controls/data%202/schema.json:1).

**Potential Ethics Issues**

- **Consent and user expectations:** Reddit posts may be public, but users may not expect their posts to be collected, classified, redistributed, or analyzed in research. The README explicitly lacks consent assumptions.
- **Platform terms and API compliance:** The project uses Reddit/PRAW, but there is no documented review of Reddit API terms, allowed use, rate limits, deletion handling, or redistribution limits.
- **PII and re-identification risk:** The schema stores usernames, timestamps, and raw post text. Together, these can directly identify users or make posts searchable and linkable back to individuals.
- **Data retention and security gaps:** The README says retention is undocumented. There is no stated deletion schedule, access-control model, encryption/storage policy, or process for honoring deleted Reddit content.
- **Dataset release risk:** Release limits are not documented. Publishing raw Reddit text plus usernames could expose users, amplify harmful content, or violate platform/user expectations.
- **Classification harm:** The NLP classification task is unspecified. If labels involve sensitive attributes, mental health, politics, toxicity, identity, or moderation, the project may create profiling, bias, or stigmatization risks.

**Suggested Mitigations**

- Add an ethics/data governance document covering purpose, subreddits/scope, legal basis or consent rationale, platform terms review, retention, deletion handling, and release policy.
- Minimize stored data: remove usernames where possible, coarsen timestamps, avoid raw text release, and consider storing derived features or controlled-access datasets instead.
- Use approved Reddit API credentials from environment variables and a descriptive research user agent; document rate limits and API compliance.
- Add an IRB/ethics review decision or exemption rationale before collecting data.
- Define dataset release tiers: internal-only raw data, restricted-access de-identified data, and public aggregate statistics only.
- Add safeguards for sensitive communities and vulnerable users, including exclusion criteria and a harm review for classification labels.

**Questions for the Researcher**

1. What exact NLP classification task is being performed, and are any labels sensitive?
2. Which subreddits or user populations will be collected?
3. Has Reddit’s API/data policy been reviewed for this use and any dataset release?
4. Will raw text, usernames, or post IDs be shared outside the research team?
5. What is the retention period, and how will deleted Reddit content be handled?
6. Has an IRB or institutional ethics review been completed or deemed unnecessary?