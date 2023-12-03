from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserPermission
from app.schemas.user import User as DbUser
from app.utils.database import db_dep


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