from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.voting import Voting as DbVoting
from app.utils.database import db_dep
from app.models.voting import Voting

votings: list[Voting] = []


class VotingsRepo:
    def __init__(self, db: Session = db_dep) -> None:
        self.db = db

    def get_by_id(self, id: UUID) -> Voting | None:
        voting = self.db.execute(
            select(DbVoting).where(DbVoting.id == id)
        ).scalar_one_or_none()

        return Voting.from_orm(voting) if voting != None else None

    def create_voting(self, voting: Voting) -> Voting:
        new_voting = DbVoting(**voting.dict(exclude={'users', 'nominations'}))
        self.db.add(new_voting)
        self.db.commit()

        return Voting.from_orm(new_voting)
