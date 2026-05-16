import re

from repo_ethics.engine.text_signals import find_positive_topic_mentions, topic_is_covered


def test_topic_coverage_positive_and_negated() -> None:
    retention = [re.compile(r"\bdata retention|retention\b", re.I)]
    assert topic_is_covered("We document data retention for 30 days.", retention)
    assert not topic_is_covered("Data retention is not documented.", retention)
    assert not topic_is_covered("Consent assumptions are TBD.", [re.compile(r"\bconsent\b", re.I)])


def test_mixed_clause_negation_keeps_positive_clause() -> None:
    text = "We do not collect usernames, but we store email addresses."
    username = [re.compile(r"\busernames?\b", re.I)]
    email = [re.compile(r"\bemail\b", re.I)]
    assert not find_positive_topic_mentions(text, username)
    assert find_positive_topic_mentions(text, email)


def test_negated_release_with_contrastive_clause() -> None:
    text = "No public dataset will be released, but aggregate statistics will be shared."
    release = [re.compile(r"\bpublic dataset|release dataset|dataset release\b", re.I)]
    aggregate = [re.compile(r"\baggregate statistics\b", re.I)]
    assert not find_positive_topic_mentions(text, release)
    assert find_positive_topic_mentions(text, aggregate)


def test_target_aware_not_a_negation() -> None:
    vulnerability = [re.compile(r"\bvulnerability scanner\b", re.I)]
    assert not find_positive_topic_mentions("This is not a vulnerability scanner.", vulnerability)
    assert find_positive_topic_mentions("This is not a toy and it is a vulnerability scanner.", vulnerability)
    assert find_positive_topic_mentions("This is not a toy, but it is a vulnerability scanner.", vulnerability)


def test_target_aware_not_used_for_negation() -> None:
    port_scanning = [re.compile(r"\bport scanning\b", re.I)]
    assert not find_positive_topic_mentions("This tool is not used for port scanning.", port_scanning)
    assert find_positive_topic_mentions("This tool is not used for demos, but it performs port scanning.", port_scanning)


def test_target_aware_use_and_perform_negation() -> None:
    face = [re.compile(r"\bface_recognition\b", re.I)]
    attendance = [re.compile(r"\battendance tracking\b", re.I)]
    assert not find_positive_topic_mentions("We do not use face_recognition.", face)
    assert find_positive_topic_mentions("We do not use images, but we use face_recognition.", face)
    assert not find_positive_topic_mentions("This project does not perform attendance tracking.", attendance)
    assert find_positive_topic_mentions(
        "This project does not perform grading, but it performs attendance tracking.",
        attendance,
    )


def test_target_aware_scrape_and_track_negation() -> None:
    scrape = [re.compile(r"\bscrape\b", re.I)]
    tracking = [re.compile(r"\btrack(?:ing|s)?\b", re.I)]
    assert not find_positive_topic_mentions("This project does not scrape websites.", scrape)
    assert find_positive_topic_mentions("This project does not scrape websites, but it does scrape local logs.", scrape)
    assert not find_positive_topic_mentions("This project does not track people.", tracking)
    assert find_positive_topic_mentions("This project does not track packages, but it tracks people.", tracking)
