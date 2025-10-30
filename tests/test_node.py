"""
Tests for the Node class.
"""

import pytest
import numpy as np
from context_engine.node import Node


def test_node_creation():
    """Test basic node creation."""
    node = Node(content="Hello World", node_type="text")
    
    assert node.content == "Hello World"
    assert node.node_type == "text"
    assert node.node_id is not None
    assert node.position_3d is not None
    assert len(node.position_3d) == 3


def test_node_with_custom_id():
    """Test node creation with custom ID."""
    node = Node(content="Test", node_id="custom-id-123")
    assert node.node_id == "custom-id-123"


def test_node_auto_id_generation():
    """Test that nodes with same content get same ID."""
    node1 = Node(content={"key": "value"})
    node2 = Node(content={"key": "value"})
    
    assert node1.node_id == node2.node_id


def test_node_different_content_different_id():
    """Test that nodes with different content get different IDs."""
    node1 = Node(content="content1")
    node2 = Node(content="content2")
    
    assert node1.node_id != node2.node_id


def test_node_set_embedding():
    """Test setting embedding for a node."""
    node = Node(content="Test")
    embedding = np.array([1.0, 2.0, 3.0])
    
    node.set_embedding(embedding)
    
    assert node.embedding is not None
    assert len(node.embedding) == 3
    # Check normalization
    assert np.isclose(np.linalg.norm(node.embedding), 1.0)


def test_node_set_position():
    """Test setting 3D position."""
    node = Node(content="Test")
    node.set_position_3d(1.0, 2.0, 3.0)
    
    assert np.array_equal(node.position_3d, np.array([1.0, 2.0, 3.0]))


def test_node_distance_euclidean():
    """Test Euclidean distance calculation."""
    node1 = Node(content="A")
    node1.set_position_3d(0.0, 0.0, 0.0)
    
    node2 = Node(content="B")
    node2.set_position_3d(3.0, 4.0, 0.0)
    
    distance = node1.distance_to(node2, metric='euclidean')
    assert np.isclose(distance, 5.0)  # 3-4-5 triangle


def test_node_distance_manhattan():
    """Test Manhattan distance calculation."""
    node1 = Node(content="A")
    node1.set_position_3d(0.0, 0.0, 0.0)
    
    node2 = Node(content="B")
    node2.set_position_3d(1.0, 2.0, 3.0)
    
    distance = node1.distance_to(node2, metric='manhattan')
    assert np.isclose(distance, 6.0)  # 1 + 2 + 3


def test_node_semantic_similarity():
    """Test semantic similarity calculation."""
    node1 = Node(content="A")
    node1.set_embedding(np.array([1.0, 0.0, 0.0]))
    
    node2 = Node(content="B")
    node2.set_embedding(np.array([1.0, 0.0, 0.0]))
    
    similarity = node1.semantic_similarity(node2)
    assert np.isclose(similarity, 1.0)  # Identical embeddings


def test_node_semantic_similarity_orthogonal():
    """Test similarity with orthogonal embeddings."""
    node1 = Node(content="A")
    node1.set_embedding(np.array([1.0, 0.0, 0.0]))
    
    node2 = Node(content="B")
    node2.set_embedding(np.array([0.0, 1.0, 0.0]))
    
    similarity = node1.semantic_similarity(node2)
    assert np.isclose(similarity, 0.0)  # Orthogonal


def test_node_to_dict():
    """Test node serialization to dict."""
    node = Node(content="Test", node_type="text", metadata={"key": "value"})
    node.set_embedding(np.array([1.0, 2.0, 3.0]))
    
    data = node.to_dict()
    
    assert data['content'] == "Test"
    assert data['node_type'] == "text"
    assert data['metadata'] == {"key": "value"}
    assert data['embedding'] is not None


def test_node_from_dict():
    """Test node deserialization from dict."""
    data = {
        'node_id': 'test-123',
        'content': 'Test content',
        'embedding': [0.5, 0.5, 0.5],
        'position_3d': [1.0, 2.0, 3.0],
        'metadata': {'key': 'value'},
        'node_type': 'text',
        'created_at': 1234567890.0
    }
    
    node = Node.from_dict(data)
    
    assert node.node_id == 'test-123'
    assert node.content == 'Test content'
    assert node.node_type == 'text'
    assert node.metadata == {'key': 'value'}
    assert np.array_equal(node.position_3d, np.array([1.0, 2.0, 3.0]))


def test_node_equality():
    """Test node equality based on ID."""
    node1 = Node(content="Test", node_id="id-1")
    node2 = Node(content="Test", node_id="id-1")
    node3 = Node(content="Test", node_id="id-2")
    
    assert node1 == node2
    assert node1 != node3


def test_node_hash():
    """Test node hashing for use in sets/dicts."""
    node1 = Node(content="Test", node_id="id-1")
    node2 = Node(content="Test", node_id="id-1")
    
    # Same hash for same ID
    assert hash(node1) == hash(node2)
    
    # Can use in set
    node_set = {node1, node2}
    assert len(node_set) == 1


def test_node_repr():
    """Test node string representation."""
    node = Node(content="Test content", node_type="text")
    repr_str = repr(node)
    
    assert "Node" in repr_str
    assert "text" in repr_str
