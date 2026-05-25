"""
Search across synthetic employee knowledge sources.
Simple keyword scoring — no external deps; replace with vector search in production.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from bestfraiend.knowledge.data import KNOWLEDGE_BASE, KnowledgeDoc, SOURCE_LABELS


@dataclass
class SearchHit:
    doc: KnowledgeDoc
    score: float


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) > 1}


def search(query: str, category: str | None = None, top_k: int = 3) -> list[SearchHit]:
    """Return top matching documents for a natural-language query."""
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    hits: list[SearchHit] = []
    for doc in KNOWLEDGE_BASE:
        if category and doc.category != category:
            continue

        searchable = " ".join(
            [doc.title, doc.summary, doc.content, doc.source, " ".join(doc.tags)]
        ).lower()
        doc_tokens = _tokenize(searchable)

        overlap = q_tokens & doc_tokens
        if not overlap:
            # partial substring match for phrases like "time off"
            if any(t in searchable for t in q_tokens if len(t) >= 4):
                overlap = q_tokens
            else:
                continue

        score = len(overlap)
        # boost title and tag matches
        title_tokens = _tokenize(doc.title)
        tag_tokens = set(t.lower() for t in doc.tags)
        score += 2 * len(q_tokens & title_tokens)
        score += 1.5 * len(q_tokens & tag_tokens)

        if score > 0:
            hits.append(SearchHit(doc=doc, score=score))

    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:top_k]


def list_sources() -> list[dict[str, str]]:
    """Summary of available source categories for help text."""
    counts: dict[str, int] = {}
    for doc in KNOWLEDGE_BASE:
        counts[doc.category] = counts.get(doc.category, 0) + 1
    return [
        {"category": cat, "label": SOURCE_LABELS.get(cat, cat), "count": counts[cat]}
        for cat in sorted(counts)
    ]


def get_doc_by_id(doc_id: str) -> KnowledgeDoc | None:
    for doc in KNOWLEDGE_BASE:
        if doc.id == doc_id:
            return doc
    return None
