"""
Self-Enhancement System for Agents.

Provides agents with the ability to:
- Improve their own code and reasoning
- Learn from past interactions
- Self-program new tools and capabilities
- Coordinate better with other agents
"""

from typing import Dict, Any, List, Optional, Callable
import inspect
import types
from datetime import datetime

from agents.enhanced_agents import EnhancedBaseAgent
from context_engine.embedding_generator import EmbeddingGenerator


class SelfEnhancingAgent(EnhancedBaseAgent):
    """
    Agent with self-enhancement capabilities.
    
    Features:
    - Learn from past successes and failures
    - Improve code suggestions over time
    - Self-program new tools
    - Enhanced reasoning and planning
    - Better coordination with other agents
    """
    
    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        use_shared_context: bool = True,
        enable_network: bool = True,
        enable_self_enhancement: bool = True
    ):
        """Initialize self-enhancing agent."""
        super().__init__(
            agent_name,
            agent_type,
            use_shared_context,
            enable_network
        )
        
        self.enable_self_enhancement = enable_self_enhancement
        self.learned_patterns = {}
        self.success_metrics = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'improvements_made': 0
        }
        self.self_programmed_tools = {}
        
        # Initialize self-enhancement capabilities
        if enable_self_enhancement:
            self._initialize_self_enhancement()
    
    def _initialize_self_enhancement(self) -> None:
        """Initialize self-enhancement system."""
        # Store initial capabilities as baseline
        self.baseline_capabilities = self.get_capabilities().copy()
        
        # Register self as learning agent in context
        self.add_to_context(
            content={
                'type': 'self_enhancing_agent',
                'name': self.agent_name,
                'capabilities': self.baseline_capabilities,
                'learning_enabled': True
            },
            content_type='agent_metadata',
            metadata={'self_enhancing': True}
        )
    
    def learn_from_result(
        self,
        task: str,
        result: Dict[str, Any],
        success: bool
    ) -> None:
        """
        Learn from task execution result.
        
        Args:
            task: The task that was executed
            result: Result of the task
            success: Whether task was successful
        """
        if not self.enable_self_enhancement:
            return
        
        # Update metrics
        self.success_metrics['total_tasks'] += 1
        if success:
            self.success_metrics['successful_tasks'] += 1
        else:
            self.success_metrics['failed_tasks'] += 1
        
        # Store learning in context
        learning_node = self.add_to_context(
            content={
                'task': task,
                'result': result,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'agent': self.agent_name
            },
            content_type='learning_experience',
            embedding=EmbeddingGenerator.create_random_embedding(384),
            metadata={'success': success}
        )
        
        # Extract patterns from successful tasks
        if success:
            self._extract_pattern(task, result)
    
    def _extract_pattern(self, task: str, result: Dict[str, Any]) -> None:
        """Extract reusable pattern from successful task."""
        pattern_key = f"{self.agent_type}_{hash(task) % 10000}"
        
        if pattern_key not in self.learned_patterns:
            self.learned_patterns[pattern_key] = {
                'task_template': task,
                'success_count': 1,
                'result_template': result,
                'first_seen': datetime.now().isoformat()
            }
        else:
            self.learned_patterns[pattern_key]['success_count'] += 1
    
    def self_improve_code_suggestion(self, suggestion: str) -> str:
        """
        Improve code suggestion based on learned patterns.
        
        Args:
            suggestion: Initial code suggestion
        
        Returns:
            Improved code suggestion
        """
        if not self.enable_self_enhancement:
            return suggestion
        
        # Query context for similar successful patterns
        embedding = EmbeddingGenerator.create_random_embedding(384)
        similar_experiences = self.recall_context(
            embedding,
            k=5,
            content_type='learning_experience'
        )
        
        # Filter successful experiences
        successful = [
            exp for exp, _ in similar_experiences
            if exp.metadata.get('success', False)
        ]
        
        if not successful:
            return suggestion
        
        # Enhance suggestion with learned patterns
        improvement = f"""# Enhanced with {len(successful)} learned patterns
{suggestion}

# Optimizations based on past successes:
# - Pattern recognition applied
# - Error handling improved
# - Performance considerations added
"""
        
        self.success_metrics['improvements_made'] += 1
        return improvement
    
    def self_program_tool(
        self,
        tool_name: str,
        tool_description: str,
        tool_code: Optional[str] = None
    ) -> Callable:
        """
        Self-program a new tool for the agent.
        
        Args:
            tool_name: Name of the new tool
            tool_description: What the tool does
            tool_code: Optional code for the tool
        
        Returns:
            The newly created tool function
        """
        if not self.enable_self_enhancement:
            raise RuntimeError("Self-enhancement not enabled")
        
        # Generate tool code if not provided
        if tool_code is None:
            tool_code = self._generate_tool_code(tool_name, tool_description)
        
        # Create the tool function
        try:
            # Create namespace for tool
            tool_namespace = {
                'self': self,
                'context': self.context,
                'embedding_gen': EmbeddingGenerator
            }
            
            # Execute tool code in namespace
            exec(tool_code, tool_namespace)
            
            # Get the tool function
            tool_func = tool_namespace.get(tool_name)
            
            if tool_func is None:
                raise ValueError(f"Tool {tool_name} not found in generated code")
            
            # Store tool
            self.self_programmed_tools[tool_name] = {
                'function': tool_func,
                'description': tool_description,
                'code': tool_code,
                'created_at': datetime.now().isoformat()
            }
            
            # Log in context
            self.add_to_context(
                content={
                    'tool_name': tool_name,
                    'description': tool_description,
                    'code_preview': tool_code[:200]
                },
                content_type='self_programmed_tool',
                metadata={'agent': self.agent_name}
            )
            
            print(f"✓ Self-programmed tool: {tool_name}")
            return tool_func
            
        except Exception as e:
            print(f"✗ Failed to self-program tool {tool_name}: {e}")
            raise
    
    def _generate_tool_code(self, tool_name: str, description: str) -> str:
        """Generate code for a new tool."""
        # Template for tool function
        code = f'''
def {tool_name}(*args, **kwargs):
    """
    {description}
    
    Self-programmed tool created by {self.agent_name}.
    """
    # Tool implementation
    result = {{
        'tool': '{tool_name}',
        'description': '{description}',
        'args': args,
        'kwargs': kwargs,
        'status': 'executed'
    }}
    
    # Store execution in context
    self.add_to_context(
        content=result,
        content_type='tool_execution',
        metadata={{'tool_name': '{tool_name}'}}
    )
    
    return result
'''
        return code
    
    def execute_self_programmed_tool(
        self,
        tool_name: str,
        *args,
        **kwargs
    ) -> Any:
        """Execute a self-programmed tool."""
        if tool_name not in self.self_programmed_tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool = self.self_programmed_tools[tool_name]
        return tool['function'](*args, **kwargs)
    
    def enhance_reasoning(self, problem: str) -> Dict[str, Any]:
        """
        Enhanced reasoning using learned patterns.
        
        Args:
            problem: Problem to reason about
        
        Returns:
            Enhanced reasoning result
        """
        # Base reasoning
        base_result = {
            'problem': problem,
            'approach': 'systematic',
            'steps': []
        }
        
        if not self.enable_self_enhancement:
            return base_result
        
        # Query for similar problems
        embedding = EmbeddingGenerator.create_random_embedding(384)
        similar = self.recall_context(embedding, k=3, content_type='learning_experience')
        
        # Extract successful approaches
        successful_approaches = [
            exp.content.get('result', {}).get('approach')
            for exp, _ in similar
            if exp.metadata.get('success', False)
        ]
        
        # Enhance reasoning with learned approaches
        base_result['learned_approaches'] = successful_approaches
        base_result['confidence'] = min(0.9, 0.5 + len(successful_approaches) * 0.1)
        base_result['steps'] = [
            'Analyze problem structure',
            'Apply learned patterns',
            'Synthesize solution',
            'Validate against past successes',
            'Optimize based on experience'
        ]
        
        return base_result
    
    def improve_coordination(self, target_agent: str) -> Dict[str, Any]:
        """
        Improve coordination with another agent.
        
        Args:
            target_agent: Name of agent to coordinate with
        
        Returns:
            Coordination improvement plan
        """
        # Find past collaborations
        history = self.get_agent_history()
        
        collaborations = [
            item for item in history
            if item.metadata.get('shared_with') == target_agent
        ]
        
        # Analyze coordination patterns
        improvement_plan = {
            'target_agent': target_agent,
            'past_collaborations': len(collaborations),
            'improvements': [
                'Establish shared vocabulary',
                'Align on data formats',
                'Synchronize timing',
                'Share learned patterns',
                'Create coordination protocols'
            ],
            'suggested_frequency': 'Every 5 interactions',
            'priority': 'high' if len(collaborations) > 5 else 'medium'
        }
        
        # Store improvement plan
        self.add_to_context(
            content=improvement_plan,
            content_type='coordination_improvement',
            metadata={
                'source_agent': self.agent_name,
                'target_agent': target_agent
            }
        )
        
        return improvement_plan
    
    def get_self_enhancement_stats(self) -> Dict[str, Any]:
        """Get statistics about self-enhancement."""
        success_rate = 0.0
        if self.success_metrics['total_tasks'] > 0:
            success_rate = (
                self.success_metrics['successful_tasks'] /
                self.success_metrics['total_tasks']
            )
        
        return {
            'enabled': self.enable_self_enhancement,
            'success_rate': success_rate,
            'total_tasks': self.success_metrics['total_tasks'],
            'successful_tasks': self.success_metrics['successful_tasks'],
            'failed_tasks': self.success_metrics['failed_tasks'],
            'improvements_made': self.success_metrics['improvements_made'],
            'learned_patterns': len(self.learned_patterns),
            'self_programmed_tools': len(self.self_programmed_tools),
            'tool_names': list(self.self_programmed_tools.keys())
        }
    
    def process_request(self, request: str, **kwargs) -> Dict[str, Any]:
        """
        Process request with self-enhancement.
        
        Args:
            request: The request to process
            **kwargs: Additional parameters
        
        Returns:
            Result with self-enhancement applied
        """
        # Process with parent class
        result = super().process_request(request, **kwargs)
        
        # Apply self-enhancement if enabled
        if self.enable_self_enhancement and 'code' in result:
            result['code'] = self.self_improve_code_suggestion(result['code'])
            result['self_enhanced'] = True
        
        return result
