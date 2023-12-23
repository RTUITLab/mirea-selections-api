from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.settings import settings
from app.models.user import TokenResp
from app.services.user_service import UserService
from app.repositories.redirect_url_repo import RedirectUrlRepo


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.get('/login')
def login(redirect_url: str, redirect_url_repo: RedirectUrlRepo = Depends()):
    state = redirect_url_repo.set_redirect_url(redirect_url)[0]
    return RedirectResponse(settings.oauth2_authorization_url +
                            '?grant_type=authorization-code&response_type=code&' +
                            f'client_id={settings.oauth2_client_id}&scope=basic student employee&' +
                            f'state={state}')


@auth_router.get('/logincallback')
def authorize(code: str, state: UUID, redirect_url_repo: RedirectUrlRepo = Depends()):
    return redirect_url_repo.get_redirect_url(state) or 'bbb'


@auth_router.post('/token')
def get_token(user_id: UUID, user_service: UserService = Depends(UserService)) -> TokenResp:
    try:
        return user_service.create_user_token(user_id)
    except PermissionError:
        raise HTTPException(status_code=403)
