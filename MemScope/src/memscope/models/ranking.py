"""Confined rankers that can only return identifiers from their input view."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List, Sequence, Tuple

from ..data.schemas import MemoryItem


class Ranker(ABC):
    @abstractmethod
    def rank(self, query: str, items: Sequence[MemoryItem], k: int) -> List[MemoryItem]:
        """Return at most k items and never introduce an identifier outside `items`."""


class LexicalRanker(Ranker):
    """Deterministic token-overlap ranker for tests and the synthetic harness."""

    @staticmethod
    def _tokens(text: str) -> set:
        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def rank(self, query: str, items: Sequence[MemoryItem], k: int) -> List[MemoryItem]:
        if k < 0:
            raise ValueError("k must be non-negative")
        query_tokens = self._tokens(query)

        def key(item: MemoryItem) -> Tuple[int, str]:
            return (-len(query_tokens & self._tokens(item.payload)), item.item_id)

        return sorted(items, key=key)[:k]
