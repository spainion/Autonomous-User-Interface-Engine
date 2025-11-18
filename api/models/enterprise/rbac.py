"""
RBAC (Role-Based Access Control) models.
Phase 5: Enterprise Features
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    """User roles in the system."""
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    SERVICE_ACCOUNT = "service_account"


class Permission(str, Enum):
    """System permissions."""
    # UI Generation
    UI_GENERATE = "ui:generate"
    UI_VIEW = "ui:view"
    UI_DELETE = "ui:delete"
    
    # Context Management
    CONTEXT_READ = "context:read"
    CONTEXT_WRITE = "context:write"
    CONTEXT_DELETE = "context:delete"
    
    # Agent Management
    AGENT_EXECUTE = "agent:execute"
    AGENT_MANAGE = "agent:manage"
    
    # Tenant Management
    TENANT_READ = "tenant:read"
    TENANT_MANAGE = "tenant:manage"
    
    # User Management
    USER_READ = "user:read"
    USER_MANAGE = "user:manage"
    
    # Analytics
    ANALYTICS_VIEW = "analytics:view"
    
    # Admin
    ADMIN_ALL = "admin:all"


# Role permissions mapping
ROLE_PERMISSIONS = {
    Role.SUPER_ADMIN: [Permission.ADMIN_ALL],
    Role.TENANT_ADMIN: [
        Permission.UI_GENERATE, Permission.UI_VIEW, Permission.UI_DELETE,
        Permission.CONTEXT_READ, Permission.CONTEXT_WRITE, Permission.CONTEXT_DELETE,
        Permission.AGENT_EXECUTE, Permission.AGENT_MANAGE,
        Permission.TENANT_READ, Permission.TENANT_MANAGE,
        Permission.USER_READ, Permission.USER_MANAGE,
        Permission.ANALYTICS_VIEW,
    ],
    Role.DEVELOPER: [
        Permission.UI_GENERATE, Permission.UI_VIEW,
        Permission.CONTEXT_READ, Permission.CONTEXT_WRITE,
        Permission.AGENT_EXECUTE,
    ],
    Role.ANALYST: [
        Permission.UI_VIEW,
        Permission.CONTEXT_READ,
        Permission.ANALYTICS_VIEW,
    ],
    Role.SERVICE_ACCOUNT: [
        Permission.UI_GENERATE,
        Permission.CONTEXT_READ, Permission.CONTEXT_WRITE,
        Permission.AGENT_EXECUTE,
    ],
}


class User(BaseModel):
    """User model with RBAC."""
    user_id: str = Field(..., description="Unique user identifier")
    tenant_id: str = Field(..., description="Tenant identifier")
    email: str = Field(..., description="User email")
    role: Role = Field(default=Role.DEVELOPER)
    permissions: List[Permission] = Field(default_factory=list)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


class APIKey(BaseModel):
    """API key for programmatic access."""
    key_id: str
    tenant_id: str
    user_id: str
    name: str
    key_hash: str
    permissions: List[Permission]
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
