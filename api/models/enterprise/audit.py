"""
Audit logging models.
Phase 5: Enterprise Features
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AuditEventType(str, Enum):
    """Types of audit events."""
    # Authentication
    LOGIN = "auth.login"
    LOGOUT = "auth.logout"
    LOGIN_FAILED = "auth.login_failed"
    TOKEN_CREATED = "auth.token_created"
    TOKEN_REVOKED = "auth.token_revoked"
    
    # Authorization
    PERMISSION_GRANTED = "authz.permission_granted"
    PERMISSION_DENIED = "authz.permission_denied"
    
    # Data Access
    DATA_READ = "data.read"
    DATA_WRITE = "data.write"
    DATA_DELETE = "data.delete"
    DATA_EXPORT = "data.export"
    
    # Configuration
    CONFIG_UPDATE = "config.update"
    QUOTA_UPDATE = "quota.update"
    
    # Admin Actions
    USER_CREATED = "admin.user_created"
    USER_UPDATED = "admin.user_updated"
    USER_DELETED = "admin.user_deleted"
    TENANT_CREATED = "admin.tenant_created"
    TENANT_UPDATED = "admin.tenant_updated"
    TENANT_SUSPENDED = "admin.tenant_suspended"
    
    # API Calls
    API_CALL = "api.call"
    API_ERROR = "api.error"
    
    # Agent Execution
    AGENT_EXECUTED = "agent.executed"
    AGENT_FAILED = "agent.failed"
    
    # Security Events
    SECURITY_ALERT = "security.alert"
    RATE_LIMIT_EXCEEDED = "security.rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "security.suspicious_activity"


class AuditSeverity(str, Enum):
    """Audit event severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLog(BaseModel):
    """Audit log entry."""
    log_id: str = Field(..., description="Unique log identifier")
    tenant_id: str = Field(..., description="Tenant identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    event_type: AuditEventType = Field(..., description="Type of event")
    severity: AuditSeverity = Field(default=AuditSeverity.INFO)
    resource_type: Optional[str] = Field(None, description="Type of resource affected")
    resource_id: Optional[str] = Field(None, description="ID of resource affected")
    action: str = Field(..., description="Action performed")
    result: str = Field(..., description="Result of action (success/failure)")
    ip_address: Optional[str] = Field(None, description="IP address of client")
    user_agent: Optional[str] = Field(None, description="User agent string")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "log_id": "log_123",
                "tenant_id": "tenant_456",
                "user_id": "user_789",
                "event_type": "auth.login",
                "severity": "info",
                "action": "User login",
                "result": "success",
                "ip_address": "192.168.1.1",
                "timestamp": "2025-11-18T05:47:00Z"
            }
        }
