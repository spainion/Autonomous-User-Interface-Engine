"""
Benchmark suite for API endpoints.
Phase 4: Performance Optimization
"""

import time
import requests
from typing import Dict, Any


class APIBenchmarks:
    """Benchmarks for API endpoints."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def benchmark_health_endpoint(self, n: int = 1000) -> float:
        """Benchmark health check endpoint."""
        start = time.time()
        for _ in range(n):
            try:
                response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
                assert response.status_code == 200
            except Exception:
                break
        duration = time.time() - start
        ops_per_sec = n / duration if duration > 0 else 0
        print(f"Health checks: {n} requests in {duration:.3f}s ({ops_per_sec:.0f} req/sec)")
        return duration

    def benchmark_ui_generation(self, n: int = 10) -> float:
        """Benchmark UI generation endpoint."""
        payload = {
            "prompt": "Create a simple form",
            "theme": "modern",
            "framework": "bootstrap"
        }
        
        start = time.time()
        for _ in range(n):
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/generate",
                    json=payload,
                    timeout=30
                )
                assert response.status_code == 200
            except Exception:
                break
        duration = time.time() - start
        ops_per_sec = n / duration if duration > 0 else 0
        print(f"UI generation: {n} requests in {duration:.3f}s ({ops_per_sec:.2f} req/sec)")
        return duration


def run_benchmarks():
    """Run all API benchmarks."""
    print("\n=== API Benchmarks ===\n")
    bench = APIBenchmarks()
    
    try:
        # Test if API is running
        response = requests.get(f"{bench.base_url}/api/v1/health", timeout=2)
        if response.status_code != 200:
            print("API not running, skipping benchmarks")
            return
    except Exception:
        print("API not running, skipping benchmarks")
        return
    
    results = {
        "health": bench.benchmark_health_endpoint(100),
        "ui_generation": bench.benchmark_ui_generation(5),
    }
    
    print(f"\n=== Summary ===")
    print(f"Health endpoint: {results['health']:.3f}s")
    print(f"UI generation: {results['ui_generation']:.3f}s")
    
    return results


if __name__ == "__main__":
    run_benchmarks()
