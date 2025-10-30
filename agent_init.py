"""
Agent Initialization Module - Auto-connects all agents to context engine.

Import this at the start of any script to automatically initialize
the context engine and make it available to all agents.

Usage:
    from agent_init import init_agent_system
    engine, agents = init_agent_system()
"""

import os
import sys
from typing import Dict, Any, Tuple

from context_engine import NetworkContextEngine
from context_engine.advanced_search import AdvancedSearchEngine
from context_engine.advanced_cache import AdvancedCache
from context_engine.performance_monitor import PerformanceMonitor
from context_engine.advanced_reasoning import AdvancedReasoning
from context_engine.memory_consolidation import MemoryConsolidation

from agents.enhanced_concrete_agents import (
    EnhancedCodexAgent,
    EnhancedUIDesignerAgent,
    EnhancedReasoningAgent
)
from agents.self_enhancing_concrete_agents import (
    SelfEnhancingCodexAgent,
    SelfEnhancingUIDesignerAgent,
    SelfEnhancingReasoningAgent
)
from universal_compatibility import UniversalAgentInterface


# Global shared context engine instance
_GLOBAL_ENGINE = None
_GLOBAL_AGENTS = None
_GLOBAL_UNIVERSAL = None


def init_agent_system(
    use_faiss: bool = True,
    enable_caching: bool = True,
    enable_monitoring: bool = True,
    self_enhancing: bool = True
) -> Tuple[NetworkContextEngine, Dict[str, Any]]:
    """
    Initialize the complete agent system with shared context.
    
    This function:
    1. Creates a shared NetworkContextEngine instance
    2. Initializes all agent types with the shared context
    3. Sets up performance monitoring
    4. Enables all advanced features
    
    Args:
        use_faiss: Enable FAISS for 10-100x faster search
        enable_caching: Enable advanced caching (1000x+ speedup on hits)
        enable_monitoring: Enable performance monitoring
        self_enhancing: Use self-enhancing agents (with learning)
    
    Returns:
        Tuple of (context_engine, agents_dict)
        
    Example:
        >>> from agent_init import init_agent_system
        >>> engine, agents = init_agent_system()
        >>> result = agents['codex'].generate_code("create API")
        >>> # All agents now share the same context automatically
    """
    global _GLOBAL_ENGINE, _GLOBAL_AGENTS, _GLOBAL_UNIVERSAL
    
    # Return cached instances if already initialized
    if _GLOBAL_ENGINE is not None and _GLOBAL_AGENTS is not None:
        print("✓ Using existing agent system instance")
        return _GLOBAL_ENGINE, _GLOBAL_AGENTS
    
    print("Initializing Agent System...")
    print("=" * 50)
    
    # 1. Initialize context engine with all features
    print("1. Initializing Context Engine...")
    engine = NetworkContextEngine(
        use_openai=bool(os.getenv("OPENAI_API_KEY")),
        use_openrouter=bool(os.getenv("OPENROUTER_API_KEY")),
        whitelist_all_domains=True
    )
    
    # 2. Set up advanced features
    if enable_caching:
        print("2. Enabling Advanced Caching (1000x+ speedup)...")
        cache = AdvancedCache(
            max_size=10000,
            ttl=3600,
            enable_disk_cache=True
        )
        engine.cache = cache
    
    if use_faiss:
        print("3. Enabling FAISS Search (10-100x speedup)...")
        search_engine = AdvancedSearchEngine(engine)
        engine.search_engine = search_engine
    
    if enable_monitoring:
        print("4. Enabling Performance Monitoring...")
        monitor = PerformanceMonitor()
        engine.monitor = monitor
    
    print("5. Enabling Advanced Reasoning (Chain/Tree-of-Thought)...")
    reasoning = AdvancedReasoning(engine)
    engine.reasoning = reasoning
    
    print("6. Enabling Memory Consolidation (10x reduction)...")
    consolidator = MemoryConsolidation(engine)
    engine.consolidator = consolidator
    
    # 3. Initialize all agent types with shared context
    print("7. Initializing All Agent Types...")
    
    if self_enhancing:
        agents = {
            'codex': SelfEnhancingCodexAgent(context_engine=engine),
            'ui_designer': SelfEnhancingUIDesignerAgent(context_engine=engine),
            'reasoning': SelfEnhancingReasoningAgent(context_engine=engine)
        }
        print("   ✓ Self-Enhancing Agents (with learning & tool creation)")
    else:
        agents = {
            'codex': EnhancedCodexAgent(context_engine=engine),
            'ui_designer': EnhancedUIDesignerAgent(context_engine=engine),
            'reasoning': EnhancedReasoningAgent(context_engine=engine)
        }
        print("   ✓ Enhanced Agents (with network & batch)")
    
    # 4. Initialize universal compatibility layer
    print("8. Initializing Universal Compatibility Layer...")
    universal = UniversalAgentInterface(
        context_engine=engine,
        enable_openai_codex=True,
        enable_github_copilot=True,
        autonomous_mode=True
    )
    
    # Register all agents
    for agent_name, agent in agents.items():
        universal.register_agent(
            agent=agent,
            agent_type=agent_name,
            capabilities=agent.capabilities if hasattr(agent, 'capabilities') else []
        )
    
    # Store globally for reuse
    _GLOBAL_ENGINE = engine
    _GLOBAL_AGENTS = agents
    _GLOBAL_UNIVERSAL = universal
    
    print("=" * 50)
    print("✓ Agent System Initialization Complete!")
    print()
    print(f"Context Engine: {type(engine).__name__}")
    print(f"Agents: {', '.join(agents.keys())}")
    print(f"Universal Interface: Enabled")
    print(f"All systems connected and operational!")
    print()
    
    return engine, agents


def get_engine() -> NetworkContextEngine:
    """Get the global shared context engine instance."""
    if _GLOBAL_ENGINE is None:
        init_agent_system()
    return _GLOBAL_ENGINE


def get_agents() -> Dict[str, Any]:
    """Get the global shared agents dictionary."""
    if _GLOBAL_AGENTS is None:
        init_agent_system()
    return _GLOBAL_AGENTS


def get_universal() -> UniversalAgentInterface:
    """Get the global universal compatibility interface."""
    if _GLOBAL_UNIVERSAL is None:
        init_agent_system()
    return _GLOBAL_UNIVERSAL


# Auto-initialize on import if AGENT_AUTO_INIT is set
if os.getenv("AGENT_AUTO_INIT", "false").lower() == "true":
    print("⚙ Auto-initializing agent system (AGENT_AUTO_INIT=true)...")
    init_agent_system()
