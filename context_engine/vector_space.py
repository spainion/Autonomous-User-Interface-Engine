"""
VectorSpace class for advanced vector operations.

Provides:
- Clustering algorithms (K-means, DBSCAN, Hierarchical)
- Similarity calculations
- Nearest neighbor search
- Dimensionality reduction
- Vector statistics
"""

from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from scipy.spatial.distance import cdist
import warnings


class VectorSpace:
    """
    Advanced vector space operations for context engine.
    
    Handles embedding clustering, similarity search, and dimensionality reduction.
    """
    
    def __init__(self, vectors: Optional[np.ndarray] = None):
        """
        Initialize vector space.
        
        Args:
            vectors: Optional initial vectors (n_samples, n_features)
        """
        self.vectors = vectors if vectors is not None else np.array([])
        self.cluster_labels = None
        self.cluster_centers = None
    
    def add_vectors(self, vectors: np.ndarray) -> None:
        """
        Add vectors to the space.
        
        Args:
            vectors: New vectors to add
        """
        if self.vectors.size == 0:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
    
    def cosine_similarity_matrix(self) -> np.ndarray:
        """
        Calculate pairwise cosine similarity matrix.
        
        Returns:
            Similarity matrix (n_vectors, n_vectors)
        """
        return cosine_similarity(self.vectors)
    
    def euclidean_distance_matrix(self) -> np.ndarray:
        """
        Calculate pairwise Euclidean distance matrix.
        
        Returns:
            Distance matrix (n_vectors, n_vectors)
        """
        return euclidean_distances(self.vectors)
    
    def find_nearest_neighbors(
        self, 
        query_vector: np.ndarray, 
        k: int = 5,
        metric: str = 'cosine'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find k nearest neighbors to a query vector.
        
        Args:
            query_vector: Query vector
            k: Number of neighbors to find
            metric: Distance metric ('cosine', 'euclidean', 'manhattan')
        
        Returns:
            Tuple of (indices, distances) of nearest neighbors
        """
        if len(self.vectors) == 0:
            return np.array([]), np.array([])
        
        query_vector = query_vector.reshape(1, -1)
        
        if metric == 'cosine':
            # For cosine, we want highest similarity (lowest distance)
            similarities = cosine_similarity(query_vector, self.vectors)[0]
            # Convert to distances
            distances = 1 - similarities
            indices = np.argsort(distances)[:k]
            return indices, distances[indices]
        else:
            distances = cdist(query_vector, self.vectors, metric=metric)[0]
            indices = np.argsort(distances)[:k]
            return indices, distances[indices]
    
    def cluster_kmeans(
        self, 
        n_clusters: int = 5,
        random_state: int = 42
    ) -> np.ndarray:
        """
        Perform K-means clustering.
        
        Args:
            n_clusters: Number of clusters
            random_state: Random seed for reproducibility
        
        Returns:
            Cluster labels for each vector
        """
        if len(self.vectors) < n_clusters:
            warnings.warn(f"Number of vectors ({len(self.vectors)}) < n_clusters ({n_clusters})")
            n_clusters = max(1, len(self.vectors))
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.cluster_labels = kmeans.fit_predict(self.vectors)
        self.cluster_centers = kmeans.cluster_centers_
        return self.cluster_labels
    
    def cluster_dbscan(
        self, 
        eps: float = 0.5,
        min_samples: int = 2
    ) -> np.ndarray:
        """
        Perform DBSCAN clustering (density-based).
        
        Args:
            eps: Maximum distance between samples in a cluster
            min_samples: Minimum samples in a neighborhood for core point
        
        Returns:
            Cluster labels (-1 for noise points)
        """
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        self.cluster_labels = dbscan.fit_predict(self.vectors)
        return self.cluster_labels
    
    def cluster_hierarchical(
        self, 
        n_clusters: int = 5,
        linkage: str = 'ward'
    ) -> np.ndarray:
        """
        Perform hierarchical/agglomerative clustering.
        
        Args:
            n_clusters: Number of clusters
            linkage: Linkage criterion ('ward', 'complete', 'average', 'single')
        
        Returns:
            Cluster labels
        """
        if len(self.vectors) < n_clusters:
            warnings.warn(f"Number of vectors ({len(self.vectors)}) < n_clusters ({n_clusters})")
            n_clusters = max(1, len(self.vectors))
        
        clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        self.cluster_labels = clustering.fit_predict(self.vectors)
        return self.cluster_labels
    
    def reduce_dimensionality_pca(
        self, 
        n_components: int = 3
    ) -> np.ndarray:
        """
        Reduce dimensionality using PCA.
        
        Args:
            n_components: Target number of dimensions
        
        Returns:
            Reduced vectors
        """
        if self.vectors.shape[1] <= n_components:
            return self.vectors
        
        pca = PCA(n_components=n_components)
        return pca.fit_transform(self.vectors)
    
    def reduce_dimensionality_tsne(
        self, 
        n_components: int = 3,
        perplexity: float = 30.0,
        random_state: int = 42
    ) -> np.ndarray:
        """
        Reduce dimensionality using t-SNE.
        
        Args:
            n_components: Target number of dimensions (typically 2 or 3)
            perplexity: t-SNE perplexity parameter
            random_state: Random seed
        
        Returns:
            Reduced vectors
        """
        if len(self.vectors) < perplexity:
            perplexity = max(5, len(self.vectors) // 2)
        
        tsne = TSNE(
            n_components=n_components, 
            perplexity=perplexity,
            random_state=random_state
        )
        return tsne.fit_transform(self.vectors)
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistical properties of the vector space.
        
        Returns:
            Dictionary with statistics
        """
        if len(self.vectors) == 0:
            return {}
        
        return {
            'n_vectors': len(self.vectors),
            'dimensionality': self.vectors.shape[1],
            'mean_vector': np.mean(self.vectors, axis=0),
            'std_vector': np.std(self.vectors, axis=0),
            'min_values': np.min(self.vectors, axis=0),
            'max_values': np.max(self.vectors, axis=0),
            'mean_norm': float(np.mean(np.linalg.norm(self.vectors, axis=1))),
            'std_norm': float(np.std(np.linalg.norm(self.vectors, axis=1)))
        }
    
    def get_cluster_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about current clusters.
        
        Returns:
            Dictionary with cluster statistics or None if not clustered
        """
        if self.cluster_labels is None:
            return None
        
        unique_labels = np.unique(self.cluster_labels)
        cluster_sizes = {int(label): int(np.sum(self.cluster_labels == label)) 
                        for label in unique_labels}
        
        return {
            'n_clusters': len(unique_labels),
            'cluster_sizes': cluster_sizes,
            'labels': self.cluster_labels.tolist(),
            'has_noise': -1 in unique_labels  # For DBSCAN
        }
    
    def __len__(self) -> int:
        """Return number of vectors in the space."""
        return len(self.vectors)
    
    def __repr__(self) -> str:
        """String representation."""
        if len(self.vectors) == 0:
            return "VectorSpace(empty)"
        return f"VectorSpace(n_vectors={len(self.vectors)}, dim={self.vectors.shape[1]})"
