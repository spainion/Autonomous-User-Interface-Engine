"""
Enhanced Agent System with Network Capabilities and Batch Processing.

Provides:
- Network-enhanced agents with API integration
- Batch processing for multiple requests
- Iterative enhancement capabilities
- Cross-agent compatibility optimization
"""

from typing import List, Dict, Any, Optional, Callable
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from agents.base_agent import BaseAgent
from context_engine.network_engine import NetworkContextEngine
from context_engine.embedding_generator import EmbeddingGenerator


class EnhancedBaseAgent(BaseAgent):
    """
    Enhanced agent with network capabilities and batch processing.
    
    Features:
    - Network API integration
    - Batch request processing
    - Iterative enhancements
    - Advanced collaboration
    """
    
    # Shared network-enabled context
    _shared_network_context: Optional[NetworkContextEngine] = None
    
    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        use_shared_context: bool = True,
        enable_network: bool = True,
        batch_size: int = 10
    ):
        """
        Initialize enhanced agent.
        
        Args:
            agent_name: Agent name
            agent_type: Agent type
            use_shared_context: Use shared context
            enable_network: Enable network features
            batch_size: Default batch size for processing
        """
        # Initialize network context if needed
        if enable_network and use_shared_context:
            if EnhancedBaseAgent._shared_network_context is None:
                EnhancedBaseAgent._shared_network_context = NetworkContextEngine(
                    use_openai=True,
                    use_openrouter=True,
                    whitelist_all_domains=True
                )
            self.context = EnhancedBaseAgent._shared_network_context
            self.network_enabled = True
        else:
            self.network_enabled = False
        
        # Call parent init (will use existing context if set)
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.use_shared_context = use_shared_context
        
        if not hasattr(self, 'context'):
            from context_engine import ContextEngine
            if use_shared_context:
                if BaseAgent._shared_context is None:
                    BaseAgent._shared_context = ContextEngine()
                self.context = BaseAgent._shared_context
            else:
                self.context = ContextEngine()
        
        self._register_agent()
        
        self.batch_size = batch_size
        self.processing_history = []
    
    def process_batch(
        self,
        requests: List[str],
        parallel: bool = True,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Process multiple requests in batch.
        
        Args:
            requests: List of requests to process
            parallel: Whether to process in parallel
            **kwargs: Additional parameters for processing
        
        Returns:
            List of results
        """
        if parallel and len(requests) > 1:
            return self._process_parallel(requests, **kwargs)
        else:
            return self._process_sequential(requests, **kwargs)
    
    def _process_sequential(
        self,
        requests: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Process requests sequentially."""
        results = []
        
        for i, request in enumerate(requests):
            print(f"Processing {i+1}/{len(requests)}: {request[:50]}...")
            
            result = self.process_request(request, **kwargs)
            result['batch_index'] = i
            results.append(result)
            
            # Store in history
            self.processing_history.append({
                'request': request,
                'result': result,
                'timestamp': time.time()
            })
        
        return results
    
    def _process_parallel(
        self,
        requests: List[str],
        max_workers: int = 4,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Process requests in parallel."""
        results = [None] * len(requests)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(self.process_request, req, **kwargs): idx
                for idx, req in enumerate(requests)
            }
            
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    result = future.result()
                    result['batch_index'] = idx
                    results[idx] = result
                    
                    print(f"Completed {idx+1}/{len(requests)}")
                except Exception as e:
                    results[idx] = {
                        'error': str(e),
                        'batch_index': idx
                    }
        
        return results
    
    def iterative_enhance(
        self,
        initial_request: str,
        iterations: int = 3,
        enhancement_func: Optional[Callable] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Iteratively enhance a request through multiple passes.
        
        Args:
            initial_request: Starting request
            iterations: Number of enhancement iterations
            enhancement_func: Custom enhancement function
            **kwargs: Additional parameters
        
        Returns:
            List of results from each iteration
        """
        results = []
        current_request = initial_request
        
        for i in range(iterations):
            print(f"\n--- Iteration {i+1}/{iterations} ---")
            
            # Process current request
            result = self.process_request(current_request, **kwargs)
            results.append(result)
            
            # Enhance for next iteration
            if enhancement_func:
                current_request = enhancement_func(result, current_request)
            else:
                current_request = self._default_enhance(result, current_request)
            
            print(f"Enhanced request: {current_request[:60]}...")
        
        return results
    
    def _default_enhance(
        self,
        previous_result: Dict[str, Any],
        previous_request: str
    ) -> str:
        """Default enhancement strategy."""
        # Add context from previous result
        enhancement = f"Building on previous: {previous_request}. "
        enhancement += "Now enhance and optimize further."
        return enhancement
    
    def query_with_context(
        self,
        query: str,
        context_depth: int = 5,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Query with deep context retrieval and optional LLM enhancement.
        
        Args:
            query: Query string
            context_depth: Number of context items to retrieve
            use_llm: Use LLM to enhance response
        
        Returns:
            Query result with context
        """
        # Generate embedding
        embedding = EmbeddingGenerator.create_random_embedding(384)
        
        if self.network_enabled and hasattr(self.context, 'has_embeddings'):
            if self.context.has_embeddings:
                try:
                    embedding = self.context.embedding_gen.generate_embedding(query)
                except:
                    pass
        
        # Recall context
        context_items = self.recall_context(
            embedding,
            k=context_depth
        )
        
        result = {
            'query': query,
            'context_items': [
                {'content': str(node.content), 'similarity': float(sim)}
                for node, sim in context_items
            ],
            'context_count': len(context_items)
        }
        
        # Enhance with LLM if enabled
        if use_llm and self.network_enabled:
            if isinstance(self.context, NetworkContextEngine):
                context_text = "\n".join([
                    f"- {item['content'][:100]}"
                    for item in result['context_items'][:3]
                ])
                
                prompt = f"""Based on this context:
{context_text}

Answer this query: {query}

Provide a comprehensive, context-aware response."""
                
                llm_response = self.context.query_llm(prompt)
                result['llm_response'] = llm_response
        
        return result
    
    def collaborate_batch(
        self,
        agent_names: List[str],
        shared_data: Any
    ) -> Dict[str, Any]:
        """
        Share data with multiple agents at once.
        
        Args:
            agent_names: List of agent names to collaborate with
            shared_data: Data to share
        
        Returns:
            Collaboration results
        """
        results = {}
        
        for agent_name in agent_names:
            try:
                self.share_with_agent(agent_name, shared_data)
                results[agent_name] = {'success': True}
            except Exception as e:
                results[agent_name] = {'success': False, 'error': str(e)}
        
        return results
    
    def optimize_compatibility(self) -> Dict[str, Any]:
        """
        Optimize agent for cross-system compatibility.
        
        Returns:
            Optimization results
        """
        optimizations = {
            'agent_name': self.agent_name,
            'agent_type': self.agent_type,
            'network_enabled': self.network_enabled,
            'batch_capable': True,
            'iterative_capable': True,
            'context_depth': len(self.context) if self.context else 0,
            'collaborators': self.get_collaborators(),
            'processing_history_size': len(self.processing_history)
        }
        
        # Add network capabilities
        if self.network_enabled:
            optimizations['capabilities'] = [
                'network_api_calls',
                'real_time_embeddings',
                'llm_integration',
                'cloud_sync',
                'batch_processing',
                'parallel_execution',
                'iterative_enhancement'
            ]
        
        return optimizations
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about agent processing.
        
        Returns:
            Processing statistics
        """
        if not self.processing_history:
            return {'total_processed': 0}
        
        return {
            'total_processed': len(self.processing_history),
            'first_request': self.processing_history[0]['timestamp'],
            'last_request': self.processing_history[-1]['timestamp'],
            'avg_time_between': (
                (self.processing_history[-1]['timestamp'] - 
                 self.processing_history[0]['timestamp']) /
                max(len(self.processing_history) - 1, 1)
            )
        }
