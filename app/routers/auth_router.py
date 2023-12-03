from fastapi import APIRouter


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.get('/')
def get_token():
    pass