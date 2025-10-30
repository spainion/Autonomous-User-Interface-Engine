"""
Copilot Context Loader - Automatically exports context for GitHub Copilot.

This script runs automatically to provide context to GitHub Copilot
during its workflow, ensuring Copilot uses the context engine system.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from context_engine import NetworkContextEngine
from context_engine.advanced_search import AdvancedSearchEngine
from context_engine.memory_consolidation import MemoryConsolidation


def export_context_for_copilot():
    """
    Export context engine state for GitHub Copilot to use.
    
    This creates .github/copilot-context.json that Copilot can read
    to understand project context, patterns, and learned information.
    """
    try:
        # Initialize context engine
        engine = NetworkContextEngine(
            use_openai=bool(os.getenv("OPENAI_API_KEY")),
            whitelist_all_domains=True
        )
        
        # Get important patterns and memories
        all_nodes = list(engine.graph.nodes.values())
        
        # Get top 50 most important nodes
        consolidator = MemoryConsolidation(engine)
        important_nodes = sorted(
            all_nodes,
            key=lambda n: consolidator._calculate_importance(n.id, n),
            reverse=True
        )[:50]
        
        # Build context export
        context_data = {
            "project": "Autonomous User Interface Engine",
            "context_engine": {
                "available": True,
                "total_nodes": len(all_nodes),
                "important_patterns": [
                    {
                        "id": node.id,
                        "content": node.content[:200] if node.content else None,
                        "metadata": node.metadata,
                        "connections": len(engine.graph.get_neighbors(node.id))
                    }
                    for node in important_nodes[:10]  # Top 10 for Copilot
                ]
            },
            "capabilities": {
                "vector_search": True,
                "semantic_similarity": True,
                "clustering": True,
                "3d_spatial": True,
                "deduplication": True,
                "network_enhanced": True,
                "batch_processing": True,
                "self_learning": True,
                "faiss_search": True,
                "advanced_caching": True,
                "memory_consolidation": True
            },
            "usage_instructions": {
                "import_context": "from context_engine import NetworkContextEngine",
                "create_engine": "engine = NetworkContextEngine(whitelist_all_domains=True)",
                "search_pattern": "results = engine.query_similar(query_vector, k=5)",
                "add_pattern": "node = engine.add_node_with_text('content', 'embedding text')",
                "batch_process": "from agents import EnhancedCodexAgent; agent.batch_generate_code(tasks, parallel=True)"
            },
            "integration_status": {
                "github_copilot": "enabled",
                "openai_codex": "enabled" if os.getenv("OPENAI_API_KEY") else "disabled",
                "autonomous_mode": "enabled",
                "all_systems_operational": True
            }
        }
        
        # Write to .github/copilot-context.json
        output_path = Path(__file__).parent / "copilot-context.json"
        with open(output_path, 'w') as f:
            json.dump(context_data, f, indent=2)
        
        print(f"✓ Copilot context exported to {output_path}")
        print(f"  Total nodes: {len(all_nodes)}")
        print(f"  Important patterns: {len(important_nodes)}")
        print(f"  Context available for GitHub Copilot")
        
        return context_data
        
    except Exception as e:
        print(f"⚠ Warning: Could not export context: {e}")
        # Create minimal context
        minimal_context = {
            "project": "Autonomous User Interface Engine",
            "context_engine": {"available": False},
            "message": "Context engine not initialized - install dependencies with: pip install -r requirements.txt"
        }
        
        output_path = Path(__file__).parent / "copilot-context.json"
        with open(output_path, 'w') as f:
            json.dump(minimal_context, f, indent=2)
        
        return minimal_context


if __name__ == "__main__":
    export_context_for_copilot()
