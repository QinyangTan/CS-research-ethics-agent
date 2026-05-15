"""Deterministic text-signal helpers for conservative scanner heuristics."""

from __future__ import annotations

import re
from collections.abc import Iterable


MISSING_CONTEXT_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.I)
    for pattern in [
        r"\bnot\s+yet\s+documented\b",
        r"\bnot\s+documented\b",
        r"\bnot\s+yet\s+covered\b",
        r"\bnot\s+covered\b",
        r"\bdoes\s+not\s+document\b",
        r"\bdoes\s+not\s+yet\s+define\b",
        r"\bdoes\s+not\s+define\b",
        r"\bdo\s+not\s+document\b",
        r"\bdo\s+not\s+define\b",
        r"\bdoesn't\s+document\b",
        r"\bdoesn't\s+define\b",
        r"\bdon't\s+document\b",
        r"\bdon't\s+define\b",
        r"\bnot\s+yet\s+define[sd]?\b",
        r"\bnot\s+define[sd]?\b",
        r"\bno\s+documentation\b",
        r"\bno\s+documented\b",
        r"\bwithout\s+documenting\b",
        r"\bwithout\s+documentation\b",
        r"\bmissing\b",
        r"\bunclear\b",
        r"\bunknown\b",
        r"\bnot\s+specified\b",
        r"\bnot\s+described\b",
        r"\bnot\s+stated\b",
        r"\bnot\s+addressed\b",
        r"\bhas\s+not\s+yet\b",
        r"\bhave\s+not\s+yet\b",
        r"\bcurrently\s+lacks\b",
        r"\blacks\b",
        r"\bto\s+be\s+determined\b",
        r"\bTBD\b",
    ]
)

ABSENCE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.I)
    for pattern in [
        r"\bdoes\s+not\s+collect\b",
        r"\bdoes\s+not\s+use\b",
        r"\bdoes\s+not\s+perform\b",
        r"\bdo\s+not\s+collect\b",
        r"\bdo\s+not\s+use\b",
        r"\bdo\s+not\s+perform\b",
        r"\bdoesn't\s+collect\b",
        r"\bdoesn't\s+use\b",
        r"\bdoesn't\s+perform\b",
        r"\bdon't\s+collect\b",
        r"\bdon't\s+use\b",
        r"\bdon't\s+perform\b",
        r"\bnot\s+collect(?:ed)?\b",
        r"\bnot\s+used\s+for\b",
        r"\bnot\s+perform\b",
        r"\bnot\s+stored?\b",
        r"\bno\s+public\s+dataset\b",
        r"\bno\s+dataset\b",
        r"\bno\s+[^.?!,;]{0,80}\b(?:stored|collected|released|shared)\b",
        r"\bwill\s+not\s+be\s+(?:stored|collected|released|shared)\b",
    ]
)

CONTRASTIVE_SPLIT_RE = re.compile(r"\b(?:but|however|although|except|unless)\b", re.I)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|[\n;]+")
TARGET_PREFIX_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.I)
    for pattern in [
        r"\bnot\s+(?:a|an|the)\s+$",
        r"\bnot\s+used\s+for\s+$",
        r"\bnot\s+intended\s+for\s+$",
        r"\bnot\s+designed\s+for\s+$",
        r"\b(?:does|do)\s+not\s+(?:collect|use|perform|store|release|share)\s+$",
        r"\b(?:doesn't|don't)\s+(?:collect|use|perform|store|release|share)\s+$",
        r"\bnot\s+(?:collect|collecting|use|using|perform|performing|store|storing|release|releasing|share|sharing)\s+$",
        r"\bwithout\s+(?:collecting|using|performing|storing|releasing|sharing)\s+$",
    ]
)
TARGET_SUFFIX_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.I)
    for pattern in [
        r"^\s+(?:is|are|was|were|will\s+be|would\s+be)?\s*not\s+(?:stored|collected|used|performed|released|shared|documented|specified|described|stated|addressed)\b",
        r"^\s+(?:is|are|was|were)?\s*(?:missing|unclear|unknown|tbd|to\s+be\s+determined)\b",
        r"^\s+(?:will\s+not|would\s+not)\s+be\s+(?:stored|collected|used|performed|released|shared)\b",
    ]
)
NO_TARGET_SUFFIX_RE = re.compile(
    r"^(?:[\w/_.-]+\s+){0,8}(?:is|are|was|were|will\s+be|would\s+be)?\s*"
    r"(?:stored|collected|used|performed|released|shared|match|matches|risk|risks|finding|findings|signal|signals)\b",
    re.I,
)


def _nonempty_span(text: str, start: int, end: int) -> tuple[int, int, str] | None:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if start >= end:
        return None
    return start, end, text[start:end]


def _split_with_offsets(text: str, separator_re: re.Pattern[str]) -> list[tuple[int, int, str]]:
    chunks: list[tuple[int, int, str]] = []
    start = 0
    for match in separator_re.finditer(text):
        chunk = _nonempty_span(text, start, match.start())
        if chunk is not None:
            chunks.append(chunk)
        start = match.end()
    chunk = _nonempty_span(text, start, len(text))
    if chunk is not None:
        chunks.append(chunk)
    return chunks


def _iter_clauses_with_offsets(text: str) -> Iterable[tuple[int, int, str]]:
    for sentence_start, sentence_end, sentence in _split_with_offsets(text, SENTENCE_SPLIT_RE):
        for clause_start, clause_end, clause in _split_with_offsets(sentence, CONTRASTIVE_SPLIT_RE):
            yield sentence_start + clause_start, sentence_start + clause_end, clause


def split_sentences(text: str) -> list[str]:
    """Split text into sentence-like clauses, including contrastive clauses."""

    return [clause for _, _, clause in _iter_clauses_with_offsets(text)]


def _clause_for_keyword(sentence: str, keyword_start: int | None) -> str:
    if keyword_start is None:
        return sentence
    for start, end, clause in _iter_clauses_with_offsets(sentence):
        if start <= keyword_start < end:
            return clause
    return sentence


def is_negated_sentence(sentence: str, keyword_start: int | None = None) -> bool:
    """Return True when the relevant sentence/clause indicates absence or uncertainty."""

    clause = _clause_for_keyword(sentence, keyword_start)
    if keyword_start is not None:
        local_start = keyword_start
        for start, end, _ in _iter_clauses_with_offsets(sentence):
            if start <= keyword_start < end:
                local_start = keyword_start - start
                break
        return is_negated_for_match(clause, local_start)
    return any(pattern.search(clause) for pattern in (*MISSING_CONTEXT_PATTERNS, *ABSENCE_PATTERNS))


def is_negated_for_match(clause: str, match_start: int, match_end: int | None = None) -> bool:
    """Return True when a negation targets the specific matched term."""

    if match_end is None:
        match_end = match_start
    prefix = clause[max(0, match_start - 120) : match_start].lower()
    suffix = clause[match_end : min(len(clause), match_end + 120)].lower().lstrip()
    local = clause[max(0, match_start - 80) : min(len(clause), (match_end or match_start) + 80)]

    if any(pattern.search(local) for pattern in MISSING_CONTEXT_PATTERNS):
        return True
    if any(pattern.search(prefix) for pattern in TARGET_PREFIX_PATTERNS):
        return True
    if any(pattern.search(clause[match_end : min(len(clause), match_end + 120)]) for pattern in TARGET_SUFFIX_PATTERNS):
        return True
    if re.search(r"\bno\s+$", prefix) and NO_TARGET_SUFFIX_RE.search(suffix):
        return True
    return False


def strip_negated_sentences(text: str) -> str:
    """Remove negated clauses so broad repo-profile signals do not count absence as presence."""

    return "\n".join(clause for _, _, clause in _iter_clauses_with_offsets(text) if not is_negated_sentence(clause))


def _find_topic_mentions(
    text: str,
    patterns: list[re.Pattern[str]],
    *,
    want_negated: bool,
) -> list[tuple[int, int, str]]:
    mentions: list[tuple[int, int, str]] = []
    for clause_start, _, clause in _iter_clauses_with_offsets(text):
        for pattern in patterns:
            for match in pattern.finditer(clause):
                negated = is_negated_for_match(clause, match.start(), match.end())
                if negated is want_negated:
                    start = clause_start + match.start()
                    end = clause_start + match.end()
                    mentions.append((start, end, clause.strip()))
    return mentions


def topic_is_covered(text: str, patterns: list[re.Pattern[str]]) -> bool:
    """Return True only when a topic has at least one positive, non-negated mention."""

    return bool(find_positive_topic_mentions(text, patterns))


def find_positive_topic_mentions(text: str, patterns: list[re.Pattern[str]]) -> list[tuple[int, int, str]]:
    return _find_topic_mentions(text, patterns, want_negated=False)


def find_negated_topic_mentions(text: str, patterns: list[re.Pattern[str]]) -> list[tuple[int, int, str]]:
    return _find_topic_mentions(text, patterns, want_negated=True)
