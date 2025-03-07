from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

__all__ = ["PageParams", "PagedResponseSchema"]


class PageParams(BaseModel):
    """Request query params for paginated API response."""

    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


T = t.TypeVar("T")


class PagedResponseSchema(BaseModel, t.Generic[T]):
    """Response schema for paginated API response."""

    total: int
    page: int
    size: int
    results: t.List[T]
