"""
Example usage of the Context Engine.

Demonstrates:
- Creating nodes with content and embeddings
- Connecting nodes with edges
- Finding similar content
- Clustering nodes
- Spatial queries
"""

import numpy as np
from context_engine import ContextEngine, Node
from context_engine.embedding_generator import EmbeddingGenerator


def main():
    print("=" * 60)
    print("Context Engine Example")
    print("=" * 60)
    
    # Initialize the context engine
    engine = ContextEngine()
    print("\n✓ Context engine initialized")
    
    # Create some sample nodes with random embeddings
    print("\n1. Adding nodes with embeddings...")
    
    nodes_data = [
        {"content": "Machine learning is a subset of AI", "type": "knowledge"},
        {"content": "Deep learning uses neural networks", "type": "knowledge"},
        {"content": "Python is great for data science", "type": "knowledge"},
        {"content": "User clicked on button A", "type": "event"},
        {"content": "User clicked on button B", "type": "event"},
    ]
    
    nodes = []
    for data in nodes_data:
        # Create random embedding (in production, use EmbeddingGenerator)
        embedding = EmbeddingGenerator.create_random_embedding(dimension=128)
        node = engine.add_node(
            content=data["content"],
            node_type=data["type"],
            embedding=embedding
        )
        nodes.append(node)
        print(f"  + Added: {data['content'][:40]}...")
    
    print(f"\n✓ Total nodes: {len(engine)}")
    
    # Add relationships between nodes
    print("\n2. Creating relationships...")
    
    # Connect related knowledge nodes
    engine.add_edge(
        nodes[0].node_id, nodes[1].node_id,
        edge_type="semantic_related",
        weight=0.9
    )
    
    # Connect event nodes in sequence
    engine.add_edge(
        nodes[3].node_id, nodes[4].node_id,
        edge_type="temporal_sequence",
        weight=1.0
    )
    
    print(f"✓ Created {engine.graph.number_of_edges()} edges")
    
    # Find similar nodes
    print("\n3. Finding similar nodes...")
    query_embedding = EmbeddingGenerator.create_random_embedding(dimension=128)
    similar_nodes = engine.find_similar_nodes(query_embedding, k=3)
    
    print(f"  Found {len(similar_nodes)} similar nodes:")
    for node, similarity in similar_nodes:
        print(f"    - {node.content[:40]}... (similarity: {similarity:.3f})")
    
    # Get neighbors
    print("\n4. Getting node neighbors...")
    neighbors = engine.get_neighbors(nodes[0].node_id)
    print(f"  Node '{nodes[0].content[:30]}...' has {len(neighbors)} neighbors")
    for neighbor in neighbors:
        print(f"    - {neighbor.content[:40]}...")
    
    # Cluster nodes
    print("\n5. Clustering nodes...")
    clusters = engine.cluster_nodes(method='kmeans', n_clusters=2)
    
    for cluster_id, cluster_nodes in clusters.items():
        print(f"  Cluster {cluster_id}: {len(cluster_nodes)} nodes")
        for node in cluster_nodes[:2]:  # Show first 2
            print(f"    - {node.content[:40]}...")
    
    # Get spatial context window
    print("\n6. Spatial context window...")
    nearby = engine.get_context_window(nodes[0].node_id, radius=2.0, max_nodes=3)
    print(f"  Found {len(nearby)} nodes near '{nodes[0].content[:30]}...'")
    
    # Statistics
    print("\n7. Engine statistics...")
    stats = engine.get_statistics()
    print(f"  Total nodes: {stats['n_nodes']}")
    print(f"  Total edges: {stats['n_edges']}")
    print(f"  Node types: {stats['node_types']}")
    print(f"  Edge types: {stats['edge_types']}")
    print(f"  Graph density: {stats['graph_density']:.3f}")
    
    # Demonstrate deduplication
    print("\n8. Testing deduplication...")
    duplicate_node = engine.add_node(
        content="Machine learning is a subset of AI",
        node_type="knowledge"
    )
    print(f"  Added duplicate content...")
    print(f"  Same node returned: {duplicate_node.node_id == nodes[0].node_id}")
    print(f"  Total nodes (unchanged): {len(engine)}")
    
    # Export and import
    print("\n9. Export/Import test...")
    export_data = engine.export_to_dict()
    new_engine = ContextEngine.import_from_dict(export_data)
    print(f"  Exported {len(export_data['nodes'])} nodes")
    print(f"  Imported engine has {len(new_engine)} nodes")
    
    print("\n" + "=" * 60)
    print("✓ Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
