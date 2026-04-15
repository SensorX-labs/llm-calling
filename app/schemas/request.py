"""Request schemas for LLM service."""
from typing import Optional

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """Request schema for LLM completion."""

    prompt: str = Field(..., description="The prompt to send to LLM")
    model: Optional[str] = Field(None, description="Model to use (optional)")
    temperature: Optional[float] = Field(
        None, description="Temperature for generation (0-2)"
    )
    max_tokens: Optional[int] = Field(None, description="Maximum tokens in response")


class ScoringRequest(BaseModel):
    """Request schema for content scoring."""

    content: str = Field(..., description="Content to score")
    scoring_type: str = Field(
        default="quality", description="Type of scoring (quality, relevance, etc)"
    )
