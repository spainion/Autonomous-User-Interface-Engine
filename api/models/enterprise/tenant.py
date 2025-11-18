"""
Multi-tenancy models for enterprise features.
Phase 5: Enterprise Features
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class TenantStatus(str, Enum):
    """Tenant status enumeration."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    INACTIVE = "inactive"


class TenantPlan(str, Enum):
    """Subscription plan types."""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class TenantQuotas(BaseModel):
    """Resource quotas for a tenant."""
    max_api_calls_per_day: int = Field(default=1000, description="Daily API call limit")
    max_ui_generations_per_month: int = Field(default=100, description="Monthly UI generations")
    max_storage_mb: int = Field(default=1000, description="Storage limit in MB")
    max_users: int = Field(default=5, description="Maximum users per tenant")
    max_agents: int = Field(default=10, description="Maximum AI agents")


class Tenant(BaseModel):
    """Tenant model for multi-tenancy."""
    tenant_id: str = Field(..., description="Unique tenant identifier")
    name: str = Field(..., description="Tenant name")
    status: TenantStatus = Field(default=TenantStatus.ACTIVE)
    plan: TenantPlan = Field(default=TenantPlan.FREE)
    quotas: TenantQuotas = Field(default_factory=TenantQuotas)
    settings: Dict[str, any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TenantContext(BaseModel):
    """Tenant context for request processing."""
    tenant_id: str
    permissions: List[str] = Field(default_factory=list)
    quotas: TenantQuotas
    metadata: Dict[str, any] = Field(default_factory=dict)


class TenantUsage(BaseModel):
    """Track tenant resource usage."""
    tenant_id: str
    api_calls_today: int = 0
    ui_generations_this_month: int = 0
    storage_used_mb: float = 0.0
    active_users: int = 0
    last_activity: Optional[datetime] = None
