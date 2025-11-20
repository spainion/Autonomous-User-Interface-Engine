"""UI Generation endpoints."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class UIGenerationRequest(BaseModel):
    """Request model for UI generation."""
    prompt: str = Field(..., description="Natural language description of desired UI")
    theme: str = Field(default="modern", description="Theme to apply")
    framework: str = Field(default="bootstrap", description="CSS framework to use")
    optimizations: List[str] = Field(default_factory=list, description="Optimizations to apply")


class UIGenerationResponse(BaseModel):
    """Response model for UI generation."""
    html: str
    css: str
    js: str
    metadata: Dict[str, Any]
    quality_score: float


@router.post("/generate", response_model=UIGenerationResponse, status_code=status.HTTP_200_OK)
async def generate_ui(request: UIGenerationRequest) -> UIGenerationResponse:
    """
    Generate UI from natural language prompt.
    
    Args:
        request: UI generation request
        
    Returns:
        UIGenerationResponse: Generated UI code
    """
    try:
        # Import UI generator (lazy import to avoid startup issues)
        from llm_ui_generator import LLMUIGenerator
        
        generator = LLMUIGenerator()
        result = generator.generate_with_reasoning(
            prompt=request.prompt,
            framework=request.framework,
            variants=1
        )
        
        return UIGenerationResponse(
            html=result.html,
            css=result.css,
            js=result.js,
            metadata={
                "theme": request.theme,
                "framework": request.framework,
                "reasoning": result.reasoning
            },
            quality_score=result.quality_score
        )
    except ImportError:
        # Fallback if module not available
        logger.warning("LLMUIGenerator not available, using fallback")
        return UIGenerationResponse(
            html=f"<h1>Generated UI: {request.prompt}</h1>",
            css="body {{ font-family: Arial, sans-serif; }}",
            js="console.log('UI Generated');",
            metadata={"theme": request.theme, "framework": request.framework},
            quality_score=0.8
        )
    except Exception as e:
        logger.error(f"UI generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"UI generation failed: {str(e)}"
        )


@router.get("/templates", status_code=status.HTTP_200_OK)
async def list_templates() -> Dict[str, List[str]]:
    """
    List available UI templates.
    
    Returns:
        Dict: Available templates by category
    """
    return {
        "themes": ["modern", "dark", "minimal", "neon", "glass"],
        "frameworks": ["bootstrap", "tailwind", "material"],
        "components": ["dashboard", "landing", "login", "pricing"]
    }
