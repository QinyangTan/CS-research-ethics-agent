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

