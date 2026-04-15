"""Response schemas for LLM service."""
from typing import Optional

from pydantic import BaseModel


class LLMResponse(BaseModel):
    """Response schema for LLM completion."""

    status: str
    content: str
    model: str
    tokens_used: Optional[int] = None
    error: Optional[str] = None


class ScoringResponse(BaseModel):
    """Response schema for content scoring."""

    status: str
    score: float
    details: Optional[dict] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response schema for health check."""

    status: str
    version: str
