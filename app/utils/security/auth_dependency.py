import re
from uuid import UUID
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader

from app.models.user import PermissionNames
from app.utils.security import validate_token


auth_scheme = APIKeyHeader(name='Authorization')


class JwtAuthDep:
    permission: PermissionNames

    def __init__(self, permission: PermissionNames) -> None:
        self.permission = permission

    def __call__(self, req: Request, token: str = Depends(auth_scheme)) -> UUID:
        try:
            if re.match(r'\/votings\/[a-z0-9\-]{36}\/nominations\/[a-z0-9\-]{36}', req.scope['path']):
                if token == 'Bearer ' or token == 'Bearer':
                    return UUID(int=0)

            user_id = validate_token(token.split('Bearer ')[1])
            return UUID(user_id)
        except:
            raise HTTPException(403)
