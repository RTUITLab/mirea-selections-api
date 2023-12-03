from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.voting import Voting
from app.models.nominant import Nominant
from app.models.user import PermissionNames
from app.models.nomination import Nomination
from app.repositories import UsersRepo, VotingsRepo, PermissionsRepo, NominationsRepo


class VotingService:
    votings_repo: VotingsRepo
    users_repo: UsersRepo
    permissions_repo: PermissionsRepo
    nominations_repo: NominationsRepo

    def __init__(
        self,
        votings_repo: VotingsRepo = Depends(VotingsRepo),
        permissions_repo: PermissionsRepo = Depends(PermissionsRepo),
        nominations_repo: NominationsRepo = Depends(NominationsRepo),
        users_repo: UsersRepo = Depends(UsersRepo)
    ) -> None:
        self.permissions_repo = permissions_repo
        self.nominations_repo = nominations_repo
        self.votings_repo = votings_repo
        self.users_repo = users_repo

    def get_one(self, active: bool | None = None, id: UUID | None = None) -> Voting:
        if (active == None or active == False) and id == None:
            return ValueError

        voting = self.votings_repo.get_active() if active else self.votings_repo.get_by_id(id)
        if voting == None:
            raise KeyError

        return voting

    def add_voting(self, title: str, description: str, start_date: datetime, finish_date: datetime, admin_id: UUID) -> Voting:
        voting = Voting(title=title, description=description,
                        start_date=start_date, finish_date=finish_date)
        self.votings_repo.create_voting(voting)
        self.attach_admin(voting.id, admin_id)

        return self.add_student_of_year_nominations(voting.id)

    def attach_admin(self, voting_id: UUID, user_id: UUID) -> Voting:
        voting = self.votings_repo.get_by_id(voting_id)
        user = self.users_repo.get_by_id(user_id)
        if user == None or voting == None:
            raise KeyError

        if not self.permissions_repo.add_user_permission(user_id, PermissionNames.ADMIN, voting_id):
            raise ValueError

        return self.votings_repo.get_by_id(voting_id)

    def add_student_of_year_nominations(self, voting_id: UUID) -> Voting:
        nominations = [Nomination(title='Студент года'), Nomination(
            title='Преподаватель года')]
        [self.nominations_repo.add_nomination(
            nom, voting_id) for nom in nominations]
        return self.votings_repo.get_by_id(voting_id)

    def activate_voting(self, id: UUID) -> Voting:
        voting = self.votings_repo.get_by_id(id)
        if voting == None:
            raise KeyError

        return self.votings_repo.set_active(voting)

    def add_nominant(self, voting_id: UUID, nomination_id: UUID, nominant: Nominant) -> Nominant:
        voting = self.votings_repo.get_by_id(voting_id)
        if voting == None:
            raise KeyError
        if not nomination_id in [n.id for n in voting.nominations]:
            raise ValueError

        return self.nominations_repo.add_nominant(nomination_id, nominant)

    def get_nomiantion(self, voting_id: UUID, nomination_id: UUID):
        nomination = self.nominations_repo.get_voting_nomination(
            voting_id, nomination_id)
        if nomination == None:
            raise KeyError

        return nomination

    def check_voting_status(self, voting_id: UUID, nomination_id: UUID) -> Nomination:
        voting = self.votings_repo.get_by_id(voting_id)
        nomination = self.nominations_repo.get_voting_nomination(
            voting_id, nomination_id)
        if voting == None or nomination == None:
            raise KeyError

        now = datetime.utcnow().timestamp()
        if voting.start_date.timestamp() > now or voting.finish_date.timestamp() < now or voting.active == False:
            raise ValueError

        return nomination
