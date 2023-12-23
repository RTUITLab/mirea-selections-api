from uuid import UUID, uuid4
from fastapi import Depends
from memcache import Client

from app.utils.store import get_store


class RedirectUrlRepo:
    mc: Client

    def __init__(self, mc: Client = Depends(get_store)) -> None:
        self.mc = mc

    def set_redirect_url(self, redirect_url: str) -> tuple[UUID, str]:
        state = uuid4()
        self.mc.set(f'redirect_url_{state}', redirect_url, time=100)
        return (state, redirect_url)

    def get_redirect_url(self, state: UUID) -> str | None:
        return self.mc.get(f'redirect_url_{state}')
