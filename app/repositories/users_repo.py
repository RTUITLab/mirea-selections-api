from uuid import UUID
from sqlalchemy import select, insert
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

    def add_user(self, user: User) -> User:
        old_user_data = self.db.execute(
            select(DbUser).where(DbUser.id == user.id)
        ).scalar_one_or_none()

        if (old_user_data == None):
            user_data = DbUser(**user.dict())
            self.db.add(user_data)
            self.db.commit()
            return User.from_orm(user_data)
        else:
            old_user_data.email = user.email
            old_user_data.name = user.name
            old_user_data.unit = user.unit
            self.db.commit()
            return User.from_orm(old_user_data)

    def get_nomination_vote(self, user_id: UUID, nomination_id: UUID) -> Vote | None:
        vote = self.db.execute(
            select(DbVote).where(DbVote.nomination_id ==
                                 nomination_id, DbVote.voter_id == user_id)
        ).scalar_one_or_none()

        return Vote.from_orm(vote) if vote != None else None

    def add_vote(self, nomination_id: UUID, nominant_id: UUID, user_id: UUID) -> Vote:
        vote = self.db.execute(
            select(DbVote).where(DbVote.nomination_id ==
                                 nomination_id and DbVote.voter_id == user_id)
        ).scalar_one_or_none()

        if vote != None:
            raise ValueError

        vote = DbVote(**Vote(nominant_id=nominant_id,
                      nomination_id=nomination_id).dict(exclude='voter'))
        vote.voter_id = user_id
        self.db.add(vote)
        self.db.commit()

        return Vote.from_orm(vote)
