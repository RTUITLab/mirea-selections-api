import uuid
from typing import Optional
from sqlalchemy import UUID, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base_schema import Base
from app.schemas import User, UserPermission, Nomination


class Voting(Base):
    __tablename__ = 'votings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    active: Mapped[bool]

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finish_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    users: Mapped[list[User]] = relationship(secondary=UserPermission.__table__, viewonly=True)
    nominations: Mapped[list[Nomination]] = relationship(viewonly=True)
