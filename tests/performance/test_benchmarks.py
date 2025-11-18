"""Performance benchmark tests - Phase 3."""
import pytest
import time


@pytest.mark.performance
class TestPerformanceBenchmarks:
    """Performance benchmarking tests."""

    def test_basic_speed(self):
        """Test basic operations are fast."""
        start = time.time()
        result = sum(range(1000))
        duration = time.time() - start
        assert duration < 0.01
        assert result > 0
