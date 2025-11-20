"""
Intelligent Model Router for Autonomous UI Engine
Phase 6: Innovation - AI Features

Routes tasks to the most appropriate model based on complexity, cost, and performance.
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class TaskComplexity(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class ModelTier(Enum):
    """Model capability tiers."""
    FAST = "fast"           # Fast, cheap models (GPT-3.5, Claude Instant)
    BALANCED = "balanced"   # Balanced models (GPT-4, Claude 2)
    POWERFUL = "powerful"   # Powerful models (GPT-4-turbo, Claude 3)
    SPECIALIST = "specialist"  # Domain-specific models


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    provider: str  # openai, anthropic, openrouter
    tier: ModelTier
    cost_per_1k_tokens: float
    max_tokens: int
    capabilities: List[str]
    strengths: List[str]
    ideal_for: List[str]


@dataclass
class RoutingDecision:
    """Represents a model routing decision."""
    selected_model: ModelConfig
    reasoning: str
    confidence: float
    estimated_cost: float
    fallback_models: List[ModelConfig]


class ModelRouter:
    """
    Intelligent model router that selects the best model for a given task.
    """
    
    def __init__(self):
        """Initialize the model router with available models."""
        self.models = self._initialize_models()
        self.routing_history: List[Dict[str, Any]] = []
        
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize available models and their configurations."""
        return {
            # Fast, economical models
            "gpt-3.5-turbo": ModelConfig(
                name="gpt-3.5-turbo",
                provider="openai",
                tier=ModelTier.FAST,
                cost_per_1k_tokens=0.002,
                max_tokens=4096,
                capabilities=["text", "chat", "code"],
                strengths=["speed", "cost-effective", "general-purpose"],
                ideal_for=["simple-queries", "quick-responses", "high-volume"]
            ),
            
            "claude-instant": ModelConfig(
                name="claude-instant-1.2",
                provider="anthropic",
                tier=ModelTier.FAST,
                cost_per_1k_tokens=0.0024,
                max_tokens=100000,
                capabilities=["text", "chat", "analysis"],
                strengths=["speed", "large-context", "safe"],
                ideal_for=["document-analysis", "quick-tasks", "conversations"]
            ),
            
            # Balanced models
            "gpt-4": ModelConfig(
                name="gpt-4",
                provider="openai",
                tier=ModelTier.BALANCED,
                cost_per_1k_tokens=0.03,
                max_tokens=8192,
                capabilities=["text", "chat", "code", "reasoning"],
                strengths=["accuracy", "reasoning", "code-quality"],
                ideal_for=["complex-tasks", "code-generation", "analysis"]
            ),
            
            "claude-2": ModelConfig(
                name="claude-2.1",
                provider="anthropic",
                tier=ModelTier.BALANCED,
                cost_per_1k_tokens=0.024,
                max_tokens=200000,
                capabilities=["text", "chat", "code", "analysis"],
                strengths=["large-context", "safe", "detailed"],
                ideal_for=["long-documents", "detailed-analysis", "research"]
            ),
            
            # Powerful models
            "gpt-4-turbo": ModelConfig(
                name="gpt-4-turbo-preview",
                provider="openai",
                tier=ModelTier.POWERFUL,
                cost_per_1k_tokens=0.01,
                max_tokens=128000,
                capabilities=["text", "chat", "code", "vision", "reasoning"],
                strengths=["speed", "large-context", "multimodal"],
                ideal_for=["complex-reasoning", "large-codebases", "vision-tasks"]
            ),
            
            "claude-3-opus": ModelConfig(
                name="claude-3-opus",
                provider="anthropic",
                tier=ModelTier.POWERFUL,
                cost_per_1k_tokens=0.015,
                max_tokens=200000,
                capabilities=["text", "chat", "code", "vision", "analysis"],
                strengths=["accuracy", "reasoning", "creativity"],
                ideal_for=["expert-tasks", "creative-work", "critical-decisions"]
            ),
            
            # Specialist models
            "codex": ModelConfig(
                name="gpt-4-code",
                provider="openai",
                tier=ModelTier.SPECIALIST,
                cost_per_1k_tokens=0.02,
                max_tokens=8192,
                capabilities=["code", "debugging", "refactoring"],
                strengths=["code-quality", "best-practices", "debugging"],
                ideal_for=["code-generation", "code-review", "refactoring"]
            )
        }
    
    async def route_task(
        self,
        task: str,
        task_type: Optional[str] = None,
        context_size: Optional[int] = None,
        budget: Optional[float] = None,
        priority: str = "balanced"  # speed, cost, quality, balanced
    ) -> RoutingDecision:
        """
        Route a task to the most appropriate model.
        
        Args:
            task: The task description
            task_type: Optional task type (code, text, analysis, etc.)
            context_size: Estimated context size in tokens
            budget: Maximum budget for the task
            priority: Optimization priority (speed, cost, quality, balanced)
            
        Returns:
            RoutingDecision with selected model and reasoning
        """
        try:
            logger.info(f"Routing task: {task[:100]}...")
            
            # Analyze task complexity
            complexity = await self._analyze_task_complexity(task, task_type)
            
            # Filter models based on requirements
            suitable_models = self._filter_suitable_models(
                complexity=complexity,
                context_size=context_size,
                budget=budget,
                task_type=task_type
            )
            
            if not suitable_models:
                logger.warning("No suitable models found, using default")
                suitable_models = [self.models["gpt-3.5-turbo"]]
            
            # Select best model based on priority
            selected_model = self._select_best_model(
                suitable_models,
                priority=priority,
                complexity=complexity
            )
            
            # Generate routing decision
            decision = RoutingDecision(
                selected_model=selected_model,
                reasoning=self._generate_reasoning(
                    selected_model, complexity, priority
                ),
                confidence=self._calculate_confidence(
                    selected_model, complexity
                ),
                estimated_cost=self._estimate_cost(
                    selected_model, context_size or 1000
                ),
                fallback_models=suitable_models[:3]
            )
            
            # Log decision
            self._log_routing_decision(task, decision)
            
            logger.info(f"Selected model: {selected_model.name} (confidence: {decision.confidence:.2f})")
            return decision
            
        except Exception as e:
            logger.error(f"Error routing task: {e}")
            # Fallback to default model
            default_model = self.models["gpt-3.5-turbo"]
            return RoutingDecision(
                selected_model=default_model,
                reasoning=f"Error in routing, using fallback: {str(e)}",
                confidence=0.5,
                estimated_cost=0.01,
                fallback_models=[default_model]
            )
    
    async def _analyze_task_complexity(
        self,
        task: str,
        task_type: Optional[str]
    ) -> TaskComplexity:
        """Analyze task complexity based on content and type."""
        # Simple heuristics (in production, use ML model or LLM)
        task_lower = task.lower()
        
        # Expert level indicators
        expert_indicators = [
            "optimize", "architect", "design system", "security audit",
            "performance tuning", "scale", "enterprise"
        ]
        if any(indicator in task_lower for indicator in expert_indicators):
            return TaskComplexity.EXPERT
        
        # Complex level indicators
        complex_indicators = [
            "analyze", "complex", "multiple", "integrate", "refactor",
            "debug", "troubleshoot"
        ]
        if any(indicator in task_lower for indicator in complex_indicators):
            return TaskComplexity.COMPLEX
        
        # Moderate level indicators
        moderate_indicators = [
            "create", "implement", "develop", "build", "generate"
        ]
        if any(indicator in task_lower for indicator in moderate_indicators):
            return TaskComplexity.MODERATE
        
        # Default to simple
        return TaskComplexity.SIMPLE
    
    def _filter_suitable_models(
        self,
        complexity: TaskComplexity,
        context_size: Optional[int],
        budget: Optional[float],
        task_type: Optional[str]
    ) -> List[ModelConfig]:
        """Filter models based on requirements."""
        suitable = []
        
        for model in self.models.values():
            # Check context size
            if context_size and context_size > model.max_tokens:
                continue
            
            # Check budget
            if budget:
                estimated_cost = (context_size or 1000) / 1000 * model.cost_per_1k_tokens
                if estimated_cost > budget:
                    continue
            
            # Check complexity match
            if complexity == TaskComplexity.SIMPLE and model.tier in [ModelTier.FAST]:
                suitable.append(model)
            elif complexity == TaskComplexity.MODERATE and model.tier in [ModelTier.FAST, ModelTier.BALANCED]:
                suitable.append(model)
            elif complexity == TaskComplexity.COMPLEX and model.tier in [ModelTier.BALANCED, ModelTier.POWERFUL]:
                suitable.append(model)
            elif complexity == TaskComplexity.EXPERT and model.tier in [ModelTier.POWERFUL, ModelTier.SPECIALIST]:
                suitable.append(model)
        
        return suitable
    
    def _select_best_model(
        self,
        suitable_models: List[ModelConfig],
        priority: str,
        complexity: TaskComplexity
    ) -> ModelConfig:
        """Select the best model based on priority."""
        if not suitable_models:
            return self.models["gpt-3.5-turbo"]
        
        if priority == "speed":
            # Prefer faster models
            return min(suitable_models, key=lambda m: m.cost_per_1k_tokens)
        
        elif priority == "cost":
            # Prefer cheaper models
            return min(suitable_models, key=lambda m: m.cost_per_1k_tokens)
        
        elif priority == "quality":
            # Prefer powerful models
            tier_priority = {
                ModelTier.FAST: 0,
                ModelTier.BALANCED: 1,
                ModelTier.POWERFUL: 2,
                ModelTier.SPECIALIST: 3
            }
            return max(suitable_models, key=lambda m: tier_priority[m.tier])
        
        else:  # balanced
            # Balance between cost and quality
            if complexity in [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]:
                return min(suitable_models, key=lambda m: m.cost_per_1k_tokens)
            else:
                tier_priority = {
                    ModelTier.FAST: 0,
                    ModelTier.BALANCED: 1,
                    ModelTier.POWERFUL: 2,
                    ModelTier.SPECIALIST: 3
                }
                return max(suitable_models, key=lambda m: tier_priority[m.tier])
    
    def _generate_reasoning(
        self,
        model: ModelConfig,
        complexity: TaskComplexity,
        priority: str
    ) -> str:
        """Generate reasoning for model selection."""
        return (
            f"Selected {model.name} based on {priority} priority. "
            f"Task complexity: {complexity.value}. "
            f"Model strengths: {', '.join(model.strengths[:3])}. "
            f"Ideal for: {', '.join(model.ideal_for[:2])}."
        )
    
    def _calculate_confidence(
        self,
        model: ModelConfig,
        complexity: TaskComplexity
    ) -> float:
        """Calculate confidence in model selection."""
        # Simple confidence calculation
        base_confidence = 0.7
        
        # Increase confidence for good matches
        if complexity == TaskComplexity.SIMPLE and model.tier == ModelTier.FAST:
            base_confidence += 0.2
        elif complexity == TaskComplexity.COMPLEX and model.tier == ModelTier.POWERFUL:
            base_confidence += 0.2
        elif complexity == TaskComplexity.EXPERT and model.tier in [ModelTier.POWERFUL, ModelTier.SPECIALIST]:
            base_confidence += 0.25
        
        return min(base_confidence, 1.0)
    
    def _estimate_cost(
        self,
        model: ModelConfig,
        context_size: int
    ) -> float:
        """Estimate cost for using the model."""
        # Estimate total tokens (input + output)
        total_tokens = context_size + (context_size * 0.5)  # Assume 50% output
        return (total_tokens / 1000) * model.cost_per_1k_tokens
    
    def _log_routing_decision(
        self,
        task: str,
        decision: RoutingDecision
    ) -> None:
        """Log routing decision for analytics."""
        self.routing_history.append({
            "task": task[:100],
            "model": decision.selected_model.name,
            "confidence": decision.confidence,
            "estimated_cost": decision.estimated_cost,
            "reasoning": decision.reasoning
        })
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions."""
        if not self.routing_history:
            return {"total_decisions": 0}
        
        model_counts = {}
        for decision in self.routing_history:
            model = decision["model"]
            model_counts[model] = model_counts.get(model, 0) + 1
        
        avg_confidence = sum(d["confidence"] for d in self.routing_history) / len(self.routing_history)
        total_estimated_cost = sum(d["estimated_cost"] for d in self.routing_history)
        
        return {
            "total_decisions": len(self.routing_history),
            "model_distribution": model_counts,
            "average_confidence": avg_confidence,
            "total_estimated_cost": total_estimated_cost
        }


# Example usage
async def example_usage():
    """Example of using the model router."""
    router = ModelRouter()
    
    # Simple task - should route to fast model
    decision1 = await router.route_task(
        "What is the capital of France?",
        priority="cost"
    )
    print(f"Simple task -> {decision1.selected_model.name}")
    
    # Complex task - should route to powerful model
    decision2 = await router.route_task(
        "Design a distributed system architecture for a high-traffic e-commerce platform",
        task_type="architecture",
        priority="quality"
    )
    print(f"Complex task -> {decision2.selected_model.name}")
    
    # Code task - should route to specialist model if available
    decision3 = await router.route_task(
        "Refactor this Python code to improve performance and maintainability",
        task_type="code",
        priority="balanced"
    )
    print(f"Code task -> {decision3.selected_model.name}")
    
    # Print routing stats
    stats = router.get_routing_stats()
    print(f"\nRouting Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
