"""
Autonomous User Interface Engine - Context Engine

A powerful context management system with:
- Graph-based nodes and edges
- Vector embeddings for semantic understanding
- 3D spatial relationships
- Clustering and similarity calculations
- Non-redundant storage with deduplication
- Network-enhanced capabilities with API integration
- Advanced caching with LRU and persistence
- Performance monitoring and profiling
- FAISS-powered ultra-fast vector search
- Advanced reasoning (Chain-of-Thought, Tree-of-Thought)
- Memory consolidation and importance scoring
"""

from .context_engine import ContextEngine
from .node import Node
from .edge import Edge
from .vector_space import VectorSpace
from .network_engine import NetworkContextEngine
from .advanced_cache import AdvancedCache
from .performance_monitor import PerformanceMonitor
from .advanced_search import AdvancedVectorSearch, HybridSearch
from .advanced_reasoning import AdvancedReasoning, ReasoningStrategy
from .memory_consolidation import MemoryConsolidation

__version__ = "0.3.0"
__all__ = [
    "ContextEngine",
    "Node",
    "Edge",
    "VectorSpace",
    "NetworkContextEngine",
    "AdvancedCache",
    "PerformanceMonitor",
    "AdvancedVectorSearch",
    "HybridSearch",
    "AdvancedReasoning",
    "ReasoningStrategy",
    "MemoryConsolidation",
]
