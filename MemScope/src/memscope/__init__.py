"""MemScope purpose-bound persistent-memory reference implementation."""

from .data.schemas import MemoryItem, MemoryLabel, Provenance, TaskContext
from .methods.policy import authorize, meet_labels
from .methods.retrieval import MemScopeService

__all__ = [
    "MemoryItem",
    "MemoryLabel",
    "MemScopeService",
    "Provenance",
    "TaskContext",
    "authorize",
    "meet_labels",
]

__version__ = "0.1.0"
