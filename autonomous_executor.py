"""
Autonomous Execution System

Provides autonomous agent execution capabilities:
- Self-directed task execution
- Quality monitoring and validation
- Multi-round processing with many changes per round
- Adaptive strategy selection
- Progress tracking and reporting
- Error recovery and retries
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


class ExecutionStatus(Enum):
    """Status of autonomous execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class ExecutionStrategy(Enum):
    """Strategy for autonomous execution"""
    SINGLE_PASS = "single_pass"  # One iteration
    ITERATIVE = "iterative"  # Multiple iterations until goal
    BATCH_PARALLEL = "batch_parallel"  # Process many changes in parallel
    ADAPTIVE = "adaptive"  # Adapt strategy based on results
    AGGRESSIVE = "aggressive"  # Maximum changes per round


@dataclass
class ExecutionConstraints:
    """Constraints for autonomous execution"""
    max_iterations: int = 10
    time_limit: float = 3600.0  # seconds
    quality_threshold: float = 0.85
    changes_per_round: int = 10
    max_retries: int = 3
    parallel_execution: bool = True


@dataclass
class ExecutionMetrics:
    """Metrics for execution monitoring"""
    iteration: int = 0
    changes_made: int = 0
    errors_encountered: int = 0
    quality_score: float = 0.0
    time_elapsed: float = 0.0
    success_rate: float = 0.0


@dataclass
class ExecutionResult:
    """Result from autonomous execution"""
    goal: str
    status: ExecutionStatus
    metrics: ExecutionMetrics
    outputs: List[Any] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    insights: Dict[str, Any] = field(default_factory=dict)


class AutonomousExecutor:
    """
    Autonomous Execution System
    
    Enables agents to execute tasks autonomously with:
    - Self-directed planning
    - Quality monitoring
    - Multi-round processing (10+ changes per round)
    - Adaptive strategies
    - Error recovery
    - Progress tracking
    """
    
    def __init__(
        self,
        agents: List[Any],
        changes_per_round: int = 10,
        max_iterations: int = 10,
        quality_threshold: float = 0.85,
        parallel_execution: bool = True,
        quality_monitor: Optional[Any] = None
    ):
        """
        Initialize autonomous executor.
        
        Args:
            agents: List of agents to use
            changes_per_round: Number of changes to process per round
            max_iterations: Maximum iterations
            quality_threshold: Minimum quality score
            parallel_execution: Enable parallel processing
            quality_monitor: Optional quality monitor
        """
        self.agents = agents
        self.changes_per_round = changes_per_round
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.parallel_execution = parallel_execution
        self.quality_monitor = quality_monitor
        
        self.execution_history: List[ExecutionResult] = []
        self.current_execution: Optional[ExecutionResult] = None
        
        print(f"✓ Autonomous Executor initialized")
        print(f"  Agents: {len(agents)}")
        print(f"  Changes per round: {changes_per_round}")
        print(f"  Max iterations: {max_iterations}")
        print(f"  Quality threshold: {quality_threshold}")
    
    def execute_autonomously(
        self,
        goal: str,
        constraints: Optional[ExecutionConstraints] = None,
        strategy: ExecutionStrategy = ExecutionStrategy.ADAPTIVE,
        monitoring: bool = True
    ) -> ExecutionResult:
        """
        Execute a goal autonomously.
        
        Args:
            goal: Goal to achieve
            constraints: Execution constraints
            strategy: Execution strategy
            monitoring: Enable monitoring
            
        Returns:
            Execution result
        """
        if constraints is None:
            constraints = ExecutionConstraints(
                max_iterations=self.max_iterations,
                quality_threshold=self.quality_threshold,
                changes_per_round=self.changes_per_round,
                parallel_execution=self.parallel_execution
            )
        
        print(f"\n🚀 Autonomous Execution Started")
        print(f"  Goal: {goal[:100]}...")
        print(f"  Strategy: {strategy.value}")
        print(f"  Changes per round: {constraints.changes_per_round}")
        
        start_time = time.time()
        metrics = ExecutionMetrics()
        outputs = []
        errors = []
        
        # Create result
        result = ExecutionResult(
            goal=goal,
            status=ExecutionStatus.RUNNING,
            metrics=metrics,
            outputs=outputs,
            errors=errors
        )
        
        self.current_execution = result
        
        try:
            # Decompose goal into tasks
            tasks = self._decompose_goal(goal, constraints.changes_per_round)
            print(f"  ✓ Decomposed into {len(tasks)} tasks")
            
            # Execute based on strategy
            if strategy == ExecutionStrategy.BATCH_PARALLEL:
                self._execute_batch_parallel(tasks, constraints, metrics, outputs, errors)
            
            elif strategy == ExecutionStrategy.ITERATIVE:
                self._execute_iterative(tasks, constraints, metrics, outputs, errors)
            
            elif strategy == ExecutionStrategy.AGGRESSIVE:
                self._execute_aggressive(tasks, constraints, metrics, outputs, errors)
            
            elif strategy == ExecutionStrategy.ADAPTIVE:
                self._execute_adaptive(tasks, constraints, metrics, outputs, errors)
            
            else:
                self._execute_single_pass(tasks, constraints, metrics, outputs, errors)
            
            # Calculate final metrics
            metrics.time_elapsed = time.time() - start_time
            metrics.success_rate = (metrics.changes_made - metrics.errors_encountered) / max(metrics.changes_made, 1)
            
            # Determine status
            if metrics.quality_score >= constraints.quality_threshold:
                result.status = ExecutionStatus.COMPLETED
            else:
                result.status = ExecutionStatus.FAILED
            
            print(f"\n  ✓ Execution completed")
            print(f"  Status: {result.status.value}")
            print(f"  Iterations: {metrics.iteration}")
            print(f"  Changes: {metrics.changes_made}")
            print(f"  Quality: {metrics.quality_score:.2f}")
            print(f"  Time: {metrics.time_elapsed:.2f}s")
        
        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.errors.append(str(e))
            print(f"\n  ✗ Execution failed: {e}")
        
        self.execution_history.append(result)
        self.current_execution = None
        
        return result
    
    def _decompose_goal(self, goal: str, max_tasks: int) -> List[str]:
        """Decompose goal into tasks"""
        # Simple decomposition - in practice, use reasoning agent
        tasks = []
        
        # Try to use reasoning agent if available
        for agent in self.agents:
            if hasattr(agent, 'agent_type') and 'reasoning' in agent.agent_type.lower():
                if hasattr(agent, 'decompose_problem'):
                    try:
                        decomposition = agent.decompose_problem(goal, max_depth=1)
                        if isinstance(decomposition, dict) and 'subtasks' in decomposition:
                            tasks = decomposition['subtasks'][:max_tasks]
                        break
                    except:
                        pass
        
        # Fallback: simple task list
        if not tasks:
            task_keywords = [
                "analyze", "design", "implement", "test", "optimize",
                "document", "deploy", "monitor", "validate", "refine"
            ]
            tasks = [f"{keyword} {goal}" for keyword in task_keywords[:max_tasks]]
        
        return tasks
    
    def _execute_single_pass(
        self,
        tasks: List[str],
        constraints: ExecutionConstraints,
        metrics: ExecutionMetrics,
        outputs: List[Any],
        errors: List[str]
    ) -> None:
        """Execute tasks in a single pass"""
        metrics.iteration = 1
        
        for task in tasks:
            if metrics.changes_made >= constraints.changes_per_round:
                break
            
            result = self._execute_task(task, metrics, errors)
            if result:
                outputs.append(result)
                metrics.changes_made += 1
        
        metrics.quality_score = self._assess_quality(outputs)
    
    def _execute_iterative(
        self,
        tasks: List[str],
        constraints: ExecutionConstraints,
        metrics: ExecutionMetrics,
        outputs: List[Any],
        errors: List[str]
    ) -> None:
        """Execute tasks iteratively until goal or limit"""
        while metrics.iteration < constraints.max_iterations:
            metrics.iteration += 1
            
            print(f"\n  Iteration {metrics.iteration}/{constraints.max_iterations}")
            
            round_outputs = []
            for task in tasks:
                if metrics.changes_made >= constraints.changes_per_round * metrics.iteration:
                    break
                
                result = self._execute_task(task, metrics, errors)
                if result:
                    round_outputs.append(result)
                    outputs.append(result)
                    metrics.changes_made += 1
            
            # Assess quality
            metrics.quality_score = self._assess_quality(outputs)
            print(f"    Quality: {metrics.quality_score:.2f}")
            
            # Check if goal achieved
            if metrics.quality_score >= constraints.quality_threshold:
                print(f"    ✓ Quality threshold reached")
                break
    
    def _execute_batch_parallel(
        self,
        tasks: List[str],
        constraints: ExecutionConstraints,
        metrics: ExecutionMetrics,
        outputs: List[Any],
        errors: List[str]
    ) -> None:
        """Execute tasks in parallel batches"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        batch_size = constraints.changes_per_round
        total_batches = (len(tasks) + batch_size - 1) // batch_size
        
        for batch_idx in range(min(total_batches, constraints.max_iterations)):
            metrics.iteration = batch_idx + 1
            
            print(f"\n  Batch {metrics.iteration}/{min(total_batches, constraints.max_iterations)}")
            
            batch_start = batch_idx * batch_size
            batch_end = min(batch_start + batch_size, len(tasks))
            batch_tasks = tasks[batch_start:batch_end]
            
            # Execute batch in parallel
            with ThreadPoolExecutor(max_workers=min(len(batch_tasks), 10)) as executor:
                futures = {
                    executor.submit(self._execute_task, task, metrics, errors): task
                    for task in batch_tasks
                }
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        outputs.append(result)
                        metrics.changes_made += 1
            
            print(f"    Completed {len(batch_tasks)} tasks")
            
            # Assess quality
            metrics.quality_score = self._assess_quality(outputs)
            print(f"    Quality: {metrics.quality_score:.2f}")
            
            if metrics.quality_score >= constraints.quality_threshold:
                print(f"    ✓ Quality threshold reached")
                break
    
    def _execute_aggressive(
        self,
        tasks: List[str],
        constraints: ExecutionConstraints,
        metrics: ExecutionMetrics,
        outputs: List[Any],
        errors: List[str]
    ) -> None:
        """Execute maximum changes per round"""
        # Set aggressive limits
        aggressive_changes = constraints.changes_per_round * 2
        
        print(f"  Aggressive mode: {aggressive_changes} changes per round")
        
        # Use parallel execution with higher throughput
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        with ThreadPoolExecutor(max_workers=min(aggressive_changes, 20)) as executor:
            futures = {
                executor.submit(self._execute_task, task, metrics, errors): task
                for task in tasks[:aggressive_changes]
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    outputs.append(result)
                    metrics.changes_made += 1
        
        metrics.iteration = 1
        metrics.quality_score = self._assess_quality(outputs)
    
    def _execute_adaptive(
        self,
        tasks: List[str],
        constraints: ExecutionConstraints,
        metrics: ExecutionMetrics,
        outputs: List[Any],
        errors: List[str]
    ) -> None:
        """Adaptively choose execution strategy"""
        # Start with batch parallel
        initial_batch = min(5, len(tasks))
        
        print(f"  Adaptive: testing with {initial_batch} tasks")
        
        test_outputs = []
        test_errors = []
        test_metrics = ExecutionMetrics()
        
        for task in tasks[:initial_batch]:
            result = self._execute_task(task, test_metrics, test_errors)
            if result:
                test_outputs.append(result)
        
        success_rate = (initial_batch - len(test_errors)) / initial_batch
        
        print(f"  Success rate: {success_rate:.2f}")
        
        # Choose strategy based on success rate
        if success_rate > 0.8:
            print(f"  Using aggressive strategy")
            self._execute_aggressive(tasks, constraints, metrics, outputs, errors)
        elif success_rate > 0.5:
            print(f"  Using batch parallel strategy")
            self._execute_batch_parallel(tasks, constraints, metrics, outputs, errors)
        else:
            print(f"  Using iterative strategy")
            self._execute_iterative(tasks, constraints, metrics, outputs, errors)
    
    def _execute_task(
        self,
        task: str,
        metrics: ExecutionMetrics,
        errors: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Execute a single task"""
        # Select best agent for task
        agent = self._select_agent(task)
        
        if not agent:
            errors.append(f"No agent available for task: {task}")
            metrics.errors_encountered += 1
            return None
        
        try:
            # Execute task
            if hasattr(agent, 'process_request'):
                result = agent.process_request(task)
                return {
                    'task': task,
                    'result': result,
                    'agent': agent.agent_name if hasattr(agent, 'agent_name') else 'unknown'
                }
            else:
                return {
                    'task': task,
                    'result': f'Simulated execution by {getattr(agent, "agent_name", "agent")}',
                    'agent': getattr(agent, 'agent_name', 'unknown')
                }
        
        except Exception as e:
            errors.append(f"Error executing {task}: {str(e)}")
            metrics.errors_encountered += 1
            return None
    
    def _select_agent(self, task: str) -> Optional[Any]:
        """Select best agent for task"""
        # Simple selection - return first agent
        # In practice, analyze task and match to agent capabilities
        return self.agents[0] if self.agents else None
    
    def _assess_quality(self, outputs: List[Any]) -> float:
        """Assess quality of outputs"""
        if not outputs:
            return 0.0
        
        if self.quality_monitor:
            try:
                return self.quality_monitor.assess(outputs)
            except:
                pass
        
        # Simple quality assessment
        successful = sum(1 for o in outputs if o and 'error' not in str(o).lower())
        return successful / len(outputs) if outputs else 0.0
    
    def execute_rounds(
        self,
        tasks: List[str],
        strategy: ExecutionStrategy = ExecutionStrategy.BATCH_PARALLEL
    ) -> ExecutionResult:
        """
        Execute multiple rounds of tasks.
        
        Args:
            tasks: List of tasks to execute
            strategy: Execution strategy
            
        Returns:
            Execution result
        """
        goal = f"Execute {len(tasks)} tasks"
        
        constraints = ExecutionConstraints(
            max_iterations=(len(tasks) + self.changes_per_round - 1) // self.changes_per_round,
            changes_per_round=self.changes_per_round,
            parallel_execution=self.parallel_execution
        )
        
        return self.execute_autonomously(goal, constraints, strategy)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_history:
            return {'total_executions': 0}
        
        return {
            'total_executions': len(self.execution_history),
            'successful': sum(1 for r in self.execution_history if r.status == ExecutionStatus.COMPLETED),
            'failed': sum(1 for r in self.execution_history if r.status == ExecutionStatus.FAILED),
            'avg_iterations': sum(r.metrics.iteration for r in self.execution_history) / len(self.execution_history),
            'avg_changes': sum(r.metrics.changes_made for r in self.execution_history) / len(self.execution_history),
            'avg_quality': sum(r.metrics.quality_score for r in self.execution_history) / len(self.execution_history),
            'avg_time': sum(r.metrics.time_elapsed for r in self.execution_history) / len(self.execution_history)
        }


# Demo usage
if __name__ == "__main__":
    print("🚀 Autonomous Executor Demo\n")
    
    # Create mock agent
    class MockAgent:
        def __init__(self, name):
            self.agent_name = name
            self.agent_type = "mock"
        
        def process_request(self, request, **kwargs):
            time.sleep(0.1)  # Simulate work
            return {
                'result': f'Completed: {request}',
                'agent': self.agent_name
            }
    
    # Create agents
    agents = [MockAgent(f"agent_{i}") for i in range(3)]
    
    # Initialize executor
    executor = AutonomousExecutor(
        agents=agents,
        changes_per_round=10,
        max_iterations=5,
        quality_threshold=0.85,
        parallel_execution=True
    )
    
    print(f"\n{'='*80}")
    print("Test 1: Batch Parallel Execution")
    print(f"{'='*80}\n")
    
    result = executor.execute_autonomously(
        goal="Build complete system",
        strategy=ExecutionStrategy.BATCH_PARALLEL
    )
    
    print(f"\n{'='*80}")
    print("Test 2: Aggressive Execution (20+ changes)")
    print(f"{'='*80}\n")
    
    result = executor.execute_autonomously(
        goal="Optimize entire codebase",
        constraints=ExecutionConstraints(
            changes_per_round=20,
            max_iterations=3,
            parallel_execution=True
        ),
        strategy=ExecutionStrategy.AGGRESSIVE
    )
    
    print(f"\n{'='*80}")
    print("Test 3: Adaptive Strategy")
    print(f"{'='*80}\n")
    
    result = executor.execute_autonomously(
        goal="Implement new features",
        strategy=ExecutionStrategy.ADAPTIVE
    )
    
    # Get statistics
    print(f"\n{'='*80}")
    print("Execution Statistics")
    print(f"{'='*80}\n")
    
    stats = executor.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n{'='*80}")
    print("✅ Demo complete!")
