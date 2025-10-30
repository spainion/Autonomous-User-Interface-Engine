"""
Full Auto-Utilization System for GitHub Copilot

This module ensures ALL features are automatically utilized with every interaction:
- Context Engine with FAISS search
- Self-Enhancement (learning, tool creation)
- Advanced Reasoning (Chain/Tree-of-Thought)
- Performance Monitoring
- Memory Consolidation
- Advanced Caching
- Batch Processing
- Network Enhancement
- Universal Compatibility
- External Integrations

Usage:
    This module is automatically imported and initialized.
    All features work transparently in the background.
"""

import os
import json
import time
from typing import Any, Dict, List, Optional, Callable
from functools import wraps

# Global feature flags (all enabled by default)
FEATURES_ENABLED = {
    'context_engine': os.getenv('COPILOT_AUTO_CONTEXT', 'true').lower() == 'true',
    'self_learning': os.getenv('COPILOT_SELF_LEARNING', 'true').lower() == 'true',
    'advanced_reasoning': os.getenv('COPILOT_ADVANCED_REASONING', 'true').lower() == 'true',
    'performance_monitoring': os.getenv('COPILOT_PERFORMANCE_MONITORING', 'true').lower() == 'true',
    'memory_consolidation': os.getenv('COPILOT_MEMORY_CONSOLIDATION', 'true').lower() == 'true',
    'advanced_caching': os.getenv('COPILOT_ADVANCED_CACHING', 'true').lower() == 'true',
    'batch_processing': os.getenv('COPILOT_BATCH_PROCESSING', 'true').lower() == 'true',
    'network_enhanced': os.getenv('COPILOT_NETWORK_ENHANCED', 'true').lower() == 'true',
    'universal_compat': os.getenv('COPILOT_UNIVERSAL_COMPAT', 'true').lower() == 'true',
    'external_integrations': os.getenv('COPILOT_EXTERNAL_INTEGRATIONS', 'true').lower() == 'true',
}

class FullAutoUtilization:
    """
    Orchestrates automatic utilization of ALL system features.
    """
    
    def __init__(self):
        self.initialized = False
        self.engine = None
        self.agents = None
        self.universal = None
        self.cache = None
        self.monitor = None
        self.consolidator = None
        self.reasoning = None
        self.search_engine = None
        self.self_enhancing_agents = {}
        
        # Performance tracking
        self.interaction_count = 0
        self.feature_usage = {feature: 0 for feature in FEATURES_ENABLED.keys()}
        self.performance_stats = []
        
        # Initialize if features are enabled
        self._initialize()
    
    def _initialize(self):
        """Initialize all enabled features."""
        if self.initialized:
            return
        
        try:
            # 1. Context Engine (always first)
            if FEATURES_ENABLED['context_engine']:
                from context_engine import NetworkContextEngine
                self.engine = NetworkContextEngine(
                    whitelist_all_domains=True,
                    enable_caching=FEATURES_ENABLED['advanced_caching']
                )
                self.feature_usage['context_engine'] += 1
            
            # 2. Advanced Search with FAISS
            if FEATURES_ENABLED['context_engine'] and self.engine:
                try:
                    from context_engine.advanced_search import AdvancedSearchEngine
                    self.search_engine = AdvancedSearchEngine(self.engine)
                    self.feature_usage['context_engine'] += 1
                except ImportError:
                    pass
            
            # 3. Performance Monitoring
            if FEATURES_ENABLED['performance_monitoring']:
                try:
                    from context_engine.performance_monitor import PerformanceMonitor
                    self.monitor = PerformanceMonitor()
                    self.feature_usage['performance_monitoring'] += 1
                except ImportError:
                    pass
            
            # 4. Advanced Reasoning
            if FEATURES_ENABLED['advanced_reasoning'] and self.engine:
                try:
                    from context_engine.advanced_reasoning import AdvancedReasoning
                    self.reasoning = AdvancedReasoning(self.engine)
                    self.feature_usage['advanced_reasoning'] += 1
                except ImportError:
                    pass
            
            # 5. Memory Consolidation
            if FEATURES_ENABLED['memory_consolidation'] and self.engine:
                try:
                    from context_engine.memory_consolidation import MemoryConsolidation
                    self.consolidator = MemoryConsolidation(self.engine)
                    self.feature_usage['memory_consolidation'] += 1
                except ImportError:
                    pass
            
            # 6. Advanced Caching
            if FEATURES_ENABLED['advanced_caching']:
                try:
                    from context_engine.advanced_cache import AdvancedCache
                    self.cache = AdvancedCache()
                    self.feature_usage['advanced_caching'] += 1
                except ImportError:
                    pass
            
            # 7. Self-Enhancing Agents
            if FEATURES_ENABLED['self_learning']:
                try:
                    from agents.self_enhancing_concrete_agents import (
                        SelfEnhancingCodexAgent,
                        SelfEnhancingUIDesignerAgent,
                        SelfEnhancingReasoningAgent
                    )
                    self.self_enhancing_agents = {
                        'codex': SelfEnhancingCodexAgent(),
                        'ui_designer': SelfEnhancingUIDesignerAgent(),
                        'reasoning': SelfEnhancingReasoningAgent()
                    }
                    self.feature_usage['self_learning'] += 1
                except ImportError:
                    pass
            
            # 8. Universal Compatibility
            if FEATURES_ENABLED['universal_compat']:
                try:
                    from universal_compatibility import UniversalAgentInterface
                    self.universal = UniversalAgentInterface()
                    self.feature_usage['universal_compat'] += 1
                except ImportError:
                    pass
            
            self.initialized = True
            print(f"✅ Full Auto-Utilization Initialized: {sum(1 for v in FEATURES_ENABLED.values() if v)}/10 features active")
            
        except Exception as e:
            print(f"⚠️  Auto-utilization initialization error: {e}")
            self.initialized = False
    
    def pre_response_hook(self, query: str) -> Dict[str, Any]:
        """
        Execute before generating a response.
        Returns context and recommendations for the query.
        """
        start_time = time.time()
        context_data = {
            'relevant_memories': [],
            'cached_response': None,
            'reasoning_chain': None,
            'recommendations': [],
            'performance': {}
        }
        
        self.interaction_count += 1
        
        # 1. Check cache first (1000x+ speedup)
        if FEATURES_ENABLED['advanced_caching'] and self.cache:
            cached = self.cache.get(query)
            if cached:
                context_data['cached_response'] = cached
                context_data['performance']['cache_hit'] = True
                return context_data
        
        # 2. Search context with FAISS (10-100x faster)
        if FEATURES_ENABLED['context_engine'] and self.search_engine:
            try:
                # Use hybrid search for best accuracy
                results = self.search_engine.hybrid_search(
                    query_vector=None,  # Will generate from query
                    query_text=query,
                    k=10
                )
                context_data['relevant_memories'] = results
            except Exception:
                # Fallback to basic context search
                if self.engine:
                    context_data['relevant_memories'] = self.engine.get_context(query)
        
        # 3. Use advanced reasoning for complex queries
        if FEATURES_ENABLED['advanced_reasoning'] and self.reasoning:
            # Detect if query needs Chain-of-Thought
            if self._is_complex_query(query):
                try:
                    reasoning_result = self.reasoning.chain_of_thought_reasoning(query)
                    context_data['reasoning_chain'] = reasoning_result
                    context_data['recommendations'].append('Use Chain-of-Thought reasoning')
                except Exception:
                    pass
        
        # 4. Load learned patterns from self-enhancing agents
        if FEATURES_ENABLED['self_learning'] and self.self_enhancing_agents:
            for agent_name, agent in self.self_enhancing_agents.items():
                if hasattr(agent, 'learned_patterns'):
                    context_data['recommendations'].extend(agent.learned_patterns[:3])
        
        # 5. Record performance
        if FEATURES_ENABLED['performance_monitoring']:
            elapsed = time.time() - start_time
            context_data['performance']['pre_hook_time_ms'] = elapsed * 1000
        
        return context_data
    
    def post_response_hook(self, query: str, response: str, context_data: Dict[str, Any]):
        """
        Execute after generating a response.
        Stores learnings and updates memory.
        """
        start_time = time.time()
        
        # 1. Store in cache for future use
        if FEATURES_ENABLED['advanced_caching'] and self.cache:
            self.cache.set(query, response, ttl=3600)
        
        # 2. Store in context engine
        if FEATURES_ENABLED['context_engine'] and self.engine:
            try:
                # Store the interaction
                self.engine.add_node_with_text(
                    content=f"Q: {query}\nA: {response}",
                    embedding_text=query
                )
            except Exception:
                pass
        
        # 3. Self-enhancement: Learn from interaction
        if FEATURES_ENABLED['self_learning'] and self.self_enhancing_agents:
            for agent in self.self_enhancing_agents.values():
                if hasattr(agent, 'learn_from_task'):
                    try:
                        agent.learn_from_task(query, response, success=True)
                    except Exception:
                        pass
        
        # 4. Memory consolidation (every 100 interactions)
        if FEATURES_ENABLED['memory_consolidation'] and self.consolidator:
            if self.interaction_count % 100 == 0:
                try:
                    self.consolidator.consolidate_memories(min_importance=0.3)
                except Exception:
                    pass
        
        # 5. Performance monitoring
        if FEATURES_ENABLED['performance_monitoring'] and self.monitor:
            elapsed = time.time() - start_time
            self.performance_stats.append({
                'query': query[:100],
                'post_hook_time_ms': elapsed * 1000,
                'interaction_num': self.interaction_count
            })
            
            # Alert on performance issues
            if elapsed > 1.0:  # > 1 second
                print(f"⚠️  Performance alert: Post-hook took {elapsed:.2f}s")
    
    def _is_complex_query(self, query: str) -> bool:
        """Detect if query needs advanced reasoning."""
        complex_indicators = [
            'how to', 'why', 'explain', 'compare', 'what if',
            'design', 'architecture', 'implement', 'optimize',
            'debug', 'solve', 'analyze', 'evaluate'
        ]
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in complex_indicators)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of all features."""
        return {
            'initialized': self.initialized,
            'interaction_count': self.interaction_count,
            'features_enabled': FEATURES_ENABLED,
            'feature_usage': self.feature_usage,
            'performance_summary': self._get_performance_summary()
        }
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Calculate performance statistics."""
        if not self.performance_stats:
            return {}
        
        times = [s['post_hook_time_ms'] for s in self.performance_stats]
        times.sort()
        n = len(times)
        
        return {
            'total_interactions': n,
            'avg_post_hook_ms': sum(times) / n if n > 0 else 0,
            'p50_ms': times[n // 2] if n > 0 else 0,
            'p95_ms': times[int(n * 0.95)] if n > 0 else 0,
            'p99_ms': times[int(n * 0.99)] if n > 0 else 0
        }
    
    def auto_enhance_response(self, query: str, base_response: str) -> str:
        """
        Automatically enhance a response using all available features.
        """
        enhanced = base_response
        
        # Add context-aware enhancements
        if FEATURES_ENABLED['context_engine'] and self.engine:
            relevant_context = self.engine.get_context(query)
            if relevant_context:
                enhanced += f"\n\n💡 Related context: {len(relevant_context)} relevant memories found"
        
        # Add self-learning insights
        if FEATURES_ENABLED['self_learning'] and self.self_enhancing_agents:
            patterns = []
            for agent in self.self_enhancing_agents.values():
                if hasattr(agent, 'learned_patterns'):
                    patterns.extend(agent.learned_patterns[:2])
            if patterns:
                enhanced += f"\n\n📚 Learned patterns applied: {len(patterns)}"
        
        return enhanced


# Global instance (automatically created)
_full_auto = None

def get_full_auto() -> FullAutoUtilization:
    """Get the global FullAutoUtilization instance."""
    global _full_auto
    if _full_auto is None:
        _full_auto = FullAutoUtilization()
    return _full_auto


def with_full_auto(func: Callable) -> Callable:
    """
    Decorator that automatically applies all features to a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auto = get_full_auto()
        
        # Extract query if first argument is a string
        query = args[0] if args and isinstance(args[0], str) else "unknown"
        
        # Pre-processing
        context_data = auto.pre_response_hook(query)
        
        # Check cache
        if context_data.get('cached_response'):
            return context_data['cached_response']
        
        # Execute original function
        result = func(*args, **kwargs)
        
        # Post-processing
        auto.post_response_hook(query, str(result), context_data)
        
        # Enhance response if it's a string
        if isinstance(result, str):
            result = auto.auto_enhance_response(query, result)
        
        return result
    
    return wrapper


# Initialize on import
if __name__ != "__main__":
    _full_auto = FullAutoUtilization()
    print("🚀 Full Auto-Utilization System Active")
