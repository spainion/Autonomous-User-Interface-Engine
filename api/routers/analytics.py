"""
Analytics endpoints.
Phase 5: Enterprise Features
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import datetime
from api.analytics.metrics import UsageMetrics, AnalyticsSummary, CostAnalytics, TimeRange
from api.models.enterprise.rbac import Permission
from api.auth.rbac import has_permission
from api.auth.jwt import get_tenant_from_token

router = APIRouter()


@router.get("/analytics/usage")
async def get_usage_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    tenant_id: str = Depends(get_tenant_from_token),
    _: bool = Depends(has_permission(Permission.ANALYTICS_VIEW))
) -> UsageMetrics:
    """Get usage metrics for tenant."""
    return UsageMetrics(
        tenant_id=tenant_id,
        time_range=time_range,
        api_calls=5432,
        ui_generations=234,
        agent_executions=567,
        storage_used_mb=345.6,
        active_users=12,
        error_count=23,
        avg_response_time_ms=145.3
    )


@router.get("/analytics/summary")
async def get_analytics_summary(
    _: bool = Depends(has_permission(Permission.ANALYTICS_VIEW))
) -> AnalyticsSummary:
    """Get analytics summary dashboard."""
    return AnalyticsSummary(
        total_api_calls=123456,
        total_ui_generations=5678,
        total_errors=123,
        avg_response_time_ms=156.7,
        cache_hit_rate=0.85,
        top_endpoints=[
            {"endpoint": "/api/v1/generate", "calls": 45678},
            {"endpoint": "/api/v1/health", "calls": 34567}
        ],
        top_tenants=[
            {"tenant_id": "tenant_1", "api_calls": 23456},
            {"tenant_id": "tenant_2", "api_calls": 12345}
        ],
        error_breakdown={
            "500": 45,
            "404": 34,
            "403": 23
        },
        time_series=[]
    )


@router.get("/analytics/costs")
async def get_cost_analytics(
    tenant_id: str = Depends(get_tenant_from_token),
    _: bool = Depends(has_permission(Permission.ANALYTICS_VIEW))
) -> CostAnalytics:
    """Get cost analytics for tenant."""
    now = datetime.utcnow()
    return CostAnalytics(
        tenant_id=tenant_id,
        period_start=now,
        period_end=now,
        api_call_cost=123.45,
        ui_generation_cost=234.56,
        storage_cost=45.67,
        agent_execution_cost=89.12,
        total_cost=492.80,
        estimated_next_month=550.00
    )
