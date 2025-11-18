# Autonomous UI Engine API

FastAPI-based REST API for the Autonomous User Interface Engine.

## Quick Start

```bash
# Development mode
make api-dev

# Production mode
make api-prod

# With Docker
make docker-up
```

## Endpoints

- **GET** `/` - Root endpoint
- **GET** `/api/v1/health` - Health check
- **GET** `/api/docs` - Interactive API documentation
- **GET** `/metrics` - Prometheus metrics

### UI Generation
- **POST** `/api/v1/generate` - Generate UI from prompt
- **GET** `/api/v1/templates` - List available templates

### Context Management
- **POST** `/api/v1/context/add` - Add context
- **POST** `/api/v1/context/query` - Query context
- **GET** `/api/v1/context/stats` - Get statistics

### Agent Orchestration
- **POST** `/api/v1/agents/execute` - Execute agent task
- **GET** `/api/v1/agents/list` - List agents
- **GET** `/api/v1/agents/{type}/status` - Get agent status

## Documentation

See [PHASE2_DEPLOYMENT_GUIDE.md](../PHASE2_DEPLOYMENT_GUIDE.md) for complete documentation.
