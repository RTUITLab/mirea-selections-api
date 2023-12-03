import uuid
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.base_schema import Base


class Nominant(Base):
    __tablename__ = 'nominants'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    slug: Mapped[str]

    title: Mapped[str]
    short_description: Mapped[str]
    description: Mapped[str]

    video_url: Mapped[str]

    nomination_id = mapped_column(ForeignKey('nominations.id', ondelete='CASCADE'))
