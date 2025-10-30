"""
Tests for the Edge class.
"""

import pytest
from context_engine.edge import Edge


def test_edge_creation():
    """Test basic edge creation."""
    edge = Edge(source_id="node1", target_id="node2", edge_type="semantic")
    
    assert edge.source_id == "node1"
    assert edge.target_id == "node2"
    assert edge.edge_type == "semantic"
    assert edge.weight == 1.0
    assert edge.directed is True


def test_edge_with_weight():
    """Test edge creation with custom weight."""
    edge = Edge(source_id="node1", target_id="node2", weight=0.5)
    assert edge.weight == 0.5


def test_edge_invalid_weight():
    """Test that invalid weight raises error."""
    with pytest.raises(ValueError):
        Edge(source_id="node1", target_id="node2", weight=1.5)
    
    with pytest.raises(ValueError):
        Edge(source_id="node1", target_id="node2", weight=-0.1)


def test_edge_self_loop_not_allowed():
    """Test that self-loops raise error."""
    with pytest.raises(ValueError):
        Edge(source_id="node1", target_id="node1")


def test_edge_undirected():
    """Test undirected edge creation."""
    edge = Edge(source_id="node1", target_id="node2", directed=False)
    assert edge.directed is False


def test_edge_reverse():
    """Test edge reversal."""
    edge = Edge(source_id="node1", target_id="node2", edge_type="semantic", weight=0.7)
    reversed_edge = edge.reverse()
    
    assert reversed_edge.source_id == "node2"
    assert reversed_edge.target_id == "node1"
    assert reversed_edge.edge_type == "semantic"
    assert reversed_edge.weight == 0.7


def test_edge_to_dict():
    """Test edge serialization to dict."""
    edge = Edge(
        source_id="node1",
        target_id="node2",
        edge_type="semantic",
        weight=0.8,
        metadata={"key": "value"}
    )
    
    data = edge.to_dict()
    
    assert data['source_id'] == "node1"
    assert data['target_id'] == "node2"
    assert data['edge_type'] == "semantic"
    assert data['weight'] == 0.8
    assert data['metadata'] == {"key": "value"}


def test_edge_from_dict():
    """Test edge deserialization from dict."""
    data = {
        'source_id': 'node1',
        'target_id': 'node2',
        'edge_type': 'temporal',
        'weight': 0.6,
        'directed': False,
        'metadata': {'timestamp': 123456},
        'created_at': 1234567890.0
    }
    
    edge = Edge.from_dict(data)
    
    assert edge.source_id == 'node1'
    assert edge.target_id == 'node2'
    assert edge.edge_type == 'temporal'
    assert edge.weight == 0.6
    assert edge.directed is False
    assert edge.metadata == {'timestamp': 123456}


def test_edge_equality_directed():
    """Test edge equality for directed edges."""
    edge1 = Edge(source_id="a", target_id="b", edge_type="test")
    edge2 = Edge(source_id="a", target_id="b", edge_type="test")
    edge3 = Edge(source_id="b", target_id="a", edge_type="test")
    
    assert edge1 == edge2
    assert edge1 != edge3  # Direction matters


def test_edge_equality_undirected():
    """Test edge equality for undirected edges."""
    edge1 = Edge(source_id="a", target_id="b", edge_type="test", directed=False)
    edge2 = Edge(source_id="b", target_id="a", edge_type="test", directed=False)
    
    assert edge1 == edge2  # Direction doesn't matter


def test_edge_hash_directed():
    """Test edge hashing for directed edges."""
    edge1 = Edge(source_id="a", target_id="b", edge_type="test")
    edge2 = Edge(source_id="a", target_id="b", edge_type="test")
    
    assert hash(edge1) == hash(edge2)
    
    edge_set = {edge1, edge2}
    assert len(edge_set) == 1


def test_edge_hash_undirected():
    """Test edge hashing for undirected edges."""
    edge1 = Edge(source_id="a", target_id="b", edge_type="test", directed=False)
    edge2 = Edge(source_id="b", target_id="a", edge_type="test", directed=False)
    
    assert hash(edge1) == hash(edge2)


def test_edge_repr():
    """Test edge string representation."""
    edge = Edge(source_id="node1", target_id="node2", edge_type="semantic", weight=0.75)
    repr_str = repr(edge)
    
    assert "Edge" in repr_str
    assert "semantic" in repr_str
    assert "0.75" in repr_str
