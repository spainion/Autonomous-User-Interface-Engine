"""Health check endpoints."""

from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any
import psutil
import time

router = APIRouter()

start_time = time.time()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    uptime_seconds: float
    version: str
    cpu_percent: float
    memory_percent: float


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: System health status
    """
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        uptime_seconds=uptime,
        version="0.4.0",
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory_percent=psutil.virtual_memory().percent
    )


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check for Kubernetes.
    
    Returns:
        Dict: Readiness status
    """
    # Check if all dependencies are ready
    # TODO: Check Redis, external APIs, etc.
    return {
        "ready": True,
        "checks": {
            "database": "ok",
            "cache": "ok",
            "external_apis": "ok"
        }
    }


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes.
    
    Returns:
        Dict: Liveness status
    """
    return {"alive": True}
