"""
ContextEngine - The main context management system.

Integrates:
- Node and Edge management
- Graph operations (NetworkX)
- Vector space operations
- Deduplication and storage
- Query and recall system
"""

from typing import Any, Dict, List, Optional, Tuple, Set
import numpy as np
import networkx as nx
from collections import defaultdict
import json
import hashlib

from .node import Node
from .edge import Edge
from .vector_space import VectorSpace


class ContextEngine:
    """
    Main context engine for managing nodes, edges, and relationships.
    
    Features:
    - Non-redundant storage with content-based deduplication
    - Graph-based relationship management
    - Vector similarity search
    - Clustering and spatial operations
    - Complex queries and context recall
    """
    
    def __init__(self):
        """Initialize the context engine."""
        self.nodes: Dict[str, Node] = {}
        self.graph = nx.DiGraph()  # Directed graph for relationships
        self.content_hashes: Dict[str, str] = {}  # Hash -> node_id mapping for dedup
        self.vector_space: Optional[VectorSpace] = None
        self._node_id_to_vector_idx: Dict[str, int] = {}
    
    def add_node(
        self, 
        content: Any,
        node_type: str = "generic",
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[np.ndarray] = None
    ) -> Node:
        """
        Add a node to the context engine with deduplication.
        
        Args:
            content: Content to store in the node
            node_type: Type/category of the node
            metadata: Additional metadata
            embedding: Pre-computed embedding vector
        
        Returns:
            The created or existing node
        """
        # Generate content hash for deduplication
        content_str = json.dumps(content, sort_keys=True, default=str)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        # Check if content already exists (deduplication)
        if content_hash in self.content_hashes:
            existing_node_id = self.content_hashes[content_hash]
            return self.nodes[existing_node_id]
        
        # Create new node
        node = Node(
            content=content,
            node_type=node_type,
            metadata=metadata or {},
            embedding=embedding
        )
        
        # Store node
        self.nodes[node.node_id] = node
        self.content_hashes[content_hash] = node.node_id
        self.graph.add_node(node.node_id, node=node)
        
        # Update vector space if embedding provided
        if embedding is not None:
            self._update_vector_space()
        
        return node
    
    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str = "generic",
        weight: float = 1.0,
        directed: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Edge:
        """
        Add an edge between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            edge_type: Type of relationship
            weight: Strength of relationship
            directed: Whether edge is directional
            metadata: Additional edge metadata
        
        Returns:
            The created edge
        """
        # Validate nodes exist
        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} does not exist")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} does not exist")
        
        # Create edge
        edge = Edge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            weight=weight,
            directed=directed,
            metadata=metadata or {}
        )
        
        # Add to graph
        self.graph.add_edge(
            source_id, 
            target_id, 
            edge=edge,
            weight=weight,
            edge_type=edge_type
        )
        
        # If undirected, add reverse edge
        if not directed:
            self.graph.add_edge(
                target_id,
                source_id,
                edge=edge,
                weight=weight,
                edge_type=edge_type
            )
        
        return edge
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node and all its edges.
        
        Args:
            node_id: ID of node to remove
        
        Returns:
            True if removed, False if not found
        """
        if node_id not in self.nodes:
            return False
        
        # Remove from content hashes
        node = self.nodes[node_id]
        content_str = json.dumps(node.content, sort_keys=True, default=str)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        if content_hash in self.content_hashes:
            del self.content_hashes[content_hash]
        
        # Remove from graph
        if self.graph.has_node(node_id):
            self.graph.remove_node(node_id)
        
        # Remove from nodes
        del self.nodes[node_id]
        
        # Update vector space
        self._update_vector_space()
        
        return True
    
    def find_similar_nodes(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        threshold: float = 0.0
    ) -> List[Tuple[Node, float]]:
        """
        Find nodes similar to a query embedding.
        
        Args:
            query_embedding: Query vector
            k: Number of similar nodes to return
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            List of (node, similarity_score) tuples
        """
        if self.vector_space is None or len(self.vector_space) == 0:
            return []
        
        # Find nearest neighbors
        indices, distances = self.vector_space.find_nearest_neighbors(
            query_embedding, k=k, metric='cosine'
        )
        
        # Convert distances to similarities and filter
        results = []
        for idx, dist in zip(indices, distances):
            similarity = 1.0 - dist
            if similarity >= threshold:
                node_id = self._vector_idx_to_node_id(idx)
                if node_id:
                    results.append((self.nodes[node_id], float(similarity)))
        
        return results
    
    def get_neighbors(
        self,
        node_id: str,
        edge_type: Optional[str] = None,
        max_depth: int = 1
    ) -> List[Node]:
        """
        Get neighboring nodes.
        
        Args:
            node_id: Source node ID
            edge_type: Filter by edge type (optional)
            max_depth: Maximum traversal depth
        
        Returns:
            List of neighbor nodes
        """
        if node_id not in self.graph:
            return []
        
        if max_depth == 1:
            neighbors = list(self.graph.successors(node_id))
            if edge_type:
                neighbors = [
                    n for n in neighbors 
                    if self.graph[node_id][n].get('edge_type') == edge_type
                ]
        else:
            # Multi-hop neighbors
            neighbors = []
            visited = {node_id}
            current_level = {node_id}
            
            for _ in range(max_depth):
                next_level = set()
                for curr_node in current_level:
                    for neighbor in self.graph.successors(curr_node):
                        if neighbor not in visited:
                            if edge_type is None or self.graph[curr_node][neighbor].get('edge_type') == edge_type:
                                next_level.add(neighbor)
                                visited.add(neighbor)
                
                neighbors.extend(next_level)
                current_level = next_level
                
                if not current_level:
                    break
        
        return [self.nodes[nid] for nid in neighbors if nid in self.nodes]
    
    def cluster_nodes(
        self,
        method: str = 'kmeans',
        n_clusters: int = 5,
        **kwargs
    ) -> Dict[int, List[Node]]:
        """
        Cluster nodes based on embeddings.
        
        Args:
            method: Clustering method ('kmeans', 'dbscan', 'hierarchical')
            n_clusters: Number of clusters (for kmeans/hierarchical)
            **kwargs: Additional parameters for clustering
        
        Returns:
            Dictionary mapping cluster_id to list of nodes
        """
        if self.vector_space is None or len(self.vector_space) == 0:
            return {}
        
        # Perform clustering
        if method == 'kmeans':
            labels = self.vector_space.cluster_kmeans(n_clusters, **kwargs)
        elif method == 'dbscan':
            labels = self.vector_space.cluster_dbscan(**kwargs)
        elif method == 'hierarchical':
            labels = self.vector_space.cluster_hierarchical(n_clusters, **kwargs)
        else:
            raise ValueError(f"Unknown clustering method: {method}")
        
        # Group nodes by cluster
        clusters = defaultdict(list)
        for idx, label in enumerate(labels):
            node_id = self._vector_idx_to_node_id(idx)
            if node_id:
                clusters[int(label)].append(self.nodes[node_id])
        
        return dict(clusters)
    
    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_length: Optional[int] = None
    ) -> List[List[Node]]:
        """
        Find all paths between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            max_length: Maximum path length
        
        Returns:
            List of paths (each path is a list of nodes)
        """
        if source_id not in self.graph or target_id not in self.graph:
            return []
        
        try:
            if max_length:
                paths = nx.all_simple_paths(
                    self.graph, source_id, target_id, cutoff=max_length
                )
            else:
                paths = nx.all_simple_paths(self.graph, source_id, target_id)
            
            return [
                [self.nodes[nid] for nid in path]
                for path in paths
            ]
        except nx.NetworkXNoPath:
            return []
    
    def get_context_window(
        self,
        center_node_id: str,
        radius: float = 1.0,
        max_nodes: int = 50
    ) -> List[Node]:
        """
        Get nodes within a spatial radius in 3D space.
        
        Args:
            center_node_id: Center node ID
            radius: Spatial radius
            max_nodes: Maximum nodes to return
        
        Returns:
            List of nearby nodes
        """
        center_node = self.nodes.get(center_node_id)
        if not center_node:
            return []
        
        nearby = []
        for node in self.nodes.values():
            if node.node_id == center_node_id:
                continue
            
            distance = center_node.distance_to(node)
            if distance <= radius:
                nearby.append((node, distance))
        
        # Sort by distance and limit
        nearby.sort(key=lambda x: x[1])
        return [node for node, _ in nearby[:max_nodes]]
    
    def _update_vector_space(self) -> None:
        """Update the vector space with current node embeddings."""
        embeddings = []
        self._node_id_to_vector_idx.clear()
        
        for idx, (node_id, node) in enumerate(self.nodes.items()):
            if node.embedding is not None:
                embeddings.append(node.embedding)
                self._node_id_to_vector_idx[node_id] = idx
        
        if embeddings:
            self.vector_space = VectorSpace(np.array(embeddings))
        else:
            self.vector_space = None
    
    def _vector_idx_to_node_id(self, idx: int) -> Optional[str]:
        """Convert vector index to node ID."""
        for node_id, vector_idx in self._node_id_to_vector_idx.items():
            if vector_idx == idx:
                return node_id
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the context engine.
        
        Returns:
            Dictionary with various statistics
        """
        stats = {
            'n_nodes': len(self.nodes),
            'n_edges': self.graph.number_of_edges(),
            'node_types': {},
            'edge_types': {},
            'graph_density': nx.density(self.graph) if len(self.nodes) > 1 else 0.0,
        }
        
        # Node type distribution
        for node in self.nodes.values():
            stats['node_types'][node.node_type] = stats['node_types'].get(node.node_type, 0) + 1
        
        # Edge type distribution
        for _, _, data in self.graph.edges(data=True):
            edge_type = data.get('edge_type', 'unknown')
            stats['edge_types'][edge_type] = stats['edge_types'].get(edge_type, 0) + 1
        
        # Vector space stats
        if self.vector_space:
            stats['vector_space'] = self.vector_space.calculate_statistics()
        
        return stats
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export the entire context engine to a dictionary."""
        return {
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'edges': [
                self.graph[u][v]['edge'].to_dict()
                for u, v in self.graph.edges()
            ]
        }
    
    @classmethod
    def import_from_dict(cls, data: Dict[str, Any]) -> 'ContextEngine':
        """Import context engine from a dictionary."""
        engine = cls()
        
        # Import nodes
        for node_dict in data['nodes'].values():
            node = Node.from_dict(node_dict)
            engine.nodes[node.node_id] = node
            engine.graph.add_node(node.node_id, node=node)
        
        # Import edges
        for edge_dict in data['edges']:
            edge = Edge.from_dict(edge_dict)
            engine.graph.add_edge(
                edge.source_id,
                edge.target_id,
                edge=edge,
                weight=edge.weight,
                edge_type=edge.edge_type
            )
        
        # Rebuild vector space
        engine._update_vector_space()
        
        return engine
    
    def __len__(self) -> int:
        """Return number of nodes."""
        return len(self.nodes)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"ContextEngine(nodes={len(self.nodes)}, edges={self.graph.number_of_edges()})"
