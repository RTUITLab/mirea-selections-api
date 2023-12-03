from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.user import PermissionNames
from app.models.voting import Voting
from app.repositories.permissions_repo import PermissionsRepo
from app.repositories.votings_repo import VotingsRepo
from app.repositories.users_repo import UsersRepo


class VotingService:
    votings_repo: VotingsRepo
    users_repo: UsersRepo
    permissions_repo: PermissionsRepo

    def __init__(
        self,
        votings_repo: VotingsRepo = Depends(VotingsRepo),
        permissions_repo: PermissionsRepo = Depends(PermissionsRepo),
        users_repo: UsersRepo = Depends(UsersRepo)
    ) -> None:
        self.permissions_repo = permissions_repo
        self.votings_repo = votings_repo
        self.users_repo = users_repo

    def add_voting(self, title: str, description: str, start_date: datetime, finish_date: datetime, admin_id: UUID) -> Voting:
        voting = Voting(title=title, description=description,
                        start_date=start_date, finish_date=finish_date)
        self.votings_repo.create_voting(voting)

        return self.attach_admin(voting.id, admin_id)

    def attach_admin(self, voting_id: UUID, user_id: UUID) -> Voting:
        voting = self.votings_repo.get_by_id(voting_id)
        user = self.users_repo.get_by_id(user_id)
        if user == None or voting == None:
            raise KeyError

        if not self.permissions_repo.add_user_permission(user_id, PermissionNames.ADMIN, voting_id):
            raise ValueError

        return self.votings_repo.get_by_id(voting_id)
