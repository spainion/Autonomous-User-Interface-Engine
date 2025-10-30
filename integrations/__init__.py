"""
System Compatibility Integrations for Context Engine

This module provides compatibility layers for external systems including:
- Web frameworks (Flask, FastAPI, Django, Express.js)
- Databases (PostgreSQL, MongoDB, Redis, SQLite, Elasticsearch)
- Message queues (RabbitMQ, Kafka, Redis Pub/Sub, AWS SQS)
- Cloud platforms (AWS, GCP, Azure)
- Monitoring systems (Prometheus, Grafana, OpenTelemetry, Datadog)
- CI/CD systems (GitHub Actions, GitLab CI, Jenkins, CircleCI)
- ML/AI frameworks (TensorFlow, PyTorch, HuggingFace, LangChain)
- API protocols (REST, GraphQL, gRPC, WebSocket)
- Authentication systems (OAuth 2.0, JWT, API Keys, SAML)
- Development tools (VSCode, Jupyter, Docker, Kubernetes)
"""

from typing import Dict, Any

__version__ = "1.0.0"
__all__ = [
    "WebFrameworkAdapter",
    "DatabaseAdapter",
    "MessageQueueAdapter",
    "CloudPlatformAdapter",
    "MonitoringAdapter",
    "CICDAdapter",
    "MLFrameworkAdapter",
    "APIAdapter",
    "AuthAdapter",
    "DevToolAdapter",
]


class IntegrationRegistry:
    """Central registry for all system integrations"""
    
    def __init__(self):
        self.integrations: Dict[str, Any] = {}
    
    def register(self, name: str, integration: Any):
        """Register a new integration"""
        self.integrations[name] = integration
    
    def get(self, name: str) -> Any:
        """Get a registered integration"""
        return self.integrations.get(name)
    
    def list_integrations(self) -> list:
        """List all registered integrations"""
        return list(self.integrations.keys())


# Global integration registry
registry = IntegrationRegistry()
