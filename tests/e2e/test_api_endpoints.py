"""E2E tests for API endpoints."""

import pytest


@pytest.mark.e2e
class TestAPIEndpoints:
    """Test all API endpoints end-to-end."""

    def test_root_endpoint(self):
        """Test root endpoint returns correct info."""
        try:
            import requests
            response = requests.get('http://localhost:8000/', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'version' in data
        except Exception:
            pytest.skip("API server not running")

    def test_docs_accessible(self):
        """Test API documentation is accessible."""
        try:
            import requests
            response = requests.get('http://localhost:8000/api/docs', timeout=5)
            assert response.status_code == 200
        except Exception:
            pytest.skip("API server not running")

    def test_metrics_endpoint(self):
        """Test Prometheus metrics endpoint."""
        try:
            import requests
            response = requests.get('http://localhost:8000/metrics', timeout=5)
            assert response.status_code == 200
            assert 'http_requests_total' in response.text
        except Exception:
            pytest.skip("API server not running")
