from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.database import db_dep
from app.models.nomination import Vote
from app.schemas.user import User as DbUser
from app.schemas.vote import Vote as DbVote


users: list[User] = []


class UsersRepo:
    db: Session

    def __init__(self, db: Session = db_dep) -> None:
        self.db = db
        
    def get_by_id(self, id: UUID) -> User | None:
        user = self.db.execute(
            select(DbUser).where(DbUser.id == id)
        ).scalar_one_or_none()

        return User.from_orm(user) if user != None else None

    def get_nomination_vote(self, user_id: UUID, nomination_id: UUID) -> Vote | None:
        vote = self.db.execute(
            select(DbVote).where(DbVote.nomination_id == nomination_id, DbVote.voter_id == user_id)
        ).scalar_one_or_none()

        return Vote.from_orm(vote) if vote != None else None