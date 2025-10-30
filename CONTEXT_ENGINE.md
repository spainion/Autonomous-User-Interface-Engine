# Context Engine Documentation

## Overview

The Context Engine is a powerful system for managing contextual information using advanced graph theory, vector mathematics, and 3D spatial relationships. It provides a sophisticated foundation for AI agents to maintain, query, and reason about complex contextual data.

## Core Features

### 1. **Graph-Based Knowledge Representation**
- Nodes represent discrete pieces of information
- Edges represent relationships between nodes
- Support for directed and undirected relationships
- Multiple edge types (semantic, temporal, causal, etc.)

### 2. **Vector Embeddings**
- Semantic similarity using cosine distance
- Integration with OpenAI embeddings or sentence transformers
- Efficient nearest-neighbor search
- High-dimensional vector operations

### 3. **3D Spatial Relationships**
- Each node has a 3D position in space
- Spatial queries (radius-based context windows)
- Distance metrics (Euclidean, Manhattan, Chebyshev)
- Visual representation of relationships

### 4. **Advanced Clustering**
- K-means clustering
- DBSCAN (density-based clustering)
- Hierarchical/agglomerative clustering
- Cluster statistics and analysis

### 5. **Non-Redundant Storage**
- Content-based deduplication
- Hash-based node identification
- Efficient memory usage

### 6. **Complex Queries**
- Path finding between nodes
- Multi-hop neighbor traversal
- Filter by node/edge types
- Similarity search with thresholds

## Architecture

```
ContextEngine
├── Node (content + embeddings + 3D position)
├── Edge (relationships with weights)
├── VectorSpace (clustering, similarity, dimensionality reduction)
└── EmbeddingGenerator (text → vectors)
```

## Installation

```bash
pip install -r requirements.txt
```

### Dependencies
- `numpy` - Numerical operations
- `scipy` - Scientific computing
- `scikit-learn` - Machine learning algorithms
- `networkx` - Graph operations
- `sentence-transformers` - Text embeddings (optional)
- `openai` - OpenAI API integration (optional)

## Quick Start

```python
from context_engine import ContextEngine
from context_engine.embedding_generator import EmbeddingGenerator

# Initialize
engine = ContextEngine()

# Add nodes
node1 = engine.add_node(
    content="Machine learning is fascinating",
    node_type="knowledge",
    embedding=some_embedding_vector
)

node2 = engine.add_node(
    content="Deep learning uses neural networks",
    node_type="knowledge"
)

# Create relationships
engine.add_edge(
    node1.node_id, 
    node2.node_id,
    edge_type="semantic_related",
    weight=0.8
)

# Find similar content
similar = engine.find_similar_nodes(query_embedding, k=5)

# Cluster related information
clusters = engine.cluster_nodes(method='kmeans', n_clusters=3)

# Get spatial context
nearby = engine.get_context_window(node1.node_id, radius=2.0)
```

## API Reference

### ContextEngine

#### `add_node(content, node_type='generic', metadata=None, embedding=None)`
Add a node to the context engine with automatic deduplication.

**Parameters:**
- `content`: The content/data to store
- `node_type`: Type/category of the node
- `metadata`: Additional metadata dictionary
- `embedding`: Optional pre-computed embedding vector

**Returns:** Node object

#### `add_edge(source_id, target_id, edge_type='generic', weight=1.0, directed=True, metadata=None)`
Create a relationship between two nodes.

**Parameters:**
- `source_id`: Source node ID
- `target_id`: Target node ID
- `edge_type`: Type of relationship
- `weight`: Strength (0.0 to 1.0)
- `directed`: Whether edge is directional
- `metadata`: Additional edge properties

**Returns:** Edge object

#### `find_similar_nodes(query_embedding, k=5, threshold=0.0)`
Find nodes most similar to a query embedding.

**Parameters:**
- `query_embedding`: Query vector (numpy array)
- `k`: Number of results to return
- `threshold`: Minimum similarity score

**Returns:** List of (node, similarity_score) tuples

#### `get_neighbors(node_id, edge_type=None, max_depth=1)`
Get neighboring nodes in the graph.

**Parameters:**
- `node_id`: Source node ID
- `edge_type`: Optional filter by edge type
- `max_depth`: Maximum traversal depth

**Returns:** List of Node objects

#### `cluster_nodes(method='kmeans', n_clusters=5, **kwargs)`
Cluster nodes based on their embeddings.

**Parameters:**
- `method`: 'kmeans', 'dbscan', or 'hierarchical'
- `n_clusters`: Number of clusters (kmeans/hierarchical)
- `**kwargs`: Additional clustering parameters

**Returns:** Dictionary mapping cluster_id → list of nodes

#### `find_paths(source_id, target_id, max_length=None)`
Find all paths between two nodes.

**Parameters:**
- `source_id`: Starting node ID
- `target_id`: Destination node ID
- `max_length`: Maximum path length

**Returns:** List of paths (each path is a list of nodes)

#### `get_context_window(center_node_id, radius=1.0, max_nodes=50)`
Get nodes within a spatial radius in 3D space.

**Parameters:**
- `center_node_id`: Center node ID
- `radius`: Spatial radius
- `max_nodes`: Maximum nodes to return

**Returns:** List of nearby nodes

#### `get_statistics()`
Get comprehensive statistics about the context engine.

**Returns:** Dictionary with node counts, edge counts, types, densities, etc.

### Node

#### Properties
- `content`: The stored content
- `node_id`: Unique identifier
- `embedding`: Vector embedding (numpy array)
- `position_3d`: 3D coordinates (x, y, z)
- `metadata`: Additional properties
- `node_type`: Type/category
- `created_at`: Timestamp

#### Methods
- `set_embedding(embedding)`: Set the embedding vector
- `set_position_3d(x, y, z)`: Set 3D position
- `distance_to(other, metric='euclidean')`: Calculate distance to another node
- `semantic_similarity(other)`: Calculate cosine similarity
- `to_dict()`: Serialize to dictionary
- `from_dict(data)`: Deserialize from dictionary

### Edge

#### Properties
- `source_id`: Source node ID
- `target_id`: Target node ID
- `edge_type`: Relationship type
- `weight`: Strength (0.0 to 1.0)
- `directed`: Directional flag
- `metadata`: Additional properties
- `created_at`: Timestamp

#### Methods
- `reverse()`: Create reversed edge
- `to_dict()`: Serialize to dictionary
- `from_dict(data)`: Deserialize from dictionary

### VectorSpace

#### Methods
- `add_vectors(vectors)`: Add vectors to the space
- `cosine_similarity_matrix()`: Calculate pairwise similarities
- `euclidean_distance_matrix()`: Calculate pairwise distances
- `find_nearest_neighbors(query, k=5, metric='cosine')`: Find k nearest vectors
- `cluster_kmeans(n_clusters=5)`: K-means clustering
- `cluster_dbscan(eps=0.5, min_samples=2)`: Density-based clustering
- `cluster_hierarchical(n_clusters=5)`: Hierarchical clustering
- `reduce_dimensionality_pca(n_components=3)`: PCA reduction
- `reduce_dimensionality_tsne(n_components=3)`: t-SNE reduction
- `calculate_statistics()`: Get vector space statistics
- `get_cluster_info()`: Get clustering information

### EmbeddingGenerator

#### Initialization
```python
# OpenAI backend
gen = EmbeddingGenerator(
    backend='openai',
    model='text-embedding-3-small',
    api_key='your-api-key'
)

# Local sentence transformer
gen = EmbeddingGenerator(
    backend='sentence-transformer',
    model='all-MiniLM-L6-v2'
)
```

#### Methods
- `generate_embedding(text)`: Generate embedding for single text
- `generate_embeddings(texts)`: Generate embeddings for multiple texts
- `get_dimension()`: Get embedding dimension
- `create_random_embedding(dimension=384)`: Create random embedding (testing)

## Use Cases

### 1. **Conversational AI Context**
Maintain conversation history with semantic relationships:
```python
# Add user messages
user_msg = engine.add_node(
    content="What's the weather?",
    node_type="user_message",
    embedding=generate_embedding("What's the weather?")
)

# Add assistant response
bot_msg = engine.add_node(
    content="It's sunny and 72°F",
    node_type="assistant_message"
)

# Link in conversation
engine.add_edge(user_msg.node_id, bot_msg.node_id, edge_type="response")
```

### 2. **Knowledge Base**
Store and query domain knowledge:
```python
# Add facts
fact1 = engine.add_node(content="Python was created by Guido van Rossum")
fact2 = engine.add_node(content="Python first released in 1991")

# Relate facts
engine.add_edge(fact1.node_id, fact2.node_id, edge_type="related_to")

# Find similar knowledge
similar_facts = engine.find_similar_nodes(query_embedding, k=5)
```

### 3. **Event Tracking**
Track temporal sequences:
```python
# Add events
event1 = engine.add_node(content="User logged in", node_type="event")
event2 = engine.add_node(content="User viewed product", node_type="event")
event3 = engine.add_node(content="User added to cart", node_type="event")

# Create timeline
engine.add_edge(event1.node_id, event2.node_id, edge_type="temporal")
engine.add_edge(event2.node_id, event3.node_id, edge_type="temporal")

# Find event sequences
path = engine.find_paths(event1.node_id, event3.node_id)
```

### 4. **UI Component Relationships**
Model UI hierarchies and interactions:
```python
# Add UI components
header = engine.add_node(content="Header", node_type="component")
nav = engine.add_node(content="Navigation", node_type="component")
button = engine.add_node(content="Login Button", node_type="component")

# Model hierarchy
engine.add_edge(header.node_id, nav.node_id, edge_type="contains")
engine.add_edge(nav.node_id, button.node_id, edge_type="contains")

# Find component context
context = engine.get_neighbors(button.node_id, max_depth=2)
```

## Advanced Features

### Custom Distance Metrics
```python
# Use different distance calculations
euclidean_dist = node1.distance_to(node2, metric='euclidean')
manhattan_dist = node1.distance_to(node2, metric='manhattan')
chebyshev_dist = node1.distance_to(node2, metric='chebyshev')
```

### Multi-Hop Traversal
```python
# Get neighbors up to 3 hops away
deep_neighbors = engine.get_neighbors(node_id, max_depth=3)
```

### Filtered Queries
```python
# Get only semantic relationships
semantic_neighbors = engine.get_neighbors(
    node_id, 
    edge_type="semantic_related"
)
```

### Clustering with Custom Parameters
```python
# DBSCAN with custom parameters
clusters = engine.cluster_nodes(
    method='dbscan',
    eps=0.3,
    min_samples=5
)

# Hierarchical with specific linkage
clusters = engine.cluster_nodes(
    method='hierarchical',
    n_clusters=4,
    linkage='average'
)
```

## Performance Considerations

1. **Embedding Dimension**: Higher dimensions = more precise but slower
2. **Graph Size**: Use indexing for very large graphs (>10K nodes)
3. **Clustering**: K-means is fastest, DBSCAN for arbitrary shapes
4. **Deduplication**: Content hashing is O(1) lookup
5. **Vector Search**: Approximate nearest neighbors for huge spaces

## Integration with Agent Systems

```python
class ContextAwareAgent:
    def __init__(self):
        self.context = ContextEngine()
        self.embedding_gen = EmbeddingGenerator()
    
    def process_message(self, message):
        # Generate embedding
        embedding = self.embedding_gen.generate_embedding(message)
        
        # Find relevant context
        relevant = self.context.find_similar_nodes(embedding, k=5)
        
        # Add new message to context
        node = self.context.add_node(
            content=message,
            node_type="message",
            embedding=embedding
        )
        
        # Link to relevant context
        for rel_node, similarity in relevant:
            if similarity > 0.7:
                self.context.add_edge(
                    node.node_id,
                    rel_node.node_id,
                    edge_type="relevant_to",
                    weight=similarity
                )
        
        return relevant
```

## Troubleshooting

**Issue**: Out of memory with large graphs
- Solution: Use batch processing, limit cluster sizes, or use approximate methods

**Issue**: Slow similarity search
- Solution: Pre-cluster nodes, use dimensionality reduction, or implement indexing

**Issue**: Poor clustering results
- Solution: Try different methods, adjust parameters, normalize embeddings

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional clustering algorithms
- Graph visualization
- Persistent storage backends
- Distributed computing support
- Custom embedding models

## License

See LICENSE file for details.
