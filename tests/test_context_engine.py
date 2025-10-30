"""
Tests for the ContextEngine class.
"""

import pytest
import numpy as np
from context_engine.context_engine import ContextEngine
from context_engine.node import Node
from context_engine.edge import Edge


@pytest.fixture
def engine():
    """Create a fresh context engine for testing."""
    return ContextEngine()


def test_context_engine_creation(engine):
    """Test basic context engine creation."""
    assert len(engine) == 0
    assert engine.graph.number_of_edges() == 0


def test_add_node(engine):
    """Test adding a node."""
    node = engine.add_node(content="Hello World", node_type="text")
    
    assert node.content == "Hello World"
    assert node.node_type == "text"
    assert len(engine) == 1


def test_add_node_with_embedding(engine):
    """Test adding node with embedding."""
    embedding = np.array([1.0, 2.0, 3.0])
    node = engine.add_node(content="Test", embedding=embedding)
    
    assert node.embedding is not None
    assert len(engine) == 1


def test_add_duplicate_content(engine):
    """Test that duplicate content is deduplicated."""
    node1 = engine.add_node(content="Same content")
    node2 = engine.add_node(content="Same content")
    
    # Should return the same node
    assert node1.node_id == node2.node_id
    assert len(engine) == 1


def test_get_node(engine):
    """Test retrieving a node."""
    node = engine.add_node(content="Test")
    retrieved = engine.get_node(node.node_id)
    
    assert retrieved == node


def test_get_nonexistent_node(engine):
    """Test getting non-existent node returns None."""
    retrieved = engine.get_node("nonexistent-id")
    assert retrieved is None


def test_remove_node(engine):
    """Test removing a node."""
    node = engine.add_node(content="Test")
    node_id = node.node_id
    
    success = engine.remove_node(node_id)
    
    assert success is True
    assert len(engine) == 0
    assert engine.get_node(node_id) is None


def test_remove_nonexistent_node(engine):
    """Test removing non-existent node."""
    success = engine.remove_node("nonexistent-id")
    assert success is False


def test_add_edge(engine):
    """Test adding an edge."""
    node1 = engine.add_node(content="Node 1")
    node2 = engine.add_node(content="Node 2")
    
    edge = engine.add_edge(node1.node_id, node2.node_id, edge_type="semantic")
    
    assert edge.source_id == node1.node_id
    assert edge.target_id == node2.node_id
    assert engine.graph.number_of_edges() >= 1


def test_add_edge_invalid_nodes(engine):
    """Test that adding edge with invalid nodes raises error."""
    with pytest.raises(ValueError):
        engine.add_edge("invalid-id-1", "invalid-id-2")


def test_add_undirected_edge(engine):
    """Test adding undirected edge."""
    node1 = engine.add_node(content="Node 1")
    node2 = engine.add_node(content="Node 2")
    
    edge = engine.add_edge(
        node1.node_id, node2.node_id, 
        directed=False, edge_type="bidirectional"
    )
    
    # Should create edges in both directions
    assert engine.graph.has_edge(node1.node_id, node2.node_id)
    assert engine.graph.has_edge(node2.node_id, node1.node_id)


def test_find_similar_nodes(engine):
    """Test finding similar nodes."""
    # Add nodes with embeddings
    emb1 = np.array([1.0, 0.0, 0.0])
    emb2 = np.array([0.9, 0.1, 0.0])
    emb3 = np.array([0.0, 1.0, 0.0])
    
    engine.add_node(content="Node 1", embedding=emb1)
    engine.add_node(content="Node 2", embedding=emb2)
    engine.add_node(content="Node 3", embedding=emb3)
    
    # Search for similar nodes
    query = np.array([1.0, 0.0, 0.0])
    similar = engine.find_similar_nodes(query, k=2)
    
    assert len(similar) <= 2
    # First result should be most similar
    if len(similar) > 1:
        assert similar[0][1] >= similar[1][1]


def test_get_neighbors(engine):
    """Test getting neighboring nodes."""
    node1 = engine.add_node(content="Node 1")
    node2 = engine.add_node(content="Node 2")
    node3 = engine.add_node(content="Node 3")
    
    engine.add_edge(node1.node_id, node2.node_id)
    engine.add_edge(node1.node_id, node3.node_id)
    
    neighbors = engine.get_neighbors(node1.node_id)
    
    assert len(neighbors) == 2
    assert node2 in neighbors
    assert node3 in neighbors


def test_get_neighbors_with_edge_type_filter(engine):
    """Test getting neighbors filtered by edge type."""
    node1 = engine.add_node(content="Node 1")
    node2 = engine.add_node(content="Node 2")
    node3 = engine.add_node(content="Node 3")
    
    engine.add_edge(node1.node_id, node2.node_id, edge_type="semantic")
    engine.add_edge(node1.node_id, node3.node_id, edge_type="temporal")
    
    semantic_neighbors = engine.get_neighbors(node1.node_id, edge_type="semantic")
    
    assert len(semantic_neighbors) == 1
    assert node2 in semantic_neighbors


def test_cluster_nodes(engine):
    """Test clustering nodes."""
    # Add nodes with embeddings
    for i in range(10):
        emb = np.random.rand(3)
        engine.add_node(content=f"Node {i}", embedding=emb)
    
    clusters = engine.cluster_nodes(method='kmeans', n_clusters=3)
    
    assert len(clusters) > 0
    # All nodes should be in a cluster
    total_nodes = sum(len(nodes) for nodes in clusters.values())
    assert total_nodes == 10


def test_find_paths(engine):
    """Test finding paths between nodes."""
    node1 = engine.add_node(content="Node 1")
    node2 = engine.add_node(content="Node 2")
    node3 = engine.add_node(content="Node 3")
    
    engine.add_edge(node1.node_id, node2.node_id)
    engine.add_edge(node2.node_id, node3.node_id)
    
    paths = engine.find_paths(node1.node_id, node3.node_id)
    
    assert len(paths) > 0
    # Should find path through node2
    assert len(paths[0]) == 3


def test_get_context_window(engine):
    """Test getting context window."""
    # Create nodes with specific positions
    node1 = engine.add_node(content="Center")
    node1.set_position_3d(0.0, 0.0, 0.0)
    
    node2 = engine.add_node(content="Near")
    node2.set_position_3d(0.1, 0.1, 0.1)
    
    node3 = engine.add_node(content="Far")
    node3.set_position_3d(5.0, 5.0, 5.0)
    
    # Update nodes in engine
    engine.nodes[node1.node_id] = node1
    engine.nodes[node2.node_id] = node2
    engine.nodes[node3.node_id] = node3
    
    nearby = engine.get_context_window(node1.node_id, radius=1.0)
    
    assert node2 in nearby
    assert node3 not in nearby


def test_get_statistics(engine):
    """Test getting engine statistics."""
    node1 = engine.add_node(content="Node 1", node_type="text")
    node2 = engine.add_node(content="Node 2", node_type="text")
    node3 = engine.add_node(content="Node 3", node_type="data")
    
    engine.add_edge(node1.node_id, node2.node_id, edge_type="semantic")
    
    stats = engine.get_statistics()
    
    assert stats['n_nodes'] == 3
    assert stats['n_edges'] >= 1
    assert 'text' in stats['node_types']
    assert 'data' in stats['node_types']
    assert 'semantic' in stats['edge_types']


def test_export_import(engine):
    """Test exporting and importing context engine."""
    # Create some nodes and edges
    node1 = engine.add_node(content="Node 1", node_type="text")
    node2 = engine.add_node(content="Node 2", node_type="text")
    engine.add_edge(node1.node_id, node2.node_id, edge_type="test")
    
    # Export
    data = engine.export_to_dict()
    
    # Import into new engine
    new_engine = ContextEngine.import_from_dict(data)
    
    assert len(new_engine) == len(engine)
    assert new_engine.graph.number_of_edges() == engine.graph.number_of_edges()


def test_context_engine_repr(engine):
    """Test string representation."""
    engine.add_node(content="Test")
    repr_str = repr(engine)
    
    assert "ContextEngine" in repr_str
    assert "nodes=1" in repr_str
