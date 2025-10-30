"""
Tests for the VectorSpace class.
"""

import pytest
import numpy as np
from context_engine.vector_space import VectorSpace


@pytest.fixture
def sample_vectors():
    """Create sample vectors for testing."""
    return np.array([
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.9, 0.1],
        [0.0, 0.0, 1.0]
    ])


def test_vector_space_creation():
    """Test basic vector space creation."""
    vectors = np.array([[1, 2, 3], [4, 5, 6]])
    vs = VectorSpace(vectors)
    
    assert len(vs) == 2
    assert vs.vectors.shape == (2, 3)


def test_vector_space_empty():
    """Test empty vector space."""
    vs = VectorSpace()
    assert len(vs) == 0


def test_add_vectors():
    """Test adding vectors to space."""
    vs = VectorSpace()
    vs.add_vectors(np.array([[1, 2, 3]]))
    
    assert len(vs) == 1
    
    vs.add_vectors(np.array([[4, 5, 6], [7, 8, 9]]))
    assert len(vs) == 3


def test_cosine_similarity_matrix(sample_vectors):
    """Test cosine similarity calculation."""
    vs = VectorSpace(sample_vectors)
    sim_matrix = vs.cosine_similarity_matrix()
    
    assert sim_matrix.shape == (5, 5)
    # Diagonal should be close to 1 (self-similarity)
    assert np.allclose(np.diag(sim_matrix), 1.0, atol=0.1)


def test_euclidean_distance_matrix(sample_vectors):
    """Test Euclidean distance calculation."""
    vs = VectorSpace(sample_vectors)
    dist_matrix = vs.euclidean_distance_matrix()
    
    assert dist_matrix.shape == (5, 5)
    # Diagonal should be 0 (distance to self)
    assert np.allclose(np.diag(dist_matrix), 0.0)


def test_find_nearest_neighbors(sample_vectors):
    """Test finding nearest neighbors."""
    vs = VectorSpace(sample_vectors)
    query = np.array([1.0, 0.0, 0.0])
    
    indices, distances = vs.find_nearest_neighbors(query, k=3)
    
    assert len(indices) == 3
    assert len(distances) == 3
    assert indices[0] == 0  # First vector should be closest


def test_find_nearest_neighbors_empty():
    """Test nearest neighbors on empty space."""
    vs = VectorSpace()
    query = np.array([1.0, 0.0, 0.0])
    
    indices, distances = vs.find_nearest_neighbors(query, k=3)
    
    assert len(indices) == 0
    assert len(distances) == 0


def test_cluster_kmeans(sample_vectors):
    """Test K-means clustering."""
    vs = VectorSpace(sample_vectors)
    labels = vs.cluster_kmeans(n_clusters=2)
    
    assert len(labels) == 5
    assert len(np.unique(labels)) <= 2


def test_cluster_dbscan(sample_vectors):
    """Test DBSCAN clustering."""
    vs = VectorSpace(sample_vectors)
    labels = vs.cluster_dbscan(eps=0.5, min_samples=1)
    
    assert len(labels) == 5


def test_cluster_hierarchical(sample_vectors):
    """Test hierarchical clustering."""
    vs = VectorSpace(sample_vectors)
    labels = vs.cluster_hierarchical(n_clusters=3)
    
    assert len(labels) == 5
    assert len(np.unique(labels)) == 3


def test_reduce_dimensionality_pca(sample_vectors):
    """Test PCA dimensionality reduction."""
    vs = VectorSpace(sample_vectors)
    reduced = vs.reduce_dimensionality_pca(n_components=2)
    
    assert reduced.shape == (5, 2)


def test_reduce_dimensionality_tsne():
    """Test t-SNE dimensionality reduction."""
    # Need more samples for t-SNE
    vectors = np.random.rand(50, 10)
    vs = VectorSpace(vectors)
    reduced = vs.reduce_dimensionality_tsne(n_components=2, perplexity=10)
    
    assert reduced.shape == (50, 2)


def test_calculate_statistics(sample_vectors):
    """Test statistics calculation."""
    vs = VectorSpace(sample_vectors)
    stats = vs.calculate_statistics()
    
    assert 'n_vectors' in stats
    assert 'dimensionality' in stats
    assert stats['n_vectors'] == 5
    assert stats['dimensionality'] == 3


def test_calculate_statistics_empty():
    """Test statistics on empty space."""
    vs = VectorSpace()
    stats = vs.calculate_statistics()
    
    assert stats == {}


def test_get_cluster_info(sample_vectors):
    """Test getting cluster information."""
    vs = VectorSpace(sample_vectors)
    vs.cluster_kmeans(n_clusters=2)
    
    cluster_info = vs.get_cluster_info()
    
    assert cluster_info is not None
    assert 'n_clusters' in cluster_info
    assert 'cluster_sizes' in cluster_info


def test_get_cluster_info_no_clustering(sample_vectors):
    """Test cluster info when not clustered."""
    vs = VectorSpace(sample_vectors)
    cluster_info = vs.get_cluster_info()
    
    assert cluster_info is None


def test_vector_space_repr():
    """Test string representation."""
    vectors = np.array([[1, 2, 3], [4, 5, 6]])
    vs = VectorSpace(vectors)
    repr_str = repr(vs)
    
    assert "VectorSpace" in repr_str
    assert "n_vectors=2" in repr_str
