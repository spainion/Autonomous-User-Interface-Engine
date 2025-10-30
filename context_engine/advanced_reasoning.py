"""
Advanced Reasoning System with Chain-of-Thought, Tree-of-Thought, and Planning.

Features:
- Chain-of-Thought reasoning
- Tree-of-Thought exploration
- Multi-step planning
- Reasoning verification
- Confidence scoring
"""

from typing import List, Dict, Any, Optional, Tuple, Callable
import numpy as np
from dataclasses import dataclass
from enum import Enum
import json


class ReasoningStrategy(Enum):
    """Different reasoning strategies."""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHT = "tree_of_thought"
    DIRECT = "direct"
    ITERATIVE_REFINEMENT = "iterative_refinement"


@dataclass
class ReasoningStep:
    """Represents a single reasoning step."""
    step_number: int
    description: str
    input_state: Dict[str, Any]
    output_state: Dict[str, Any]
    confidence: float
    reasoning: str
    alternatives: List[str] = None


@dataclass
class ThoughtNode:
    """Node in a tree-of-thought exploration."""
    thought: str
    state: Dict[str, Any]
    score: float
    parent: Optional['ThoughtNode'] = None
    children: List['ThoughtNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class AdvancedReasoning:
    """
    Advanced reasoning system with multiple strategies.
    
    Features:
    - Chain-of-Thought: Step-by-step reasoning
    - Tree-of-Thought: Exploring multiple reasoning paths
    - Planning: Multi-step task decomposition
    - Verification: Reasoning validation
    - Confidence: Scoring reasoning quality
    """
    
    def __init__(
        self,
        default_strategy: ReasoningStrategy = ReasoningStrategy.CHAIN_OF_THOUGHT,
        max_reasoning_steps: int = 10,
        min_confidence: float = 0.7
    ):
        """
        Initialize advanced reasoning system.
        
        Args:
            default_strategy: Default reasoning strategy
            max_reasoning_steps: Maximum steps in reasoning chain
            min_confidence: Minimum confidence threshold
        """
        self.default_strategy = default_strategy
        self.max_reasoning_steps = max_reasoning_steps
        self.min_confidence = min_confidence
        
        # Reasoning history
        self.reasoning_history: List[Dict[str, Any]] = []
    
    def chain_of_thought(
        self,
        problem: str,
        context: Dict[str, Any],
        step_generator: Callable[[str, Dict[str, Any]], Tuple[str, Dict[str, Any], float]]
    ) -> List[ReasoningStep]:
        """
        Chain-of-Thought reasoning.
        
        Args:
            problem: Problem to solve
            context: Initial context
            step_generator: Function to generate next step
        
        Returns:
            List of reasoning steps
        """
        steps = []
        current_state = context.copy()
        
        for i in range(self.max_reasoning_steps):
            # Generate next step
            description, output_state, confidence = step_generator(problem, current_state)
            
            step = ReasoningStep(
                step_number=i + 1,
                description=description,
                input_state=current_state.copy(),
                output_state=output_state,
                confidence=confidence,
                reasoning=f"Step {i+1}: {description}"
            )
            
            steps.append(step)
            
            # Check if we've reached a solution
            if output_state.get('solved', False):
                break
            
            # Check confidence threshold
            if confidence < self.min_confidence:
                break
            
            current_state = output_state
        
        # Record in history
        self.reasoning_history.append({
            'problem': problem,
            'strategy': 'chain_of_thought',
            'steps': len(steps),
            'final_confidence': steps[-1].confidence if steps else 0,
            'solved': steps[-1].output_state.get('solved', False) if steps else False
        })
        
        return steps
    
    def tree_of_thought(
        self,
        problem: str,
        initial_state: Dict[str, Any],
        thought_generator: Callable[[str, Dict[str, Any]], List[Tuple[str, Dict[str, Any], float]]],
        max_depth: int = 3,
        beam_width: int = 3
    ) -> Tuple[ThoughtNode, List[ThoughtNode]]:
        """
        Tree-of-Thought reasoning with beam search.
        
        Args:
            problem: Problem to solve
            initial_state: Initial state
            thought_generator: Function to generate possible thoughts
            max_depth: Maximum tree depth
            beam_width: Number of best paths to keep
        
        Returns:
            (best_leaf_node, all_explored_nodes)
        """
        # Create root
        root = ThoughtNode(
            thought="Initial state",
            state=initial_state,
            score=1.0,
            parent=None
        )
        
        all_nodes = [root]
        current_beam = [root]
        
        for depth in range(max_depth):
            next_beam = []
            
            for node in current_beam:
                # Check if solved
                if node.state.get('solved', False):
                    return node, all_nodes
                
                # Generate possible next thoughts
                possibilities = thought_generator(problem, node.state)
                
                for thought, state, score in possibilities:
                    child = ThoughtNode(
                        thought=thought,
                        state=state,
                        score=score * node.score,  # Cumulative score
                        parent=node
                    )
                    node.children.append(child)
                    all_nodes.append(child)
                    next_beam.append(child)
            
            # Keep only top beam_width nodes
            next_beam.sort(key=lambda n: n.score, reverse=True)
            current_beam = next_beam[:beam_width]
            
            if not current_beam:
                break
        
        # Return best leaf
        best_node = max(current_beam, key=lambda n: n.score) if current_beam else root
        
        # Record in history
        self.reasoning_history.append({
            'problem': problem,
            'strategy': 'tree_of_thought',
            'nodes_explored': len(all_nodes),
            'best_score': best_node.score,
            'depth': depth + 1,
            'solved': best_node.state.get('solved', False)
        })
        
        return best_node, all_nodes
    
    def decompose_problem(
        self,
        problem: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Decompose a complex problem into subtasks.
        
        Args:
            problem: Complex problem
            context: Problem context
        
        Returns:
            List of subtasks with dependencies
        """
        # Simple heuristic-based decomposition
        # In practice, this would use an LLM
        
        subtasks = []
        
        # Check problem complexity
        problem_words = problem.lower().split()
        
        # Look for keywords indicating subtasks
        if "and" in problem_words or "then" in problem_words:
            # Multiple steps indicated
            parts = problem.replace(" and ", " SPLIT ").replace(" then ", " SPLIT ").split(" SPLIT ")
            for i, part in enumerate(parts):
                subtasks.append({
                    'id': i,
                    'description': part.strip(),
                    'dependencies': [i-1] if i > 0 else [],
                    'status': 'pending',
                    'priority': len(parts) - i
                })
        else:
            # Single task
            subtasks.append({
                'id': 0,
                'description': problem,
                'dependencies': [],
                'status': 'pending',
                'priority': 1
            })
        
        return subtasks
    
    def create_plan(
        self,
        problem: str,
        context: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a multi-step plan to solve a problem.
        
        Args:
            problem: Problem to solve
            context: Context information
            constraints: Optional constraints
        
        Returns:
            Execution plan
        """
        # Decompose problem
        subtasks = self.decompose_problem(problem, context)
        
        # Estimate resources
        total_complexity = sum(
            len(task['description'].split()) for task in subtasks
        )
        
        # Create plan
        plan = {
            'problem': problem,
            'subtasks': subtasks,
            'total_steps': len(subtasks),
            'estimated_complexity': total_complexity,
            'strategy': 'sequential',
            'constraints': constraints or {},
            'status': 'created'
        }
        
        # Add execution order
        execution_order = []
        completed = set()
        
        while len(completed) < len(subtasks):
            for task in subtasks:
                if task['id'] in completed:
                    continue
                
                # Check if dependencies are met
                deps_met = all(dep in completed for dep in task['dependencies'])
                
                if deps_met:
                    execution_order.append(task['id'])
                    completed.add(task['id'])
        
        plan['execution_order'] = execution_order
        
        return plan
    
    def verify_reasoning(
        self,
        steps: List[ReasoningStep],
        verification_fn: Optional[Callable[[ReasoningStep], bool]] = None
    ) -> Dict[str, Any]:
        """
        Verify reasoning steps for consistency and correctness.
        
        Args:
            steps: Reasoning steps to verify
            verification_fn: Optional custom verification function
        
        Returns:
            Verification results
        """
        if not steps:
            return {'valid': False, 'reason': 'No steps provided'}
        
        issues = []
        
        # Check step continuity
        for i in range(len(steps) - 1):
            current = steps[i]
            next_step = steps[i + 1]
            
            # Check if output state matches next input state
            # (simplified check)
            if current.confidence < self.min_confidence:
                issues.append(f"Step {i+1} has low confidence: {current.confidence}")
        
        # Check final step
        final_step = steps[-1]
        if not final_step.output_state.get('solved', False):
            issues.append("Final step does not indicate a solution")
        
        # Custom verification
        if verification_fn:
            for i, step in enumerate(steps):
                if not verification_fn(step):
                    issues.append(f"Step {i+1} failed custom verification")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'total_steps': len(steps),
            'avg_confidence': np.mean([s.confidence for s in steps]),
            'min_confidence': min(s.confidence for s in steps)
        }
    
    def calculate_reasoning_quality(
        self,
        steps: List[ReasoningStep]
    ) -> float:
        """
        Calculate overall quality score for reasoning chain.
        
        Args:
            steps: Reasoning steps
        
        Returns:
            Quality score (0-1)
        """
        if not steps:
            return 0.0
        
        # Factors:
        # 1. Average confidence
        avg_confidence = np.mean([s.confidence for s in steps])
        
        # 2. Consistency (variance in confidence)
        confidence_variance = np.var([s.confidence for s in steps])
        consistency_score = 1.0 - min(confidence_variance, 1.0)
        
        # 3. Completeness (solution reached)
        completeness = 1.0 if steps[-1].output_state.get('solved', False) else 0.5
        
        # 4. Efficiency (fewer steps is better)
        efficiency = max(0, 1.0 - (len(steps) / self.max_reasoning_steps))
        
        # Weighted combination
        quality = (
            0.4 * avg_confidence +
            0.2 * consistency_score +
            0.3 * completeness +
            0.1 * efficiency
        )
        
        return quality
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get statistics about reasoning history."""
        if not self.reasoning_history:
            return {}
        
        by_strategy = {}
        for entry in self.reasoning_history:
            strategy = entry['strategy']
            if strategy not in by_strategy:
                by_strategy[strategy] = []
            by_strategy[strategy].append(entry)
        
        stats = {
            'total_problems': len(self.reasoning_history),
            'by_strategy': {}
        }
        
        for strategy, entries in by_strategy.items():
            solved_count = sum(1 for e in entries if e.get('solved', False))
            stats['by_strategy'][strategy] = {
                'count': len(entries),
                'solved': solved_count,
                'success_rate': solved_count / len(entries) if entries else 0
            }
        
        return stats
