"""
Edge class for the context engine.

Represents relationships between nodes with:
- Source and target nodes
- Relationship type
- Weight/strength
- Directional or bidirectional
- Metadata
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import time


@dataclass
class Edge:
    """
    An edge representing a relationship between two nodes.
    
    Attributes:
        source_id: ID of the source node
        target_id: ID of the target node
        edge_type: Type of relationship (e.g., 'semantic', 'temporal', 'causal')
        weight: Strength of the relationship (0.0 to 1.0)
        directed: Whether the edge is directional
        metadata: Additional edge properties
        created_at: Timestamp of edge creation
    """
    source_id: str
    target_id: str
    edge_type: str = "generic"
    weight: float = 1.0
    directed: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[float] = None
    
    def __post_init__(self):
        """Initialize edge with validation and defaults."""
        if self.created_at is None:
            self.created_at = time.time()
        
        # Validate weight
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {self.weight}")
        
        # Ensure source and target are different (no self-loops by default)
        if self.source_id == self.target_id:
            raise ValueError("Self-loops not allowed (source_id == target_id)")
    
    def reverse(self) -> 'Edge':
        """
        Create a reversed copy of this edge (swap source and target).
        
        Returns:
            New Edge with reversed direction
        """
        return Edge(
            source_id=self.target_id,
            target_id=self.source_id,
            edge_type=self.edge_type,
            weight=self.weight,
            directed=self.directed,
            metadata=self.metadata.copy(),
            created_at=self.created_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary representation."""
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'edge_type': self.edge_type,
            'weight': self.weight,
            'directed': self.directed,
            'metadata': self.metadata,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Edge':
        """Create edge from dictionary representation."""
        return cls(
            source_id=data['source_id'],
            target_id=data['target_id'],
            edge_type=data.get('edge_type', 'generic'),
            weight=data.get('weight', 1.0),
            directed=data.get('directed', True),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at')
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on source, target, and type."""
        if not isinstance(other, Edge):
            return False
        if self.directed:
            return (self.source_id == other.source_id and 
                    self.target_id == other.target_id and
                    self.edge_type == other.edge_type)
        else:
            # For undirected, order doesn't matter
            return (self.edge_type == other.edge_type and
                    ((self.source_id == other.source_id and self.target_id == other.target_id) or
                     (self.source_id == other.target_id and self.target_id == other.source_id)))
    
    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""
        if self.directed:
            return hash((self.source_id, self.target_id, self.edge_type))
        else:
            # For undirected edges, order shouldn't matter
            ids = tuple(sorted([self.source_id, self.target_id]))
            return hash((*ids, self.edge_type))
    
    def __repr__(self) -> str:
        """String representation of the edge."""
        arrow = "->" if self.directed else "<->"
        return f"Edge({self.source_id[:8]}...{arrow}{self.target_id[:8]}..., type={self.edge_type}, weight={self.weight:.2f})"
