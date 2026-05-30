"""Workflow registration."""

from __future__ import annotations

from .core import WorkflowRegistry
from .workflows import (
    alumni_visit,
    business_book,
    faith,
    family,
    learning,
    lexicon,
    media_growth,
)


def build_registry() -> WorkflowRegistry:
    registry = WorkflowRegistry()
    registry.register("business-book", business_book.run)
    registry.register("alumni-visit", alumni_visit.run)
    registry.register("media-growth", media_growth.run)
    registry.register("faith-study", faith.run)
    registry.register("family-day", family.run)
    registry.register("topology-lexicon", lexicon.run)
    registry.register("personal-growth", learning.run)
    return registry
