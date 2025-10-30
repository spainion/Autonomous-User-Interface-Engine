"""
Autonomous User Interface Engine - Context Engine

A powerful context management system with:
- Graph-based nodes and edges
- Vector embeddings for semantic understanding
- 3D spatial relationships
- Clustering and similarity calculations
- Non-redundant storage with deduplication
- Network-enhanced capabilities with API integration
"""

from .context_engine import ContextEngine
from .node import Node
from .edge import Edge
from .vector_space import VectorSpace
from .network_engine import NetworkContextEngine

__version__ = "0.2.0"
__all__ = ["ContextEngine", "Node", "Edge", "VectorSpace", "NetworkContextEngine"]
