"""
AI Features Router for Autonomous UI Engine API
Phase 6: Innovation - API Routes
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging

from ai.advanced_reasoning import ChainOfThoughtReasoner, TreeOfThoughtReasoner, ReActAgent, ReasoningStrategy
from ai.model_router import ModelRouter
from ai.prompt_optimizer import PromptOptimizer
from ai.context_compression import ContextCompressor

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize AI components
cot_reasoner = ChainOfThoughtReasoner()
tot_reasoner = TreeOfThoughtReasoner()
react_agent = ReActAgent()
model_router = ModelRouter()
prompt_optimizer = PromptOptimizer()
context_compressor = ContextCompressor()


# Request/Response models
class ReasoningRequest(BaseModel):
    """Request for reasoning operations."""
    problem: str = Field(..., description="Problem to reason about")
    strategy: Optional[str] = Field("chain_of_thought", description="Reasoning strategy")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ModelRoutingRequest(BaseModel):
    """Request for model routing."""
    task: str = Field(..., description="Task description")
    task_type: Optional[str] = None
    context_size: Optional[int] = None
    budget: Optional[float] = None
    priority: str = "balanced"


class PromptOptimizationRequest(BaseModel):
    """Request for prompt optimization."""
    prompt: str = Field(..., description="Prompt to optimize")
    strategy: Optional[str] = None
    target_task: Optional[str] = None


class ContextCompressionRequest(BaseModel):
    """Request for context compression."""
    text: str = Field(..., description="Text to compress")
    max_tokens: int = Field(..., description="Maximum tokens allowed")
    strategy: Optional[str] = None
    preserve_sections: Optional[List[str]] = None


@router.post("/reasoning/chain-of-thought")
async def chain_of_thought_reasoning(request: ReasoningRequest):
    """Apply chain-of-thought reasoning to a problem."""
    try:
        result = await cot_reasoner.reason(request.problem, request.context)
        
        return {
            "success": True,
            "steps": [
                {
                    "step_number": step.step_number,
                    "thought": step.thought,
                    "reasoning": step.reasoning,
                    "confidence": step.confidence
                }
                for step in result.steps
            ],
            "final_answer": result.final_answer,
            "confidence": result.total_confidence,
            "strategy": "chain_of_thought"
        }
    except Exception as e:
        logger.error(f"Chain-of-thought reasoning failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reasoning/tree-of-thought")
async def tree_of_thought_reasoning(request: ReasoningRequest):
    """Apply tree-of-thought reasoning to explore multiple paths."""
    try:
        result = await tot_reasoner.reason(request.problem, request.context)
        
        return {
            "success": True,
            "steps": [
                {
                    "step_number": step.step_number,
                    "thought": step.thought,
                    "reasoning": step.reasoning,
                    "confidence": step.confidence
                }
                for step in result.steps
            ],
            "final_answer": result.final_answer,
            "confidence": result.total_confidence,
            "strategy": "tree_of_thought"
        }
    except Exception as e:
        logger.error(f"Tree-of-thought reasoning failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reasoning/react")
async def react_reasoning(request: ReasoningRequest):
    """Apply ReAct reasoning (reasoning + acting)."""
    try:
        result = await react_agent.reason_and_act(request.problem, request.context)
        
        return {
            "success": True,
            "steps": [
                {
                    "step_number": step.step_number,
                    "thought": step.thought,
                    "action": step.metadata.get("action"),
                    "observation": step.metadata.get("observation"),
                    "confidence": step.confidence
                }
                for step in result.steps
            ],
            "final_answer": result.final_answer,
            "confidence": result.total_confidence,
            "strategy": "react"
        }
    except Exception as e:
        logger.error(f"ReAct reasoning failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/model-routing/route")
async def route_model(request: ModelRoutingRequest):
    """Route task to the most appropriate model."""
    try:
        decision = await model_router.route_task(
            task=request.task,
            task_type=request.task_type,
            context_size=request.context_size,
            budget=request.budget,
            priority=request.priority
        )
        
        return {
            "success": True,
            "selected_model": {
                "name": decision.selected_model.name,
                "provider": decision.selected_model.provider,
                "tier": decision.selected_model.tier.value
            },
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "estimated_cost": decision.estimated_cost,
            "fallback_models": [
                {"name": m.name, "provider": m.provider}
                for m in decision.fallback_models
            ]
        }
    except Exception as e:
        logger.error(f"Model routing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-routing/stats")
async def get_routing_stats():
    """Get model routing statistics."""
    try:
        stats = model_router.get_routing_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Failed to get routing stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prompt/optimize")
async def optimize_prompt(request: PromptOptimizationRequest):
    """Optimize a prompt for better results."""
    try:
        from ai.prompt_optimizer import OptimizationStrategy
        
        strategy = None
        if request.strategy:
            strategy = OptimizationStrategy(request.strategy)
        
        result = await prompt_optimizer.optimize(
            prompt=request.prompt,
            strategy=strategy,
            target_task=request.target_task
        )
        
        return {
            "success": True,
            "original_prompt": result.original_prompt,
            "optimized_prompt": result.optimized_prompt,
            "improvements": result.improvements,
            "strategy": result.strategy_used.value,
            "confidence": result.confidence_score,
            "estimated_improvement": result.estimated_improvement
        }
    except Exception as e:
        logger.error(f"Prompt optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prompt/stats")
async def get_optimization_stats():
    """Get prompt optimization statistics."""
    try:
        stats = prompt_optimizer.get_optimization_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Failed to get optimization stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/context/compress")
async def compress_context(request: ContextCompressionRequest):
    """Compress context to fit within token limits."""
    try:
        from ai.context_compression import CompressionStrategy
        
        strategy = None
        if request.strategy:
            strategy = CompressionStrategy(request.strategy)
        
        result = await context_compressor.compress(
            text=request.text,
            max_tokens=request.max_tokens,
            strategy=strategy,
            preserve_sections=request.preserve_sections
        )
        
        return {
            "success": True,
            "original_tokens": result.original_tokens,
            "compressed_tokens": result.compressed_tokens,
            "compression_ratio": result.compression_ratio,
            "preserved_information": result.preserved_information,
            "strategy": result.strategy_used.value,
            "compressed_text": result.compressed_text
        }
    except Exception as e:
        logger.error(f"Context compression failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/context/compression-stats")
async def get_compression_stats():
    """Get context compression statistics."""
    try:
        stats = context_compressor.get_compression_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Failed to get compression stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def ai_health_check():
    """Check health of AI features."""
    return {
        "status": "healthy",
        "features": {
            "reasoning": "available",
            "model_routing": "available",
            "prompt_optimization": "available",
            "context_compression": "available"
        }
    }
