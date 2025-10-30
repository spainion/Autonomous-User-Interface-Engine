"""
Integration example showing how AI agents can use the Context Engine.

This demonstrates:
- Agent using context for memory
- Context-aware decision making
- Temporal relationship tracking
- Semantic query for relevant information
"""

from typing import List, Tuple, Optional
import numpy as np
from context_engine import ContextEngine
from context_engine.embedding_generator import EmbeddingGenerator


class ContextAwareAgent:
    """
    An AI agent that uses the Context Engine to maintain memory and context.
    
    This agent:
    - Stores all interactions in the context graph
    - Recalls relevant past context when processing new inputs
    - Builds relationships between related concepts
    - Maintains temporal ordering of events
    """
    
    def __init__(self, agent_name: str = "Agent"):
        """
        Initialize the context-aware agent.
        
        Args:
            agent_name: Name identifier for this agent
        """
        self.name = agent_name
        self.context = ContextEngine()
        self.last_interaction_id: Optional[str] = None
        print(f"✓ {self.name} initialized with Context Engine")
    
    def process_input(self, user_input: str, input_type: str = "message") -> dict:
        """
        Process user input with full context awareness.
        
        Args:
            user_input: The user's input text
            input_type: Type of input (message, query, command, etc.)
        
        Returns:
            Dictionary with response and context information
        """
        print(f"\n{'='*60}")
        print(f"{self.name} Processing: '{user_input}'")
        print(f"{'='*60}")
        
        # Generate random embedding for demo (in production, use real embeddings)
        embedding = EmbeddingGenerator.create_random_embedding(384)
        
        # Find relevant past context
        relevant_context = self._recall_relevant_context(embedding)
        
        # Store this input in context
        input_node = self.context.add_node(
            content=user_input,
            node_type=input_type,
            embedding=embedding,
            metadata={
                'agent': self.name,
                'interaction_number': len(self.context)
            }
        )
        
        # Link to previous interaction (temporal sequence)
        if self.last_interaction_id:
            self.context.add_edge(
                self.last_interaction_id,
                input_node.node_id,
                edge_type="temporal_next",
                weight=1.0
            )
        
        # Link to relevant context (semantic relationships)
        for ctx_node, similarity in relevant_context:
            if similarity > 0.5:  # Threshold for relevance
                self.context.add_edge(
                    input_node.node_id,
                    ctx_node.node_id,
                    edge_type="semantically_related",
                    weight=similarity
                )
        
        self.last_interaction_id = input_node.node_id
        
        # Generate response based on context
        response = self._generate_response(user_input, relevant_context)
        
        # Store response in context
        response_node = self.context.add_node(
            content=response,
            node_type="agent_response",
            embedding=EmbeddingGenerator.create_random_embedding(384),
            metadata={'agent': self.name}
        )
        
        # Link input to response
        self.context.add_edge(
            input_node.node_id,
            response_node.node_id,
            edge_type="response_to",
            weight=1.0
        )
        
        return {
            'response': response,
            'relevant_context': [
                {'content': node.content, 'similarity': sim}
                for node, sim in relevant_context
            ],
            'context_stats': self.context.get_statistics()
        }
    
    def _recall_relevant_context(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5
    ) -> List[Tuple]:
        """
        Recall relevant context from memory.
        
        Args:
            query_embedding: Embedding of current query
            k: Number of relevant items to recall
        
        Returns:
            List of (node, similarity_score) tuples
        """
        if len(self.context) == 0:
            return []
        
        similar = self.context.find_similar_nodes(
            query_embedding, 
            k=k, 
            threshold=0.3
        )
        
        if similar:
            print(f"\n📚 Recalled {len(similar)} relevant context items:")
            for node, sim in similar[:3]:  # Show top 3
                print(f"  • [{sim:.3f}] {node.content[:50]}...")
        
        return similar
    
    def _generate_response(
        self, 
        user_input: str, 
        context: List[Tuple]
    ) -> str:
        """
        Generate response based on input and context.
        
        In a real implementation, this would call an LLM with the context.
        For this demo, we return a context-aware acknowledgment.
        
        Args:
            user_input: The user's input
            context: Relevant context items
        
        Returns:
            Generated response string
        """
        if not context:
            return f"I understand you said: '{user_input}'. This is our first interaction!"
        
        # Reference the most relevant context
        most_relevant = context[0][0].content
        return (
            f"I understand '{user_input}'. "
            f"This relates to our earlier discussion about '{most_relevant[:40]}...'. "
            f"I have {len(context)} related items in my context."
        )
    
    def get_conversation_history(self) -> List[str]:
        """
        Get the full conversation history in temporal order.
        
        Returns:
            List of interaction contents in order
        """
        # Find all message nodes
        messages = [
            node for node in self.context.nodes.values()
            if node.node_type in ['message', 'agent_response']
        ]
        
        # Sort by creation time
        messages.sort(key=lambda n: n.created_at)
        
        return [msg.content for msg in messages]
    
    def find_related_topics(self, topic: str, k: int = 5) -> List[str]:
        """
        Find topics related to a given topic.
        
        Args:
            topic: Topic to search for
            k: Number of related topics to find
        
        Returns:
            List of related topic contents
        """
        embedding = EmbeddingGenerator.create_random_embedding(384)
        similar = self.context.find_similar_nodes(embedding, k=k)
        return [node.content for node, _ in similar]
    
    def summarize_context(self) -> dict:
        """
        Get a summary of the agent's context state.
        
        Returns:
            Dictionary with context summary
        """
        stats = self.context.get_statistics()
        
        # Get interaction count
        message_count = stats['node_types'].get('message', 0)
        response_count = stats['node_types'].get('agent_response', 0)
        
        return {
            'agent_name': self.name,
            'total_interactions': message_count + response_count,
            'user_messages': message_count,
            'agent_responses': response_count,
            'total_nodes': stats['n_nodes'],
            'total_relationships': stats['n_edges'],
            'node_types': stats['node_types'],
            'edge_types': stats['edge_types']
        }


def main():
    """Demonstrate the context-aware agent."""
    print("="*60)
    print("Context-Aware Agent Demo")
    print("="*60)
    
    # Create agent
    agent = ContextAwareAgent("ContextBot")
    
    # Simulate a conversation
    interactions = [
        "Hello! I'm interested in machine learning.",
        "Can you tell me about neural networks?",
        "What about deep learning specifically?",
        "How does this relate to AI?",
        "Thanks! Can we talk about Python programming?",
        "I want to build an AI application.",
        "What machine learning tools should I use?"  # Should recall earlier ML context
    ]
    
    print("\n" + "="*60)
    print("Starting Conversation")
    print("="*60)
    
    for i, user_input in enumerate(interactions, 1):
        result = agent.process_input(user_input, input_type="message")
        
        print(f"\n💬 User: {user_input}")
        print(f"🤖 {agent.name}: {result['response']}")
        
        if i % 3 == 0:  # Show stats every 3 interactions
            print(f"\n📊 Context Summary:")
            summary = agent.summarize_context()
            print(f"   Total nodes: {summary['total_nodes']}")
            print(f"   Relationships: {summary['total_relationships']}")
            print(f"   Node types: {summary['node_types']}")
    
    # Final summary
    print("\n" + "="*60)
    print("Final Context Summary")
    print("="*60)
    
    summary = agent.summarize_context()
    print(f"\n✓ Agent: {summary['agent_name']}")
    print(f"✓ Total Interactions: {summary['total_interactions']}")
    print(f"✓ User Messages: {summary['user_messages']}")
    print(f"✓ Agent Responses: {summary['agent_responses']}")
    print(f"✓ Total Context Nodes: {summary['total_nodes']}")
    print(f"✓ Total Relationships: {summary['total_relationships']}")
    print(f"\nNode Types: {summary['node_types']}")
    print(f"Edge Types: {summary['edge_types']}")
    
    # Demonstrate topic finding
    print("\n" + "="*60)
    print("Related Topics Query")
    print("="*60)
    
    print("\n🔍 Finding topics related to 'machine learning':")
    related = agent.find_related_topics("machine learning", k=3)
    for topic in related:
        print(f"   • {topic[:60]}...")
    
    print("\n" + "="*60)
    print("✓ Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
