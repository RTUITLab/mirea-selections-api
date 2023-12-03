from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.models.user import TokenResp
from app.services.user_service import UserService


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/token')
def get_token(user_id: UUID, user_service: UserService = Depends(UserService)) -> TokenResp:
    try:
        return user_service.create_user_token(user_id)
    except PermissionError:
        raise HTTPException(status_code=403)