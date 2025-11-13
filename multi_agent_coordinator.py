"""
Multi-Agent Coordination System

Provides advanced coordination capabilities for multiple agents working together:
- Agent discovery and registration
- Collaborative problem solving
- Task distribution and load balancing
- Result aggregation and synthesis
- Conflict resolution
- Performance optimization
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


class CoordinationStrategy(Enum):
    """Coordination strategies for multi-agent execution"""
    SEQUENTIAL = "sequential"  # One after another
    PARALLEL = "parallel"  # All at once
    HIERARCHICAL = "hierarchical"  # Leader delegates to workers
    PIPELINE = "pipeline"  # Output of one becomes input of next
    CONSENSUS = "consensus"  # All agents must agree
    VOTING = "voting"  # Majority vote wins


class AgentRole(Enum):
    """Roles agents can play in coordination"""
    LEADER = "leader"
    WORKER = "worker"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    VALIDATOR = "validator"


@dataclass
class AgentCapabilityProfile:
    """Profile of agent capabilities"""
    agent_id: str
    agent_type: str
    capabilities: List[str]
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    availability: float = 1.0
    current_load: float = 0.0


@dataclass
class TaskAssignment:
    """Assignment of task to agent"""
    task_id: str
    agent_id: str
    task_description: str
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    estimated_time: float = 0.0
    status: str = "pending"


@dataclass
class CollaborativeResult:
    """Result from collaborative agent execution"""
    task_id: str
    strategy: CoordinationStrategy
    results: Dict[str, Any]
    consensus_score: float = 0.0
    execution_time: float = 0.0
    agents_involved: List[str] = field(default_factory=list)
    quality_score: float = 0.0


class MultiAgentCoordinator:
    """
    Multi-Agent Coordination System
    
    Manages multiple agents working together on complex tasks:
    - Automatic agent discovery
    - Intelligent task distribution
    - Multiple coordination strategies
    - Result synthesis
    - Performance optimization
    """
    
    def __init__(self, max_workers: int = 10):
        """Initialize multi-agent coordinator"""
        self.agents: Dict[str, Any] = {}
        self.agent_profiles: Dict[str, AgentCapabilityProfile] = {}
        self.task_assignments: Dict[str, TaskAssignment] = {}
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.coordination_history: List[CollaborativeResult] = []
        
        print(f"✓ Multi-Agent Coordinator initialized (max_workers={max_workers})")
    
    def register_agent(
        self,
        agent_id: str,
        agent: Any,
        capabilities: Optional[List[str]] = None
    ) -> AgentCapabilityProfile:
        """
        Register an agent with the coordinator.
        
        Args:
            agent_id: Unique identifier for agent
            agent: Agent instance
            capabilities: List of agent capabilities
            
        Returns:
            Agent capability profile
        """
        self.agents[agent_id] = agent
        
        # Get capabilities from agent if not provided
        if capabilities is None and hasattr(agent, 'get_capabilities'):
            capabilities = agent.get_capabilities()
        elif capabilities is None:
            capabilities = []
        
        # Create profile
        profile = AgentCapabilityProfile(
            agent_id=agent_id,
            agent_type=getattr(agent, 'agent_type', 'unknown'),
            capabilities=capabilities,
            performance_metrics={},
            availability=1.0,
            current_load=0.0
        )
        
        self.agent_profiles[agent_id] = profile
        
        print(f"  ✓ Registered agent '{agent_id}' with {len(capabilities)} capabilities")
        
        return profile
    
    def discover_agents(self) -> List[AgentCapabilityProfile]:
        """
        Discover all registered agents and their capabilities.
        
        Returns:
            List of agent profiles
        """
        return list(self.agent_profiles.values())
    
    def find_capable_agents(
        self,
        required_capabilities: List[str],
        min_availability: float = 0.5
    ) -> List[AgentCapabilityProfile]:
        """
        Find agents with required capabilities.
        
        Args:
            required_capabilities: List of required capabilities
            min_availability: Minimum availability threshold
            
        Returns:
            List of matching agent profiles
        """
        matching = []
        
        for profile in self.agent_profiles.values():
            if profile.availability < min_availability:
                continue
            
            # Check if agent has all required capabilities
            has_all = all(cap in profile.capabilities for cap in required_capabilities)
            
            if has_all:
                matching.append(profile)
        
        # Sort by current load (prefer less loaded agents)
        matching.sort(key=lambda p: p.current_load)
        
        return matching
    
    def solve_collaboratively(
        self,
        problem: str,
        required_agents: Optional[List[str]] = None,
        coordination_strategy: CoordinationStrategy = CoordinationStrategy.SEQUENTIAL,
        **kwargs
    ) -> CollaborativeResult:
        """
        Solve a problem collaboratively using multiple agents.
        
        Args:
            problem: Problem description
            required_agents: List of agent IDs to use
            coordination_strategy: How to coordinate agents
            **kwargs: Additional parameters
            
        Returns:
            Collaborative result
        """
        start_time = time.time()
        task_id = hashlib.md5(f"{problem}{time.time()}".encode()).hexdigest()[:8]
        
        print(f"\n🤝 Collaborative Problem Solving")
        print(f"  Task ID: {task_id}")
        print(f"  Strategy: {coordination_strategy.value}")
        print(f"  Problem: {problem[:100]}...")
        
        # Select agents
        if required_agents is None:
            # Auto-select based on capabilities
            agents_to_use = self._auto_select_agents(problem, kwargs)
        else:
            agents_to_use = [self.agents[aid] for aid in required_agents if aid in self.agents]
        
        if not agents_to_use:
            raise ValueError("No suitable agents found")
        
        print(f"  Agents: {[a.agent_name if hasattr(a, 'agent_name') else 'unknown' for a in agents_to_use]}")
        
        # Execute based on strategy
        if coordination_strategy == CoordinationStrategy.SEQUENTIAL:
            results = self._execute_sequential(agents_to_use, problem, kwargs)
        
        elif coordination_strategy == CoordinationStrategy.PARALLEL:
            results = self._execute_parallel(agents_to_use, problem, kwargs)
        
        elif coordination_strategy == CoordinationStrategy.PIPELINE:
            results = self._execute_pipeline(agents_to_use, problem, kwargs)
        
        elif coordination_strategy == CoordinationStrategy.CONSENSUS:
            results = self._execute_consensus(agents_to_use, problem, kwargs)
        
        else:
            results = self._execute_sequential(agents_to_use, problem, kwargs)
        
        execution_time = time.time() - start_time
        
        # Create result
        result = CollaborativeResult(
            task_id=task_id,
            strategy=coordination_strategy,
            results=results,
            execution_time=execution_time,
            agents_involved=[a.agent_name if hasattr(a, 'agent_name') else 'unknown' for a in agents_to_use],
            quality_score=self._calculate_quality(results)
        )
        
        self.coordination_history.append(result)
        
        print(f"  ✓ Completed in {execution_time:.2f}s")
        print(f"  ✓ Quality score: {result.quality_score:.2f}")
        
        return result
    
    def _auto_select_agents(
        self,
        problem: str,
        kwargs: Dict[str, Any]
    ) -> List[Any]:
        """Auto-select agents based on problem"""
        # Simple heuristic - select all available agents
        return list(self.agents.values())
    
    def _execute_sequential(
        self,
        agents: List[Any],
        problem: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agents sequentially"""
        results = {}
        current_input = problem
        
        for i, agent in enumerate(agents):
            agent_name = agent.agent_name if hasattr(agent, 'agent_name') else f'agent_{i}'
            
            try:
                if hasattr(agent, 'process_request'):
                    result = agent.process_request(current_input, **kwargs)
                else:
                    result = {'output': f'Agent {agent_name} processed: {current_input}'}
                
                results[agent_name] = result
                
                # Use result as input for next agent
                if isinstance(result, dict) and 'result' in result:
                    current_input = result['result']
                elif isinstance(result, dict) and 'output' in result:
                    current_input = result['output']
            
            except Exception as e:
                results[agent_name] = {'error': str(e)}
        
        return results
    
    def _execute_parallel(
        self,
        agents: List[Any],
        problem: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agents in parallel"""
        results = {}
        futures = {}
        
        # Submit all tasks
        for i, agent in enumerate(agents):
            agent_name = agent.agent_name if hasattr(agent, 'agent_name') else f'agent_{i}'
            
            if hasattr(agent, 'process_request'):
                future = self.executor.submit(agent.process_request, problem, **kwargs)
                futures[future] = agent_name
        
        # Collect results
        for future in as_completed(futures):
            agent_name = futures[future]
            try:
                results[agent_name] = future.result()
            except Exception as e:
                results[agent_name] = {'error': str(e)}
        
        return results
    
    def _execute_pipeline(
        self,
        agents: List[Any],
        problem: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agents in pipeline (output of one feeds next)"""
        results = {}
        current_input = problem
        
        for i, agent in enumerate(agents):
            agent_name = agent.agent_name if hasattr(agent, 'agent_name') else f'agent_{i}'
            
            try:
                if hasattr(agent, 'process_request'):
                    result = agent.process_request(current_input, **kwargs)
                else:
                    result = {'output': current_input}
                
                results[agent_name] = result
                
                # Extract output for next stage
                if isinstance(result, dict):
                    if 'result' in result:
                        current_input = result['result']
                    elif 'output' in result:
                        current_input = result['output']
                    else:
                        current_input = str(result)
            
            except Exception as e:
                results[agent_name] = {'error': str(e)}
                break
        
        # Add final output
        results['final_output'] = current_input
        
        return results
    
    def _execute_consensus(
        self,
        agents: List[Any],
        problem: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agents and reach consensus"""
        # Get all agent responses
        parallel_results = self._execute_parallel(agents, problem, kwargs)
        
        # Simple consensus - majority vote or averaging
        consensus_result = self._synthesize_results(parallel_results)
        
        return {
            'individual_results': parallel_results,
            'consensus': consensus_result,
            'agreement_score': self._calculate_agreement(parallel_results)
        }
    
    def _synthesize_results(self, results: Dict[str, Any]) -> Any:
        """Synthesize multiple agent results"""
        # Simple synthesis - return most common result or aggregate
        values = []
        for result in results.values():
            if isinstance(result, dict):
                if 'result' in result:
                    values.append(result['result'])
                elif 'output' in result:
                    values.append(result['output'])
        
        if not values:
            return results
        
        # Return first non-error result for simplicity
        return values[0] if values else None
    
    def _calculate_agreement(self, results: Dict[str, Any]) -> float:
        """Calculate agreement score among agents"""
        # Simplified - just check if results are similar
        if len(results) <= 1:
            return 1.0
        
        # Count non-error results
        valid_results = [r for r in results.values() if not (isinstance(r, dict) and 'error' in r)]
        
        if not valid_results:
            return 0.0
        
        return len(valid_results) / len(results)
    
    def _calculate_quality(self, results: Dict[str, Any]) -> float:
        """Calculate overall quality score"""
        if not results:
            return 0.0
        
        # Count successful results
        successful = sum(1 for r in results.values() if not (isinstance(r, dict) and 'error' in r))
        
        return successful / len(results) if len(results) > 0 else 0.0
    
    def distribute_tasks(
        self,
        tasks: List[str],
        load_balancing: bool = True
    ) -> List[TaskAssignment]:
        """
        Distribute tasks among available agents.
        
        Args:
            tasks: List of tasks to distribute
            load_balancing: Enable load balancing
            
        Returns:
            List of task assignments
        """
        assignments = []
        available_agents = [p for p in self.agent_profiles.values() if p.availability > 0.5]
        
        if not available_agents:
            raise ValueError("No available agents")
        
        for i, task in enumerate(tasks):
            # Select agent (round-robin or load-based)
            if load_balancing:
                agent = min(available_agents, key=lambda a: a.current_load)
            else:
                agent = available_agents[i % len(available_agents)]
            
            assignment = TaskAssignment(
                task_id=f"task_{i}",
                agent_id=agent.agent_id,
                task_description=task,
                priority=1
            )
            
            assignments.append(assignment)
            agent.current_load += 0.1  # Simulate load increase
        
        return assignments
    
    def execute_assignments(
        self,
        assignments: List[TaskAssignment],
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Execute task assignments.
        
        Args:
            assignments: List of task assignments
            parallel: Execute in parallel
            
        Returns:
            Dictionary of results by task_id
        """
        results = {}
        
        if parallel:
            futures = {}
            
            for assignment in assignments:
                agent = self.agents.get(assignment.agent_id)
                if agent and hasattr(agent, 'process_request'):
                    future = self.executor.submit(
                        agent.process_request,
                        assignment.task_description
                    )
                    futures[future] = assignment.task_id
            
            for future in as_completed(futures):
                task_id = futures[future]
                try:
                    results[task_id] = future.result()
                except Exception as e:
                    results[task_id] = {'error': str(e)}
        
        else:
            for assignment in assignments:
                agent = self.agents.get(assignment.agent_id)
                if agent and hasattr(agent, 'process_request'):
                    try:
                        results[assignment.task_id] = agent.process_request(
                            assignment.task_description
                        )
                    except Exception as e:
                        results[assignment.task_id] = {'error': str(e)}
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get coordination statistics"""
        return {
            'total_agents': len(self.agents),
            'total_coordinations': len(self.coordination_history),
            'average_execution_time': sum(r.execution_time for r in self.coordination_history) / len(self.coordination_history) if self.coordination_history else 0,
            'average_quality': sum(r.quality_score for r in self.coordination_history) / len(self.coordination_history) if self.coordination_history else 0,
            'strategies_used': list(set(r.strategy for r in self.coordination_history))
        }


# Demo usage
if __name__ == "__main__":
    print("🤝 Multi-Agent Coordinator Demo\n")
    
    # Create simple mock agents
    class MockAgent:
        def __init__(self, name, agent_type):
            self.agent_name = name
            self.agent_type = agent_type
        
        def get_capabilities(self):
            return [f'{self.agent_type}_task_1', f'{self.agent_type}_task_2']
        
        def process_request(self, request, **kwargs):
            return {
                'result': f'{self.agent_name} processed: {request}',
                'agent': self.agent_name
            }
    
    # Initialize coordinator
    coordinator = MultiAgentCoordinator(max_workers=5)
    
    # Create and register agents
    agent1 = MockAgent("codex", "code")
    agent2 = MockAgent("ui_designer", "ui")
    agent3 = MockAgent("reasoning", "logic")
    
    coordinator.register_agent("codex", agent1)
    coordinator.register_agent("ui", agent2)
    coordinator.register_agent("reasoning", agent3)
    
    print(f"\n{'='*80}")
    print("Testing Coordination Strategies")
    print(f"{'='*80}\n")
    
    # Test sequential
    result = coordinator.solve_collaboratively(
        problem="Build a web application",
        required_agents=["reasoning", "codex", "ui"],
        coordination_strategy=CoordinationStrategy.SEQUENTIAL
    )
    print(f"\nSequential result: {len(result.results)} agents")
    
    # Test parallel
    result = coordinator.solve_collaboratively(
        problem="Analyze system architecture",
        required_agents=["codex", "ui", "reasoning"],
        coordination_strategy=CoordinationStrategy.PARALLEL
    )
    print(f"Parallel result: {len(result.results)} agents")
    
    # Test pipeline
    result = coordinator.solve_collaboratively(
        problem="Create and deploy feature",
        required_agents=["reasoning", "codex", "ui"],
        coordination_strategy=CoordinationStrategy.PIPELINE
    )
    print(f"Pipeline result: {len(result.results)} stages")
    
    # Get statistics
    print(f"\n{'='*80}")
    print("Coordination Statistics")
    print(f"{'='*80}\n")
    
    stats = coordinator.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n{'='*80}")
    print("✅ Demo complete!")
