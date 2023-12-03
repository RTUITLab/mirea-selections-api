from uuid import UUID
from fastapi import Depends

from app.models.nomination import Vote
from app.repositories.users_repo import UsersRepo


class UserService:
    def __init__(
        self,
        users_repo: UsersRepo = Depends(UsersRepo)
    ) -> None:
        self.users_repo = users_repo

    def get_nomination_vote(self, nomination_id: UUID, user_id: UUID) -> Vote:
        vote = self.users_repo.get_nomination_vote(user_id, nomination_id)
        if vote == None:
            raise KeyError

        return vote