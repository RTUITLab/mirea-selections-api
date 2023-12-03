from uuid import UUID, uuid4
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.models.user import PermissionNames
from app.utils.security import validate_token


auth_scheme = APIKeyHeader(name='Authorization')


class JwtAuthDep:
    permission: PermissionNames

    def __init__(self, permission: PermissionNames) -> None:
        self.permission = permission

    def __call__(self, token: str = Depends(auth_scheme)) -> UUID:
        try:
            user_id = validate_token(token.split('Bearer ')[1])
            return UUID(user_id)
        except:
            raise HTTPException(403)