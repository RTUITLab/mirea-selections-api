from uuid import UUID, uuid4
from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.models.user import PermissionNames


oauth2_scheme = APIKeyHeader(name='Authorization')


class JwtAuthDep:
    permission: PermissionNames

    def __init__(self, permission: PermissionNames) -> None:
        self.permission = permission

    def __call__(self, token: str = Depends(oauth2_scheme)) -> UUID:
        return uuid4()