"""
Load testing with Locust for the Autonomous UI Engine API.
Phase 3: Quality & Security

Run with: locust -f locustfile.py --host=http://localhost:8000
"""

from locust import HttpUser, task, between
import json


class UIEngineUser(HttpUser):
    """Simulated user for load testing."""
    
    # Wait between 1-3 seconds between tasks
    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        """Test health endpoint (most frequent)."""
        self.client.get("/api/v1/health")

    @task(2)
    def list_templates(self):
        """Test templates listing."""
        self.client.get("/api/v1/templates")

    @task(1)
    def generate_ui(self):
        """Test UI generation (most expensive)."""
        self.client.post(
            "/api/v1/generate",
            json={
                "prompt": "Create a simple login form",
                "theme": "modern",
                "framework": "bootstrap"
            },
            headers={"Content-Type": "application/json"}
        )

    @task(2)
    def context_stats(self):
        """Test context statistics."""
        self.client.get("/api/v1/context/stats")

    @task(1)
    def list_agents(self):
        """Test agents listing."""
        self.client.get("/api/v1/agents/list")

    def on_start(self):
        """Called when a user starts."""
        # Could do login/authentication here
        pass
