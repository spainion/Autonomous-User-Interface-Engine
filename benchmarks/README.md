# Performance Benchmarks

Phase 4: Performance Optimization

## Running Benchmarks

```bash
# Run all benchmarks
make benchmark

# Run specific benchmark
python -m benchmarks.bench_context_engine
python -m benchmarks.bench_api

# With pytest
pytest benchmarks/ -v
```

## Benchmark Files

- `bench_context_engine.py` - Context engine operations
- `bench_api.py` - API endpoint performance

## Metrics Tracked

- Operations per second
- Response times
- Memory usage
- Throughput

## Expected Results

Context Engine:
- Add nodes: >1000 ops/sec
- Retrieve nodes: >2000 ops/sec
- Search: >50 ops/sec

API:
- Health check: >400 req/sec
- UI generation: >0.5 req/sec

## Continuous Benchmarking

Benchmarks are run in CI/CD to detect performance regressions.
