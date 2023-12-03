from uuid import UUID
from fastapi import Depends

from app.models.user import TokenResp
from app.models.nomination import Vote
from app.utils.security import create_token
from app.repositories.users_repo import UsersRepo


class UserService:
    def __init__(
        self,
        users_repo: UsersRepo = Depends(UsersRepo)
    ) -> None:
        self.users_repo = users_repo

    def create_user_token(self, user_id) -> str:
        user = self.users_repo.get_by_id(user_id)
        if user == None:
            raise PermissionError

        return TokenResp(user_id=user.id, token=create_token(user))

    def get_nomination_vote(self, nomination_id: UUID, user_id: UUID) -> Vote | None:
        vote = self.users_repo.get_nomination_vote(user_id, nomination_id)
        return vote

    def vote(self, nomination_id: UUID, nominant_id: UUID, user_id: UUID) -> Vote:
        return self.users_repo.add_vote(nomination_id, nominant_id, user_id)
        
