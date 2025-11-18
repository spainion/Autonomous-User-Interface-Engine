"""
Benchmark suite for Context Engine.
Phase 4: Performance Optimization
"""

import time
import pytest
from typing import List, Dict, Any


class ContextEngineBenchmarks:
    """Benchmarks for context engine operations."""

    def setup_method(self):
        """Setup for each test."""
        try:
            from context_engine import ContextEngine
            self.engine = ContextEngine()
        except ImportError:
            pytest.skip("ContextEngine not available")

    def benchmark_add_nodes(self, n: int = 1000) -> float:
        """Benchmark adding nodes to context engine."""
        start = time.time()
        for i in range(n):
            self.engine.add_node(f"node_{i}", f"content_{i}")
        duration = time.time() - start
        ops_per_sec = n / duration if duration > 0 else 0
        print(f"Added {n} nodes in {duration:.3f}s ({ops_per_sec:.0f} ops/sec)")
        return duration

    def benchmark_retrieve_nodes(self, n: int = 1000) -> float:
        """Benchmark retrieving nodes from context engine."""
        # Setup
        for i in range(n):
            self.engine.add_node(f"node_{i}", f"content_{i}")
        
        # Benchmark
        start = time.time()
        for i in range(n):
            self.engine.get_node(f"node_{i}")
        duration = time.time() - start
        ops_per_sec = n / duration if duration > 0 else 0
        print(f"Retrieved {n} nodes in {duration:.3f}s ({ops_per_sec:.0f} ops/sec)")
        return duration

    def benchmark_search(self, n: int = 100) -> float:
        """Benchmark search operations."""
        # Setup
        for i in range(1000):
            self.engine.add_node(f"node_{i}", f"content_{i}")
        
        # Benchmark
        start = time.time()
        for i in range(n):
            self.engine.search(f"content_{i}")
        duration = time.time() - start
        ops_per_sec = n / duration if duration > 0 else 0
        print(f"Performed {n} searches in {duration:.3f}s ({ops_per_sec:.0f} ops/sec)")
        return duration


def run_benchmarks():
    """Run all context engine benchmarks."""
    print("\n=== Context Engine Benchmarks ===\n")
    bench = ContextEngineBenchmarks()
    bench.setup_method()
    
    results = {
        "add_nodes": bench.benchmark_add_nodes(1000),
        "retrieve_nodes": bench.benchmark_retrieve_nodes(1000),
        "search": bench.benchmark_search(100),
    }
    
    print(f"\n=== Summary ===")
    print(f"Add nodes: {results['add_nodes']:.3f}s")
    print(f"Retrieve nodes: {results['retrieve_nodes']:.3f}s")
    print(f"Search: {results['search']:.3f}s")
    
    return results


if __name__ == "__main__":
    run_benchmarks()
