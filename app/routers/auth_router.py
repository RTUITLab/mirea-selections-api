from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


# @auth_router.get()
