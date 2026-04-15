"""API routes for LLM service."""
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.schemas.request import LLMRequest, ScoringRequest
from app.schemas.response import HealthResponse, LLMResponse, ScoringResponse
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.services.scoring_service import ScoringService

router = APIRouter()

# Initialize services
llm_client = LLMClient()
prompt_builder = PromptBuilder()
scoring_service = ScoringService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
    }


@router.post("/llm/complete", response_model=LLMResponse)
async def complete_prompt(request: LLMRequest):
    """
    Complete a prompt using LLM.

    Args:
        request: LLM request with prompt and parameters

    Returns:
        LLM response with completion
    """
    try:
        result = await llm_client.complete(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return LLMResponse(
            status="success",
            content=result.get("content", ""),
            model=result.get("model", settings.LLM_MODEL),
            tokens_used=result.get("tokens_used"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/score", response_model=ScoringResponse)
async def score_content(request: ScoringRequest):
    """
    Score content.

    Args:
        request: Scoring request with content and type

    Returns:
        Scoring response with score
    """
    try:
        result = scoring_service.score_content(
            content=request.content,
            scoring_type=request.scoring_type,
        )
        return ScoringResponse(
            status="success",
            score=result.get("score", 0.0),
            details=result.get("details"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/llm/complete-with-context", response_model=LLMResponse)
async def complete_with_context(request: LLMRequest):
    """
    Complete a prompt with context.

    Args:
        request: LLM request

    Returns:
        LLM response with completion
    """
    try:
        # Build prompt with context
        built_prompt = prompt_builder.build(request.prompt)

        result = await llm_client.complete(
            prompt=built_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return LLMResponse(
            status="success",
            content=result.get("content", ""),
            model=result.get("model", settings.LLM_MODEL),
            tokens_used=result.get("tokens_used"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
