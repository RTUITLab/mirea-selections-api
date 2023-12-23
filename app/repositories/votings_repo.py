from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from app.models.voting import Voting
from app.utils.database import db_dep
from app.schemas.vote import Vote as DbVote
from app.schemas.voting import Voting as DbVoting

votings: list[Voting] = []


class VotingsRepo:
    def __init__(self, db: Session = db_dep) -> None:
        self.db = db

    def _from_orm(self, voting: DbVoting | None) -> Voting | None:
        if voting == None:
            return None

        return Voting.from_orm(voting)

    def get_by_id(self, id: UUID) -> Voting | None:
        voting = self.db.execute(
            select(DbVoting).where(DbVoting.id == id)
        ).scalar_one_or_none()

        return self._from_orm(voting)

    def get_active(self) -> Voting | None:
        voting = self.db.execute(
            select(DbVoting).where(DbVoting.active == True)
        ).scalar_one_or_none()

        return self._from_orm(voting)

    def create_voting(self, voting: Voting) -> Voting:
        new_voting = DbVoting(**voting.dict(exclude={'users', 'nominations'}))
        self.db.add(new_voting)
        self.db.commit()

        return Voting.from_orm(new_voting)

    def set_active(self, voting: Voting) -> Voting:
        self.db.execute(
            update(DbVoting).where(
                DbVoting.active == True).values(active=False)
        )

        new_voting = self.db.execute(
            update(DbVoting).where(DbVoting.id == voting.id).values(
                active=True).returning(DbVoting),
        ).scalar_one()

        self.db.commit()

        return self._from_orm(new_voting)

    def delete_nomination_votes(self, nomination_id: UUID) -> None:
        self.db.execute(
            delete(DbVote).where(DbVote.nomination_id == nomination_id)
        )

        self.db.commit()
