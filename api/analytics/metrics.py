"""
Analytics and metrics collection.
Phase 5: Enterprise Features
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class MetricType(str, Enum):
    """Types of metrics to track."""
    API_CALLS = "api_calls"
    UI_GENERATIONS = "ui_generations"
    AGENT_EXECUTIONS = "agent_executions"
    CACHE_HITS = "cache_hits"
    ERRORS = "errors"
    RESPONSE_TIME = "response_time"
    STORAGE_USAGE = "storage_usage"
    USER_ACTIVITY = "user_activity"


class TimeRange(str, Enum):
    """Time range for analytics."""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class UsageMetrics(BaseModel):
    """Usage metrics for a tenant."""
    tenant_id: str
    time_range: TimeRange
    api_calls: int = 0
    ui_generations: int = 0
    agent_executions: int = 0
    storage_used_mb: float = 0.0
    active_users: int = 0
    error_count: int = 0
    avg_response_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyticsSummary(BaseModel):
    """Analytics summary for dashboard."""
    total_api_calls: int
    total_ui_generations: int
    total_errors: int
    avg_response_time_ms: float
    cache_hit_rate: float
    top_endpoints: List[Dict[str, any]]
    top_tenants: List[Dict[str, any]]
    error_breakdown: Dict[str, int]
    time_series: List[Dict[str, any]]


class CostAnalytics(BaseModel):
    """Cost analysis for tenant."""
    tenant_id: str
    period_start: datetime
    period_end: datetime
    api_call_cost: float = 0.0
    ui_generation_cost: float = 0.0
    storage_cost: float = 0.0
    agent_execution_cost: float = 0.0
    total_cost: float = 0.0
    estimated_next_month: float = 0.0
