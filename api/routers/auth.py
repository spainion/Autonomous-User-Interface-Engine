"""
Authentication endpoints.
Phase 5: Enterprise Features
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from api.auth.jwt import create_access_token
from api.models.enterprise.rbac import Role

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


@router.post("/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest) -> LoginResponse:
    """Authenticate user and return JWT token."""
    # In production, verify credentials against database
    # This is a simplified example
    
    if credentials.email == "admin@example.com" and credentials.password == "admin":
        token_data = {
            "user_id": "user_123",
            "tenant_id": "tenant_456",
            "email": credentials.email,
            "role": Role.TENANT_ADMIN.value
        }
        
        access_token = create_access_token(data=token_data)
        
        return LoginResponse(access_token=access_token)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )


@router.post("/auth/logout")
async def logout() -> dict:
    """Logout user (invalidate token)."""
    # In production, add token to blacklist
    return {"message": "Successfully logged out"}


@router.post("/auth/refresh")
async def refresh_token() -> LoginResponse:
    """Refresh access token."""
    # In production, verify refresh token and issue new access token
    return LoginResponse(access_token="new_token_here")
