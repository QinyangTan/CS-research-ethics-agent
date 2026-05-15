# Computer Science Research Ethics Pre-Review

## Project Summary

This repository appears to be a minimal web-scraping research fixture. The code performs an HTTP GET request to `https://example.test` using `requests.get` in [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/src/main.py:1). The README states that pages are collected for research and that platform terms, `robots.txt`, rate limits, data policy, and collection dates are documented in [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/README.md:1). A governance note says rate limits use backoff and that platform terms and `robots.txt` were reviewed in [docs/governance.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/docs/governance.md:1).

## Risk Categories And Evidence From Files

**Web scraping and platform governance risk**

Evidence: [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/src/main.py:2) performs a direct `requests.get(...)`. The README and governance document claim review of platform terms and `robots.txt`, but the repository does not include the reviewed terms, `robots.txt` snapshots, target-specific policy notes, or collection timestamps.

Risk: Without concrete documentation, it is difficult to evaluate whether scraping aligns with site expectations, rate limits, or research norms.

**Rate limiting and service impact risk**

Evidence: [docs/governance.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/docs/governance.md:1) says backoff is used, but [src/main.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/src/main.py:2) shows only a bare request call.

Risk: The implemented code does not demonstrate timeout handling, retry limits, backoff, user-agent identification, request pacing, or error handling. If scaled beyond the fixture, it could unintentionally burden a service.

**Data protection and privacy risk**

Evidence: [README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_scraping_positive_governance/README.md:1) mentions a data policy, but no policy file or data schema is present.

Risk: The repository does not show what data is collected, whether personal data may be captured, how data is minimized, retained, secured, or deleted, or whether sensitive pages are excluded.

**Reproducibility and auditability risk**

Evidence: The README claims collection dates are documented, but no dates, crawl logs, target list, config, or versioned policy snapshots are present.

Risk: Reviewers cannot reconstruct what was collected, when, from where, under which rules, or with which safeguards.

## Missing Context And Clarification Questions

- What specific websites or platforms are targeted beyond `https://example.test`?
- What categories of pages and data fields are collected?
- Does the collection include personal data, user-generated content, login-protected content, deleted content, or content from vulnerable populations?
- Where are the documented platform terms, `robots.txt` records, collection dates, and data policy?
- What rate limit values are used, and are they target-specific?
- Is there an allowlist or denylist for domains and URL paths?
- How are errors, redirects, retries, and HTTP status codes handled?
- How will collected data be stored, secured, shared, anonymized, retained, and deleted?
- Will outputs include quotes, identifiers, usernames, URLs, or other traceable material?

## Concrete Mitigations

- Add a target-specific scraping policy file recording reviewed terms, `robots.txt` URLs, review dates, allowed paths, prohibited paths, and collection windows.
- Implement technical safeguards in code: timeouts, explicit user-agent, bounded retries, exponential backoff, maximum request rate, and clear failure handling.
- Add a domain allowlist and avoid scraping arbitrary URLs.
- Add a data minimization plan specifying fields collected, fields excluded, and whether identifiers are hashed, removed, or retained.
- Add retention and access-control documentation for collected data.
- Add crawl logging that records timestamp, URL, status code, and applied rate-limit behavior.
- Add a dry-run or audit mode that verifies policy constraints before collection.
- Document whether any human-subjects, user-generated, or sensitive content may be involved, and route that question to the appropriate advisor or review body.

## Advisor Or Review-Body Discussion Questions

- Does the project collect data about people, accounts, behavior, or communications in a way that needs additional institutional review?
- Are public web pages being treated as ethically usable by default, or does the research context require additional consent, aggregation, or de-identification?
- Are the platform’s terms and `robots.txt` compatible with the intended collection method and scale?
- What threshold of scale, sensitivity, or identifiability would trigger additional review before deployment?
- Are quotes, URLs, usernames, or page excerpts planned for publication, and could they enable re-identification?
- Who is responsible for monitoring changes to platform policies during collection?

## Limitations Of This Review

This review is based only on the repository files inspected directly: `README.md`, `docs/governance.md`, and `src/main.py`. The repository is extremely small and contains assertions about governance without the supporting artifacts needed to verify them. I did not use external scanners, repo-ethics MCP tools, network checks, or live platform policy lookups. This is a preliminary ethics pre-review, not a final determination of ethical approval, legal compliance, safety, or whether formal review is mandatory.