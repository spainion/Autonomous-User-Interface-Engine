# Phase 2: Production Deployment Guide
**Autonomous UI Engine - Production Readiness**

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# 1. Set up environment variables
cp .env.template .env
# Edit .env with your API keys

# 2. Start all services
docker-compose up -d

# 3. Check service health
curl http://localhost:8000/api/v1/health

# 4. Access services
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# 3. In another terminal, start monitoring (optional)
docker-compose up prometheus grafana -d
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Key Endpoints

#### Health & Monitoring
```bash
# Health check
GET /api/v1/health

# Readiness probe
GET /api/v1/health/ready

# Liveness probe
GET /api/v1/health/live

# Prometheus metrics
GET /metrics
```

#### UI Generation
```bash
# Generate UI from prompt
POST /api/v1/generate
Content-Type: application/json

{
  "prompt": "Create a modern dashboard with charts",
  "theme": "modern",
  "framework": "bootstrap",
  "optimizations": ["performance", "accessibility"]
}

# List available templates
GET /api/v1/templates
```

#### Context Management
```bash
# Add context
POST /api/v1/context/add
{
  "key": "user_preference",
  "content": "Modern dark theme",
  "metadata": {"user_id": "123"}
}

# Query context
POST /api/v1/context/query
{
  "query": "user preferences",
  "limit": 10
}

# Get statistics
GET /api/v1/context/stats
```

#### Agent Orchestration
```bash
# Execute agent task
POST /api/v1/agents/execute
{
  "agent_type": "codex",
  "task": "Generate authentication code",
  "parameters": {"language": "python"}
}

# List agents
GET /api/v1/agents/list

# Get agent status
GET /api/v1/agents/{agent_type}/status
```

## 🐳 Docker Deployment

### Building the Image

```bash
# Build image
docker build -t ui-engine:latest .

# Build with specific version
docker build -t ui-engine:0.4.0 .

# Check image size
docker images ui-engine
```

### Running Containers

```bash
# Run API only
docker run -d -p 8000:8000 \
  -e OPENROUTER_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  --name ui-engine-api \
  ui-engine:latest

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Scale API service
docker-compose up -d --scale api=3
```

### Container Management

```bash
# Stop all services
docker-compose stop

# Restart services
docker-compose restart

# Remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build
```

## 📊 Monitoring & Observability

### Prometheus Metrics

Access Prometheus at http://localhost:9090

**Available Metrics:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency histogram
- `process_cpu_seconds_total` - CPU usage
- `process_resident_memory_bytes` - Memory usage

**Example Queries:**
```promql
# Request rate per second
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

### Grafana Dashboards

Access Grafana at http://localhost:3000 (admin/admin)

**Pre-configured Dashboards:**
- API Performance
- System Resources
- Error Rates
- Cache Performance

### Structured Logging

Logs are structured in JSON format:

```json
{
  "timestamp": "2025-11-18T05:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "method": "POST",
  "path": "/api/v1/generate",
  "duration": 0.234,
  "status": 200
}
```

## 🔧 Configuration Management

### Environment Variables

Required variables in `.env`:

```bash
# API Keys
OPENROUTER_API_KEY=your_openrouter_key
OPENAI_API_KEY=your_openai_key

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Redis (optional)
REDIS_HOST=redis
REDIS_PORT=6379

# Monitoring
PROMETHEUS_ENABLED=true
METRICS_PORT=9090
```

### Configuration Validation

The API validates configuration at startup:

```bash
# Test configuration
python -c "from api.main import app; print('Config valid!')"

# Check environment
docker-compose config
```

## 🔒 Security

### Container Security

- Running as non-root user (uid: 1000)
- Multi-stage builds for minimal attack surface
- Health checks enabled
- Resource limits configured

### API Security

- CORS configured (update for production)
- Rate limiting enabled (60 req/min default)
- Input validation with Pydantic
- Structured error responses (no stack traces in prod)

### Secrets Management

```bash
# Using Docker secrets
echo "your_api_key" | docker secret create openrouter_key -

# Using environment variables
export OPENROUTER_API_KEY="your_key"

# Using .env file (gitignored)
cp .env.template .env
# Edit .env with your keys
```

## 🚀 Production Deployment

### Pre-deployment Checklist

- [ ] Environment variables configured
- [ ] API keys secured
- [ ] CORS origins updated
- [ ] Rate limits adjusted
- [ ] Logging level set to INFO/WARNING
- [ ] Health checks configured
- [ ] Monitoring dashboards set up
- [ ] Backup strategy in place

### Kubernetes Deployment (Optional)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ui-engine-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ui-engine-api
  template:
    metadata:
      labels:
        app: ui-engine-api
    spec:
      containers:
      - name: api
        image: ui-engine:0.4.0
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        livenessProbe:
          httpGet:
            path: /api/v1/health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Cloud Deployment

**AWS ECS:**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t ui-engine .
docker tag ui-engine:latest your-account.dkr.ecr.us-east-1.amazonaws.com/ui-engine:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/ui-engine:latest
```

**Google Cloud Run:**
```bash
# Deploy to Cloud Run
gcloud run deploy ui-engine \
  --image gcr.io/your-project/ui-engine:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🧪 Testing

### API Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Generate UI
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a login form",
    "theme": "modern"
  }'

# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/v1/health

# Load testing with wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/v1/health
```

### Integration Testing

```bash
# Run integration tests
pytest tests/integration/ -v

# Test with docker-compose
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Performance Tuning

### API Server

```bash
# Increase workers
uvicorn api.main:app --workers 4

# Enable HTTP/2
uvicorn api.main:app --http h2

# Adjust timeouts
uvicorn api.main:app --timeout-keep-alive 30
```

### Docker Optimization

```dockerfile
# Use specific Python version
FROM python:3.11.7-slim

# Enable buildkit
DOCKER_BUILDKIT=1 docker build .

# Multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 -t ui-engine .
```

## 🆘 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs api

# Verify environment variables
docker-compose config

# Test locally first
python -m uvicorn api.main:app --reload
```

**High memory usage:**
```bash
# Check container stats
docker stats

# Limit memory
docker-compose up -d --memory 512m

# Profile memory
docker exec ui-engine-api python -m memory_profiler api/main.py
```

**Slow response times:**
```bash
# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=http_request_duration_seconds

# Enable profiling
uvicorn api.main:app --debug

# Check database connections
docker-compose logs redis
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Prometheus Guide](https://prometheus.io/docs/introduction/overview/)
- [Grafana Tutorials](https://grafana.com/tutorials/)

## 🔄 Next Steps

After Phase 2 completion:
- ✅ Containerization complete
- ✅ API server deployed
- ✅ Monitoring configured
- ✅ Production ready

**Ready for Phase 3: Quality & Security**
- Security hardening
- Comprehensive testing (85% coverage)
- Code refactoring
- E2E testing
