import uuid
from datetime import datetime
from sqlalchemy import UUID, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.user import User
from app.schemas.base_schema import Base


class Vote(Base):
    __tablename__ = 'votes'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    voter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    nominant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('nominants.id'))
    nomination_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('nominations.id'))
    voted_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    voter: Mapped[User] = relationship(back_populates='votes')
