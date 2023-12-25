from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL

from app.settings import settings
from app.models.user import TokenResp
from app.utils.security.jwt import create_token
from app.repositories.users_repo import UsersRepo
from app.repositories.identity_repo import IdentityRepo
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
def authorize(
    code: str,
    state: UUID,
    users_repo: UsersRepo = Depends(),
    identity_repo: IdentityRepo = Depends(),
    redirect_url_repo: RedirectUrlRepo = Depends()
):
    try:
        token = identity_repo.get_token_by_code(code)
        print(token)
        user = identity_repo.get_user(token)
        print(user)
        users_repo.add_user(user)
        print('User added...')

        redirect_url = URL(redirect_url_repo.get_redirect_url(state)).include_query_params(token=create_token(user))

        return RedirectResponse(redirect_url)
    except:
        raise HTTPException(401)
