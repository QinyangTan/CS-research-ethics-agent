**Ethics Pre-Review Report**

**Project Summary**

This repository appears to be a minimal scraper for public forum posts. The stated project controls include rate limits, review of `robots.txt` where applicable, platform terms review, exclusion of private groups, 30-day retention, documented collection dates, and removal of raw usernames before analysis.

Evidence:
- [README.md](benchmarks/fixtures/case_scraping_with_controls/README.md:1)
- [docs/data_policy.md](benchmarks/fixtures/case_scraping_with_controls/docs/data_policy.md:1)
- [src/main.py](benchmarks/fixtures/case_scraping_with_controls/src/main.py:1)

**Risk Categories And Evidence**

- **Human subjects / user data risk:** The project collects forum posts, which may include user-generated content and potentially sensitive personal information, even if publicly accessible. The repository says raw usernames are removed before analysis, but does not show how this is implemented.
- **Privacy and re-identification risk:** Removing usernames alone may not prevent re-identification if post text contains names, handles, locations, URLs, quotations, or rare events.
- **Platform and consent expectations:** The README mentions terms review, `robots.txt` review, no private groups, and rate limits, but the code does not demonstrate these controls.
- **Data retention risk:** The README states a 30-day retention period, but there is no visible retention enforcement mechanism.
- **Operational scraping risk:** `src/main.py` performs a direct `requests.get(...)` call with a timeout, but there is no visible rate limiting, user-agent policy, retry/backoff behavior, logging discipline, or robots/terms check.

**Missing Context And Clarification Questions**

- What forums or platforms are actually being scraped?
- What kinds of posts are collected: text only, metadata, timestamps, URLs, media, reactions, replies?
- Are any posts about sensitive topics, marginalized communities, health, politics, minors, employment, or illegal activity?
- How are usernames and other identifiers removed in practice?
- Is raw data stored locally, in cloud storage, or only in memory?
- Who can access raw and processed data?
- How is the 30-day deletion policy enforced and audited?
- Are quoted posts or reproduced examples included in publications?
- Is there a data management plan for accidental collection of private, deleted, or sensitive content?
- What is the research purpose, and why is scraping necessary instead of using platform APIs, aggregate data, or opt-in data?

**Concrete Mitigations**

- Add implementation-level controls for rate limiting, backoff, and explicit crawl scope.
- Document the exact platforms, endpoints, and fields collected.
- Add a preprocessing step that removes or masks usernames, handles, profile URLs, post IDs, locations, emails, phone numbers, and other direct identifiers.
- Add a policy for handling sensitive content and accidental collection.
- Enforce 30-day deletion with code or documented operational procedure.
- Store raw data separately from analysis data with restricted access.
- Avoid publishing verbatim post text unless necessary; use paraphrases or synthetic examples where possible.
- Record collection dates, platform terms review dates, and `robots.txt` review outcomes.
- Consider whether platform API access, aggregate statistics, or consent-based collection would reduce risk.

**Advisor Or Review-Body Discussion Questions**

- Does the public nature of the forum data sufficiently align with user expectations for research use?
- Could collected posts contain sensitive personal data despite being public?
- Is username removal enough, or is broader de-identification needed?
- Should verbatim quotes be avoided to reduce search-based re-identification?
- Does the project need additional review because of the topic, population, or data sensitivity?
- Are retention and access controls adequate for the expected data volume and risk?
- Are the scraping practices consistent with platform rules and community norms?

**Limitations Of This Review**

This review is based only on the visible repository files and does not verify actual runtime behavior, external platform terms, legal obligations, institutional policies, or the full research protocol. The repository is very small, and several stated safeguards appear only as documentation rather than implemented controls. This is a pre-review risk assessment, not a final determination of ethical approval, legality, compliance, safety, or review-body requirements.