"""
Base Agent class that integrates with the Context Engine.

All agents (GPT agents, custom agents, etc.) should inherit from this class
to ensure they have access to shared context and memory.
"""

from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import numpy as np

from context_engine import ContextEngine


class BaseAgent(ABC):
    """
    Base class for all agents that use the Context Engine.
    
    This provides:
    - Shared context access
    - Memory persistence
    - Context-aware responses
    - Agent coordination
    """
    
    # Shared context engine across all agents
    _shared_context: Optional[ContextEngine] = None
    
    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        use_shared_context: bool = True
    ):
        """
        Initialize base agent.
        
        Args:
            agent_name: Unique name for this agent
            agent_type: Type of agent (e.g., 'codex', 'ui_designer', 'reasoning')
            use_shared_context: Whether to use shared context across agents
        """
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.use_shared_context = use_shared_context
        
        # Initialize or use shared context
        if use_shared_context:
            if BaseAgent._shared_context is None:
                BaseAgent._shared_context = ContextEngine()
            self.context = BaseAgent._shared_context
        else:
            self.context = ContextEngine()
        
        # Register this agent in context
        self._register_agent()
    
    def _register_agent(self) -> None:
        """Register this agent in the context system."""
        agent_info = {
            'name': self.agent_name,
            'type': self.agent_type,
            'capabilities': self.get_capabilities()
        }
        
        self.agent_node = self.context.add_node(
            content=agent_info,
            node_type='agent',
            metadata={
                'agent_name': self.agent_name,
                'agent_type': self.agent_type,
                'active': True
            }
        )
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return list of agent capabilities.
        
        Returns:
            List of capability strings
        """
        pass
    
    @abstractmethod
    def process_request(self, request: str, **kwargs) -> Dict[str, Any]:
        """
        Process a request using context awareness.
        
        Args:
            request: The request to process
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with response and metadata
        """
        pass
    
    def add_to_context(
        self,
        content: Any,
        content_type: str = "generic",
        embedding: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Add content to the shared context.
        
        Args:
            content: Content to add
            content_type: Type of content
            embedding: Optional embedding vector
            metadata: Optional metadata
        
        Returns:
            The created node
        """
        meta = metadata or {}
        meta['added_by'] = self.agent_name
        
        node = self.context.add_node(
            content=content,
            node_type=content_type,
            embedding=embedding,
            metadata=meta
        )
        
        # Link to agent
        self.context.add_edge(
            self.agent_node.node_id,
            node.node_id,
            edge_type='created_by',
            weight=1.0
        )
        
        return node
    
    def recall_context(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        content_type: Optional[str] = None
    ) -> List:
        """
        Recall relevant context.
        
        Args:
            query_embedding: Query embedding
            k: Number of results
            content_type: Optional filter by content type
        
        Returns:
            List of relevant nodes with similarity scores
        """
        similar = self.context.find_similar_nodes(
            query_embedding,
            k=k * 2  # Get more then filter
        )
        
        if content_type:
            similar = [
                (node, sim) for node, sim in similar
                if node.node_type == content_type
            ]
        
        return similar[:k]
    
    def share_with_agent(
        self,
        target_agent_name: str,
        content: Any,
        relationship_type: str = "shared_info"
    ) -> None:
        """
        Share information with another agent.
        
        Args:
            target_agent_name: Name of target agent
            content: Content to share
            relationship_type: Type of relationship
        """
        # Find target agent node
        target_agent = None
        for node in self.context.nodes.values():
            if (node.node_type == 'agent' and 
                node.metadata.get('agent_name') == target_agent_name):
                target_agent = node
                break
        
        if not target_agent:
            raise ValueError(f"Agent {target_agent_name} not found")
        
        # Create content node
        content_node = self.add_to_context(
            content,
            content_type='shared_data',
            metadata={'shared_with': target_agent_name}
        )
        
        # Link to target agent
        self.context.add_edge(
            content_node.node_id,
            target_agent.node_id,
            edge_type=relationship_type,
            weight=1.0
        )
    
    def get_agent_history(self) -> List[Any]:
        """
        Get this agent's interaction history.
        
        Returns:
            List of nodes created by this agent
        """
        neighbors = self.context.get_neighbors(
            self.agent_node.node_id,
            edge_type='created_by'
        )
        
        # Sort by creation time
        neighbors.sort(key=lambda n: n.created_at)
        return neighbors
    
    def collaborate_with(self, other_agent_name: str) -> None:
        """
        Establish collaboration with another agent.
        
        Args:
            other_agent_name: Name of agent to collaborate with
        """
        # Find other agent
        for node in self.context.nodes.values():
            if (node.node_type == 'agent' and 
                node.metadata.get('agent_name') == other_agent_name):
                # Create collaboration edge
                self.context.add_edge(
                    self.agent_node.node_id,
                    node.node_id,
                    edge_type='collaborates_with',
                    weight=1.0,
                    directed=False
                )
                break
    
    def get_collaborators(self) -> List[str]:
        """
        Get names of agents this agent collaborates with.
        
        Returns:
            List of collaborator agent names
        """
        collaborators = self.context.get_neighbors(
            self.agent_node.node_id,
            edge_type='collaborates_with'
        )
        
        return [
            node.metadata.get('agent_name')
            for node in collaborators
            if node.node_type == 'agent'
        ]
    
    def get_context_stats(self) -> Dict[str, Any]:
        """
        Get context statistics relevant to this agent.
        
        Returns:
            Dictionary with statistics
        """
        all_stats = self.context.get_statistics()
        my_history = self.get_agent_history()
        
        return {
            'agent_name': self.agent_name,
            'agent_type': self.agent_type,
            'items_created': len(my_history),
            'total_context_nodes': all_stats['n_nodes'],
            'total_relationships': all_stats['n_edges'],
            'collaborators': self.get_collaborators()
        }
    
    @classmethod
    def get_shared_context(cls) -> Optional[ContextEngine]:
        """
        Get the shared context engine.
        
        Returns:
            Shared ContextEngine instance or None
        """
        return cls._shared_context
    
    @classmethod
    def reset_shared_context(cls) -> None:
        """Reset the shared context (useful for testing)."""
        cls._shared_context = None
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name={self.agent_name}, type={self.agent_type})"
