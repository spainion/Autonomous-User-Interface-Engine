# Enterprise Features

Phase 5: Multi-tenancy, RBAC, Audit Logging, Analytics

## Quick Start

### Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin"}'

# Use token
export TOKEN="your_jwt_token"
```

### Tenant Management

```bash
# Create tenant
curl -X POST http://localhost:8000/api/v1/tenants \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "tenant_123",
    "name": "My Company",
    "plan": "professional"
  }'

# Get usage
curl http://localhost:8000/api/v1/tenants/tenant_123/usage \
  -H "Authorization: Bearer $TOKEN"
```

### Analytics

```bash
# Usage metrics
curl http://localhost:8000/api/v1/analytics/usage \
  -H "Authorization: Bearer $TOKEN"

# Cost analytics
curl http://localhost:8000/api/v1/analytics/costs \
  -H "Authorization: Bearer $TOKEN"
```

## Features

- **Multi-tenancy**: Complete tenant isolation
- **RBAC**: 5 roles, 10+ permissions
- **Audit Logging**: Comprehensive audit trail
- **Analytics**: Real-time usage and cost tracking
- **JWT Authentication**: Secure token-based auth
- **API Keys**: Programmatic access

## Documentation

See [PHASE5_ENTERPRISE_GUIDE.md](../PHASE5_ENTERPRISE_GUIDE.md) for complete documentation.

## Roles

- **Super Admin**: Full system access
- **Tenant Admin**: Manage tenant resources
- **Developer**: API access, read/write
- **Analyst**: Read-only access
- **Service Account**: Programmatic access

## Permissions

- ui:generate, ui:view, ui:delete
- context:read, context:write, context:delete
- agent:execute, agent:manage
- tenant:read, tenant:manage
- user:read, user:manage
- analytics:view
- admin:all
