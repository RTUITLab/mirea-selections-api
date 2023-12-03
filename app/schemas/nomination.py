import uuid
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.base_schema import Base


class Nomination(Base):
    __tablename__ = 'nominations'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    voting_id = mapped_column(ForeignKey('votings.id'))
