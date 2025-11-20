"""
Prompt Optimizer for Autonomous UI Engine
Phase 6: Innovation - AI Features

Automatically improves and optimizes prompts for better LLM responses.
"""

import logging
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class OptimizationStrategy(Enum):
    """Prompt optimization strategies."""
    CLARITY = "clarity"           # Improve clarity and specificity
    STRUCTURE = "structure"       # Add structure and formatting
    CONTEXT = "context"           # Enhance context and examples
    CONSTRAINTS = "constraints"   # Add constraints and guidelines
    CHAIN_OF_THOUGHT = "cot"     # Add reasoning steps
    FEW_SHOT = "few_shot"        # Add examples


@dataclass
class PromptImprovement:
    """Represents a prompt improvement suggestion."""
    original_prompt: str
    optimized_prompt: str
    improvements: List[str]
    strategy_used: OptimizationStrategy
    confidence_score: float
    estimated_improvement: float  # 0-1 scale


@dataclass
class PromptAnalysis:
    """Analysis of a prompt's quality."""
    clarity_score: float          # 0-1
    specificity_score: float      # 0-1
    structure_score: float        # 0-1
    context_score: float          # 0-1
    overall_score: float          # 0-1
    issues: List[str]
    suggestions: List[str]


class PromptOptimizer:
    """
    Automatically optimizes prompts for better LLM performance.
    """
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initialize the prompt optimizer.
        
        Args:
            llm_client: Optional LLM client for advanced optimization
        """
        self.llm_client = llm_client
        self.optimization_history: List[Dict[str, Any]] = []
        
    async def optimize(
        self,
        prompt: str,
        strategy: Optional[OptimizationStrategy] = None,
        target_task: Optional[str] = None
    ) -> PromptImprovement:
        """
        Optimize a prompt using specified or automatic strategy.
        
        Args:
            prompt: The original prompt to optimize
            strategy: Optional specific optimization strategy
            target_task: Optional description of intended task
            
        Returns:
            PromptImprovement with optimized version and analysis
        """
        try:
            logger.info(f"Optimizing prompt: {prompt[:100]}...")
            
            # Analyze current prompt
            analysis = await self._analyze_prompt(prompt)
            
            # Determine best strategy if not specified
            if strategy is None:
                strategy = self._select_optimization_strategy(analysis)
            
            # Apply optimization
            optimized_prompt = await self._apply_optimization(
                prompt, strategy, analysis, target_task
            )
            
            # Create improvement report
            improvement = PromptImprovement(
                original_prompt=prompt,
                optimized_prompt=optimized_prompt,
                improvements=self._identify_improvements(prompt, optimized_prompt, analysis),
                strategy_used=strategy,
                confidence_score=self._calculate_confidence(analysis, strategy),
                estimated_improvement=self._estimate_improvement(analysis)
            )
            
            # Log optimization
            self._log_optimization(improvement)
            
            logger.info(f"Prompt optimized using {strategy.value} strategy")
            return improvement
            
        except Exception as e:
            logger.error(f"Error optimizing prompt: {e}")
            return PromptImprovement(
                original_prompt=prompt,
                optimized_prompt=prompt,
                improvements=[f"Error: {str(e)}"],
                strategy_used=strategy or OptimizationStrategy.CLARITY,
                confidence_score=0.0,
                estimated_improvement=0.0
            )
    
    async def _analyze_prompt(self, prompt: str) -> PromptAnalysis:
        """Analyze prompt quality across multiple dimensions."""
        # Clarity score
        clarity_score = self._calculate_clarity_score(prompt)
        
        # Specificity score
        specificity_score = self._calculate_specificity_score(prompt)
        
        # Structure score
        structure_score = self._calculate_structure_score(prompt)
        
        # Context score
        context_score = self._calculate_context_score(prompt)
        
        # Overall score
        overall_score = (
            clarity_score + specificity_score + 
            structure_score + context_score
        ) / 4
        
        # Identify issues
        issues = self._identify_issues(
            prompt, clarity_score, specificity_score, 
            structure_score, context_score
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(issues)
        
        return PromptAnalysis(
            clarity_score=clarity_score,
            specificity_score=specificity_score,
            structure_score=structure_score,
            context_score=context_score,
            overall_score=overall_score,
            issues=issues,
            suggestions=suggestions
        )
    
    def _calculate_clarity_score(self, prompt: str) -> float:
        """Calculate how clear and unambiguous the prompt is."""
        score = 0.5  # Base score
        
        # Check for question marks (clear intent)
        if '?' in prompt:
            score += 0.1
        
        # Check for imperative verbs (clear instructions)
        imperative_verbs = ['create', 'generate', 'explain', 'describe', 'analyze', 'implement']
        if any(verb in prompt.lower() for verb in imperative_verbs):
            score += 0.2
        
        # Penalize if too short or too vague
        if len(prompt.split()) < 5:
            score -= 0.2
        
        # Check for vague words
        vague_words = ['something', 'anything', 'somehow', 'maybe', 'kind of']
        if any(word in prompt.lower() for word in vague_words):
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_specificity_score(self, prompt: str) -> float:
        """Calculate how specific the prompt is."""
        score = 0.5  # Base score
        
        # Check for specific numbers or constraints
        if re.search(r'\d+', prompt):
            score += 0.15
        
        # Check for specific requirements
        requirement_keywords = ['must', 'should', 'require', 'need', 'include']
        if any(word in prompt.lower() for word in requirement_keywords):
            score += 0.2
        
        # Check for specific technologies or domains
        if re.search(r'[A-Z][a-z]+(?:[A-Z][a-z]+)+', prompt):  # CamelCase (tech names)
            score += 0.15
        
        return max(0.0, min(1.0, score))
    
    def _calculate_structure_score(self, prompt: str) -> float:
        """Calculate how well-structured the prompt is."""
        score = 0.5  # Base score
        
        # Check for bullet points or numbered lists
        if re.search(r'(\n\s*[-*\d]+\.?\s)', prompt):
            score += 0.2
        
        # Check for sections or headers
        if re.search(r'(^|\n)#+\s|\*\*[^*]+\*\*', prompt):
            score += 0.15
        
        # Check for multiple sentences (better structure)
        sentences = prompt.split('.')
        if len(sentences) > 2:
            score += 0.15
        
        return max(0.0, min(1.0, score))
    
    def _calculate_context_score(self, prompt: str) -> float:
        """Calculate how much context the prompt provides."""
        score = 0.5  # Base score
        
        # Check for background information
        context_keywords = ['background', 'context', 'given', 'assume', 'scenario']
        if any(word in prompt.lower() for word in context_keywords):
            score += 0.2
        
        # Check for examples
        if 'example' in prompt.lower() or 'e.g.' in prompt.lower():
            score += 0.15
        
        # Check for role specification
        if 'you are' in prompt.lower() or 'act as' in prompt.lower():
            score += 0.15
        
        return max(0.0, min(1.0, score))
    
    def _identify_issues(
        self,
        prompt: str,
        clarity: float,
        specificity: float,
        structure: float,
        context: float
    ) -> List[str]:
        """Identify specific issues with the prompt."""
        issues = []
        
        if clarity < 0.6:
            issues.append("Prompt lacks clarity - consider using more specific verbs and clear instructions")
        
        if specificity < 0.6:
            issues.append("Prompt is too vague - add specific requirements and constraints")
        
        if structure < 0.6:
            issues.append("Prompt lacks structure - consider using bullet points or sections")
        
        if context < 0.6:
            issues.append("Insufficient context - provide background information and examples")
        
        if len(prompt.split()) < 10:
            issues.append("Prompt is too short - add more detail")
        
        return issues
    
    def _generate_suggestions(self, issues: List[str]) -> List[str]:
        """Generate actionable suggestions based on issues."""
        suggestions = []
        
        for issue in issues:
            if "clarity" in issue:
                suggestions.append("Use imperative verbs: 'Create...', 'Generate...', 'Explain...'")
            elif "vague" in issue or "specific" in issue:
                suggestions.append("Add specific requirements: formats, lengths, technologies, etc.")
            elif "structure" in issue:
                suggestions.append("Organize with sections: Background, Requirements, Constraints")
            elif "context" in issue:
                suggestions.append("Provide examples: 'For example...', 'Similar to...'")
        
        return suggestions
    
    def _select_optimization_strategy(
        self,
        analysis: PromptAnalysis
    ) -> OptimizationStrategy:
        """Select best optimization strategy based on analysis."""
        # Find the lowest scoring aspect
        scores = {
            OptimizationStrategy.CLARITY: analysis.clarity_score,
            OptimizationStrategy.STRUCTURE: analysis.structure_score,
            OptimizationStrategy.CONTEXT: analysis.context_score
        }
        
        # Return strategy for lowest scoring aspect
        return min(scores.items(), key=lambda x: x[1])[0]
    
    async def _apply_optimization(
        self,
        prompt: str,
        strategy: OptimizationStrategy,
        analysis: PromptAnalysis,
        target_task: Optional[str]
    ) -> str:
        """Apply specific optimization strategy to prompt."""
        if strategy == OptimizationStrategy.CLARITY:
            return self._optimize_clarity(prompt)
        elif strategy == OptimizationStrategy.STRUCTURE:
            return self._optimize_structure(prompt)
        elif strategy == OptimizationStrategy.CONTEXT:
            return self._optimize_context(prompt, target_task)
        elif strategy == OptimizationStrategy.CONSTRAINTS:
            return self._optimize_constraints(prompt)
        elif strategy == OptimizationStrategy.CHAIN_OF_THOUGHT:
            return self._optimize_chain_of_thought(prompt)
        elif strategy == OptimizationStrategy.FEW_SHOT:
            return self._optimize_few_shot(prompt)
        else:
            return prompt
    
    def _optimize_clarity(self, prompt: str) -> str:
        """Optimize prompt for clarity."""
        # Add clear instruction prefix if missing
        if not any(prompt.lower().startswith(verb) for verb in ['create', 'generate', 'explain', 'describe']):
            prompt = f"Please {prompt.lower()}"
        
        # Ensure proper capitalization
        prompt = prompt[0].upper() + prompt[1:]
        
        # Add period if missing
        if not prompt.endswith(('.', '?', '!')):
            prompt += '.'
        
        return prompt
    
    def _optimize_structure(self, prompt: str) -> str:
        """Optimize prompt structure."""
        sections = []
        
        # Add task section
        sections.append("## Task")
        sections.append(prompt)
        
        # Add requirements section
        sections.append("\n## Requirements")
        sections.append("- Provide detailed and accurate output")
        sections.append("- Follow best practices")
        sections.append("- Include explanations where appropriate")
        
        return '\n'.join(sections)
    
    def _optimize_context(self, prompt: str, target_task: Optional[str]) -> str:
        """Add context to prompt."""
        context_prefix = "You are an expert AI assistant. "
        
        if target_task:
            context_prefix += f"The user needs help with: {target_task}. "
        
        context_prefix += "\n\n"
        
        return context_prefix + prompt
    
    def _optimize_constraints(self, prompt: str) -> str:
        """Add constraints to prompt."""
        constraints = [
            "\n\nConstraints:",
            "- Be concise but comprehensive",
            "- Use clear, professional language",
            "- Provide examples when helpful"
        ]
        
        return prompt + '\n'.join(constraints)
    
    def _optimize_chain_of_thought(self, prompt: str) -> str:
        """Add chain-of-thought reasoning to prompt."""
        cot_instruction = (
            "\n\nPlease think through this step-by-step:\n"
            "1. First, analyze the requirements\n"
            "2. Then, consider different approaches\n"
            "3. Finally, provide your solution with reasoning"
        )
        
        return prompt + cot_instruction
    
    def _optimize_few_shot(self, prompt: str) -> str:
        """Add few-shot examples to prompt."""
        examples = (
            "\n\nExamples of good responses:\n"
            "- Clear and well-organized\n"
            "- Include relevant details\n"
            "- Provide practical examples\n\n"
            "Now, please respond to: "
        )
        
        return examples + prompt
    
    def _identify_improvements(
        self,
        original: str,
        optimized: str,
        analysis: PromptAnalysis
    ) -> List[str]:
        """Identify specific improvements made."""
        improvements = []
        
        if len(optimized) > len(original):
            improvements.append("Added more detail and context")
        
        if '\n' in optimized and '\n' not in original:
            improvements.append("Improved structure with sections")
        
        if analysis.clarity_score < 0.7:
            improvements.append("Enhanced clarity and specificity")
        
        if any(word in optimized.lower() for word in ['step', 'first', 'then', 'finally']):
            improvements.append("Added step-by-step guidance")
        
        return improvements if improvements else ["General improvements to prompt quality"]
    
    def _calculate_confidence(
        self,
        analysis: PromptAnalysis,
        strategy: OptimizationStrategy
    ) -> float:
        """Calculate confidence in optimization."""
        base_confidence = 0.7
        
        # Higher confidence if the original prompt had clear issues
        if analysis.overall_score < 0.5:
            base_confidence += 0.2
        
        return min(base_confidence, 1.0)
    
    def _estimate_improvement(self, analysis: PromptAnalysis) -> float:
        """Estimate how much the prompt will improve."""
        # Maximum improvement is inverse of current quality
        max_improvement = 1.0 - analysis.overall_score
        
        # Estimate we can achieve 70% of maximum improvement
        return max_improvement * 0.7
    
    def _log_optimization(self, improvement: PromptImprovement) -> None:
        """Log optimization for analytics."""
        self.optimization_history.append({
            "original_length": len(improvement.original_prompt),
            "optimized_length": len(improvement.optimized_prompt),
            "strategy": improvement.strategy_used.value,
            "confidence": improvement.confidence_score,
            "estimated_improvement": improvement.estimated_improvement
        })
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about optimizations."""
        if not self.optimization_history:
            return {"total_optimizations": 0}
        
        strategy_counts = {}
        for opt in self.optimization_history:
            strategy = opt["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        avg_improvement = sum(o["estimated_improvement"] for o in self.optimization_history) / len(self.optimization_history)
        
        return {
            "total_optimizations": len(self.optimization_history),
            "strategy_distribution": strategy_counts,
            "average_estimated_improvement": avg_improvement
        }


# Example usage
async def example_usage():
    """Example of using the prompt optimizer."""
    optimizer = PromptOptimizer()
    
    # Example 1: Vague prompt
    vague_prompt = "make something cool"
    improvement1 = await optimizer.optimize(vague_prompt)
    print(f"Original: {improvement1.original_prompt}")
    print(f"Optimized: {improvement1.optimized_prompt}")
    print(f"Improvements: {improvement1.improvements}\n")
    
    # Example 2: Unstructured prompt
    unstructured_prompt = "I need a function that processes data and returns results"
    improvement2 = await optimizer.optimize(
        unstructured_prompt,
        strategy=OptimizationStrategy.STRUCTURE
    )
    print(f"Original: {improvement2.original_prompt}")
    print(f"Optimized: {improvement2.optimized_prompt}\n")
    
    # Print stats
    stats = optimizer.get_optimization_stats()
    print(f"Optimization Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
