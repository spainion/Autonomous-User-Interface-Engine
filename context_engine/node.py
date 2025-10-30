"""
Node class for the context engine.

Represents a single node in the context graph with:
- Unique identifier
- Content/data storage
- Vector embedding for semantic similarity
- 3D spatial coordinates
- Metadata and relationships
"""

from typing import Any, Dict, Optional, List
import numpy as np
from dataclasses import dataclass, field
import hashlib
import json


@dataclass
class Node:
    """
    A node in the context graph with vector embeddings and 3D spatial representation.
    
    Attributes:
        content: The actual content/data stored in the node
        node_id: Unique identifier (auto-generated from content hash if not provided)
        embedding: Vector embedding for semantic similarity (numpy array)
        position_3d: 3D coordinates in space (x, y, z)
        metadata: Additional metadata for the node
        node_type: Type/category of the node
        created_at: Timestamp of node creation
    """
    content: Any
    node_id: Optional[str] = None
    embedding: Optional[np.ndarray] = None
    position_3d: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    node_type: str = "generic"
    created_at: Optional[float] = None
    
    def __post_init__(self):
        """Initialize node with auto-generated ID and default values."""
        if self.node_id is None:
            self.node_id = self._generate_id()
        
        if self.position_3d is None:
            # Initialize with random 3D position in unit cube
            self.position_3d = np.random.rand(3)
        
        if self.created_at is None:
            import time
            self.created_at = time.time()
    
    def _generate_id(self) -> str:
        """Generate a unique ID based on content hash."""
        content_str = json.dumps(self.content, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]
    
    def set_embedding(self, embedding: np.ndarray) -> None:
        """
        Set the vector embedding for this node.
        
        Args:
            embedding: Numpy array representing the semantic embedding
        """
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        self.embedding = embedding / np.linalg.norm(embedding)  # Normalize
    
    def set_position_3d(self, x: float, y: float, z: float) -> None:
        """
        Set the 3D spatial position of the node.
        
        Args:
            x, y, z: 3D coordinates
        """
        self.position_3d = np.array([x, y, z])
    
    def distance_to(self, other: 'Node', metric: str = 'euclidean') -> float:
        """
        Calculate distance to another node in 3D space.
        
        Args:
            other: Another Node instance
            metric: Distance metric ('euclidean', 'manhattan', 'chebyshev')
        
        Returns:
            Distance value
        """
        if metric == 'euclidean':
            return float(np.linalg.norm(self.position_3d - other.position_3d))
        elif metric == 'manhattan':
            return float(np.sum(np.abs(self.position_3d - other.position_3d)))
        elif metric == 'chebyshev':
            return float(np.max(np.abs(self.position_3d - other.position_3d)))
        else:
            raise ValueError(f"Unknown metric: {metric}")
    
    def semantic_similarity(self, other: 'Node') -> float:
        """
        Calculate cosine similarity between embeddings.
        
        Args:
            other: Another Node instance
        
        Returns:
            Cosine similarity score (0 to 1)
        """
        if self.embedding is None or other.embedding is None:
            raise ValueError("Both nodes must have embeddings")
        
        # Cosine similarity (already normalized)
        return float(np.dot(self.embedding, other.embedding))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            'node_id': self.node_id,
            'content': self.content,
            'embedding': self.embedding.tolist() if self.embedding is not None else None,
            'position_3d': self.position_3d.tolist() if self.position_3d is not None else None,
            'metadata': self.metadata,
            'node_type': self.node_type,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """Create node from dictionary representation."""
        embedding = np.array(data['embedding']) if data.get('embedding') else None
        position_3d = np.array(data['position_3d']) if data.get('position_3d') else None
        
        return cls(
            content=data['content'],
            node_id=data['node_id'],
            embedding=embedding,
            position_3d=position_3d,
            metadata=data.get('metadata', {}),
            node_type=data.get('node_type', 'generic'),
            created_at=data.get('created_at')
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on node_id."""
        if not isinstance(other, Node):
            return False
        return self.node_id == other.node_id
    
    def __hash__(self) -> int:
        """Hash based on node_id."""
        return hash(self.node_id)
    
    def __repr__(self) -> str:
        """String representation of the node."""
        return f"Node(id={self.node_id[:8]}..., type={self.node_type}, content={str(self.content)[:50]}...)"
