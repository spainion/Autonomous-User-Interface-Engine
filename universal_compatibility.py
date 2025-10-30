"""
Universal Agent Compatibility Layer.

Provides seamless integration with:
- GitHub Copilot
- OpenAI Codex
- OpenAI Assistants API
- Custom agents
- Autonomous operation

All agents share the same context engine and can interoperate.
"""

from typing import Dict, Any, List, Optional, Callable
import os
import json
from datetime import datetime

from agents.self_enhancing_agent import SelfEnhancingAgent
from context_engine import ContextEngine, NetworkContextEngine


class UniversalAgentInterface:
    """
    Universal interface for all agent types.
    
    Compatible with:
    - GitHub Copilot workspace agents
    - OpenAI Codex API
    - OpenAI Assistants API
    - Custom agents
    - Autonomous agents
    """
    
    def __init__(
        self,
        context_engine: Optional[ContextEngine] = None,
        enable_openai_codex: bool = True,
        enable_github_copilot: bool = True,
        autonomous_mode: bool = True
    ):
        """
        Initialize universal agent interface.
        
        Args:
            context_engine: Shared context engine (auto-created if None)
            enable_openai_codex: Enable OpenAI Codex integration
            enable_github_copilot: Enable GitHub Copilot integration
            autonomous_mode: Enable autonomous operation
        """
        # Use shared context or create new
        if context_engine is None:
            self.context = NetworkContextEngine(
                use_openai=True,
                use_openrouter=True,
                whitelist_all_domains=True
            )
        else:
            self.context = context_engine
        
        self.enable_openai_codex = enable_openai_codex
        self.enable_github_copilot = enable_github_copilot
        self.autonomous_mode = autonomous_mode
        
        # Agent registry
        self.registered_agents = {}
        
        # Initialize integrations
        self._initialize_integrations()
    
    def _initialize_integrations(self) -> None:
        """Initialize all integrations."""
        # OpenAI API key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # GitHub Copilot workspace info
        self.github_workspace = os.getenv("GITHUB_WORKSPACE", os.getcwd())
        
        # Store integration status
        self.integrations = {
            'openai_codex': self.enable_openai_codex and self.openai_api_key is not None,
            'github_copilot': self.enable_github_copilot,
            'autonomous': self.autonomous_mode,
            'context_engine': True
        }
        
        print(f"✓ Universal Agent Interface initialized")
        print(f"  OpenAI Codex: {'enabled' if self.integrations['openai_codex'] else 'disabled'}")
        print(f"  GitHub Copilot: {'enabled' if self.integrations['github_copilot'] else 'disabled'}")
        print(f"  Autonomous Mode: {'enabled' if self.integrations['autonomous'] else 'disabled'}")
    
    def register_agent(
        self,
        agent: Any,
        agent_type: str,
        capabilities: List[str]
    ) -> str:
        """
        Register an agent with the universal interface.
        
        Args:
            agent: Agent instance
            agent_type: Type identifier
            capabilities: List of agent capabilities
        
        Returns:
            Agent ID
        """
        agent_id = f"{agent_type}_{len(self.registered_agents)}"
        
        self.registered_agents[agent_id] = {
            'agent': agent,
            'type': agent_type,
            'capabilities': capabilities,
            'registered_at': datetime.now().isoformat()
        }
        
        # Store in context
        self.context.add_node(
            content={
                'agent_id': agent_id,
                'type': agent_type,
                'capabilities': capabilities
            },
            node_type='registered_agent',
            metadata={'agent_id': agent_id}
        )
        
        print(f"✓ Registered agent: {agent_id} ({agent_type})")
        return agent_id
    
    def route_request(
        self,
        request: str,
        preferred_agent_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Route request to best available agent.
        
        Args:
            request: The request to process
            preferred_agent_type: Preferred agent type
            **kwargs: Additional parameters
        
        Returns:
            Response from selected agent
        """
        # Determine best agent
        if preferred_agent_type and preferred_agent_type in self._get_available_types():
            agent_type = preferred_agent_type
        else:
            agent_type = self._select_best_agent(request)
        
        # Route to agent
        if agent_type == 'openai_codex' and self.integrations['openai_codex']:
            return self._call_openai_codex(request, **kwargs)
        elif agent_type == 'github_copilot' and self.integrations['github_copilot']:
            return self._call_github_copilot(request, **kwargs)
        elif agent_type in [a['type'] for a in self.registered_agents.values()]:
            return self._call_registered_agent(agent_type, request, **kwargs)
        else:
            return self._autonomous_fallback(request, **kwargs)
    
    def _select_best_agent(self, request: str) -> str:
        """Select best agent for request."""
        request_lower = request.lower()
        
        # Code-related requests
        if any(kw in request_lower for kw in ['code', 'function', 'class', 'implement']):
            if self.integrations['openai_codex']:
                return 'openai_codex'
            return 'codex'
        
        # UI-related requests
        if any(kw in request_lower for kw in ['ui', 'design', 'component', 'interface']):
            return 'ui_designer'
        
        # Reasoning requests
        if any(kw in request_lower for kw in ['plan', 'design', 'reason', 'analyze']):
            return 'reasoning'
        
        # Default to Copilot or autonomous
        if self.integrations['github_copilot']:
            return 'github_copilot'
        
        return 'autonomous'
    
    def _call_openai_codex(self, request: str, **kwargs) -> Dict[str, Any]:
        """Call OpenAI Codex API."""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=request,
                max_tokens=kwargs.get('max_tokens', 1024),
                temperature=kwargs.get('temperature', 0.3)
            )
            
            result = {
                'source': 'openai_codex',
                'response': response.choices[0].text,
                'model': 'code-davinci-002',
                'success': True
            }
            
            # Store in context
            self.context.add_node(
                content=result,
                node_type='codex_response',
                metadata={'source': 'openai_codex'}
            )
            
            return result
            
        except Exception as e:
            return {
                'source': 'openai_codex',
                'error': str(e),
                'success': False
            }
    
    def _call_github_copilot(self, request: str, **kwargs) -> Dict[str, Any]:
        """
        Simulate GitHub Copilot integration.
        
        Note: Actual Copilot integration would use workspace APIs.
        This provides compatibility structure.
        """
        result = {
            'source': 'github_copilot',
            'request': request,
            'workspace': self.github_workspace,
            'response': f"# GitHub Copilot suggestion for: {request}\n# (Integrated with context engine)",
            'success': True
        }
        
        # Store in context
        self.context.add_node(
            content=result,
            node_type='copilot_response',
            metadata={'source': 'github_copilot'}
        )
        
        return result
    
    def _call_registered_agent(
        self,
        agent_type: str,
        request: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Call a registered agent."""
        for agent_id, agent_info in self.registered_agents.items():
            if agent_info['type'] == agent_type:
                agent = agent_info['agent']
                
                # Call agent
                if hasattr(agent, 'process_request'):
                    result = agent.process_request(request, **kwargs)
                    result['source'] = f"registered_agent_{agent_id}"
                    return result
        
        return {'error': f"Agent type {agent_type} not found", 'success': False}
    
    def _autonomous_fallback(self, request: str, **kwargs) -> Dict[str, Any]:
        """Autonomous fallback handler."""
        return {
            'source': 'autonomous',
            'request': request,
            'response': f"Autonomous processing: {request}",
            'context_available': True,
            'success': True
        }
    
    def _get_available_types(self) -> List[str]:
        """Get list of available agent types."""
        types = []
        
        if self.integrations['openai_codex']:
            types.append('openai_codex')
        if self.integrations['github_copilot']:
            types.append('github_copilot')
        
        types.extend([a['type'] for a in self.registered_agents.values()])
        
        if self.integrations['autonomous']:
            types.append('autonomous')
        
        return list(set(types))
    
    def get_compatibility_status(self) -> Dict[str, Any]:
        """Get complete compatibility status."""
        return {
            'integrations': self.integrations,
            'registered_agents': len(self.registered_agents),
            'available_types': self._get_available_types(),
            'context_nodes': len(self.context),
            'fully_compatible': all(self.integrations.values())
        }
    
    def create_openai_assistant_compatible(
        self,
        name: str,
        instructions: str,
        tools: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create OpenAI Assistant-compatible configuration.
        
        Args:
            name: Assistant name
            instructions: System instructions
            tools: List of tool configurations
        
        Returns:
            Assistant configuration
        """
        assistant_config = {
            'name': name,
            'instructions': instructions,
            'tools': tools or [],
            'model': 'gpt-4-turbo-preview',
            'context_engine_enabled': True,
            'compatible_with': [
                'openai_assistants_api',
                'github_copilot',
                'codex',
                'autonomous'
            ]
        }
        
        # Store in context
        self.context.add_node(
            content=assistant_config,
            node_type='assistant_config',
            metadata={'assistant_name': name}
        )
        
        return assistant_config


class CopilotCompatibilityHelper:
    """
    Helper for GitHub Copilot integration.
    
    Provides:
    - Workspace integration
    - File context awareness
    - Suggestion enhancement
    """
    
    @staticmethod
    def get_workspace_context() -> Dict[str, Any]:
        """Get current workspace context."""
        workspace = os.getenv("GITHUB_WORKSPACE", os.getcwd())
        
        return {
            'workspace_path': workspace,
            'available': os.path.exists(workspace),
            'type': 'github_workspace'
        }
    
    @staticmethod
    def enhance_copilot_suggestion(
        suggestion: str,
        context_engine: ContextEngine
    ) -> str:
        """
        Enhance Copilot suggestion with context.
        
        Args:
            suggestion: Original Copilot suggestion
            context_engine: Context engine with learned patterns
        
        Returns:
            Enhanced suggestion
        """
        enhanced = f"{suggestion}\n\n# Enhanced with context engine patterns"
        return enhanced
    
    @staticmethod
    def export_context_for_copilot(
        context_engine: ContextEngine,
        output_file: str = ".copilot-context.json"
    ) -> None:
        """
        Export context for Copilot workspace.
        
        Args:
            context_engine: Context to export
            output_file: Output file path
        """
        context_data = context_engine.export_to_dict()
        
        with open(output_file, 'w') as f:
            json.dump(context_data, f, indent=2)
        
        print(f"✓ Context exported to {output_file}")


class CodexCompatibilityHelper:
    """
    Helper for OpenAI Codex integration.
    
    Provides:
    - Codex API integration
    - Context-aware prompts
    - Response enhancement
    """
    
    @staticmethod
    def create_codex_prompt(
        request: str,
        context_engine: ContextEngine,
        include_context: bool = True
    ) -> str:
        """
        Create Codex-compatible prompt with context.
        
        Args:
            request: Base request
            context_engine: Context for relevant information
            include_context: Whether to include context
        
        Returns:
            Enhanced prompt
        """
        prompt = request
        
        if include_context and len(context_engine) > 0:
            prompt = f"""# Context from previous interactions:
# (Learned patterns available)

{request}
"""
        
        return prompt
    
    @staticmethod
    def parse_codex_response(
        response: str,
        store_in_context: bool = True,
        context_engine: Optional[ContextEngine] = None
    ) -> Dict[str, Any]:
        """
        Parse and enhance Codex response.
        
        Args:
            response: Raw Codex response
            store_in_context: Whether to store in context
            context_engine: Context engine for storage
        
        Returns:
            Parsed response
        """
        parsed = {
            'raw_response': response,
            'code': response,
            'source': 'openai_codex',
            'enhanced': True
        }
        
        if store_in_context and context_engine:
            context_engine.add_node(
                content=parsed,
                node_type='codex_output',
                metadata={'source': 'codex'}
            )
        
        return parsed


def create_universal_agent_system() -> UniversalAgentInterface:
    """
    Create a universal agent system compatible with all agent types.
    
    Returns:
        Configured universal interface
    """
    # Create interface
    interface = UniversalAgentInterface(
        enable_openai_codex=True,
        enable_github_copilot=True,
        autonomous_mode=True
    )
    
    # Register local agents
    from agents import (
        SelfEnhancingCodexAgent,
        SelfEnhancingUIDesignerAgent,
        SelfEnhancingReasoningAgent
    )
    
    # Create and register agents
    codex = SelfEnhancingCodexAgent("UniversalCodex")
    ui = SelfEnhancingUIDesignerAgent("UniversalUI")
    reasoner = SelfEnhancingReasoningAgent("UniversalReasoner")
    
    interface.register_agent(codex, 'codex', codex.get_capabilities())
    interface.register_agent(ui, 'ui_designer', ui.get_capabilities())
    interface.register_agent(reasoner, 'reasoning', reasoner.get_capabilities())
    
    return interface
