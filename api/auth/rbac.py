"""
Role-Based Access Control implementation.
Phase 5: Enterprise Features
"""

from fastapi import HTTPException, Depends
from typing import List
from api.models.enterprise.rbac import Permission, Role, ROLE_PERMISSIONS
from api.auth.jwt import verify_token


def has_permission(required_permission: Permission):
    """Dependency to check if user has required permission."""
    
    def permission_checker(token_data: dict = Depends(verify_token)) -> bool:
        user_role = token_data.get("role")
        
        if not user_role:
            raise HTTPException(status_code=403, detail="No role found in token")
        
        # Super admin has all permissions
        if user_role == Role.SUPER_ADMIN.value:
            return True
        
        # Check if role has the required permission
        try:
            role_enum = Role(user_role)
            role_permissions = ROLE_PERMISSIONS.get(role_enum, [])
            
            if required_permission in role_permissions:
                return True
        except ValueError:
            pass
        
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: {required_permission.value}"
        )
    
    return permission_checker


def require_role(required_role: Role):
    """Dependency to check if user has required role."""
    
    def role_checker(token_data: dict = Depends(verify_token)) -> bool:
        user_role = token_data.get("role")
        
        if not user_role:
            raise HTTPException(status_code=403, detail="No role found in token")
        
        if user_role == required_role.value or user_role == Role.SUPER_ADMIN.value:
            return True
        
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient role. Required: {required_role.value}"
        )
    
    return role_checker
