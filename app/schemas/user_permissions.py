import uuid
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.base_schema import Base
from app.models.user import PermissionNames


class UserPermission(Base):
    __tablename__ = 'user_permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    voting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('votings.id'))
    permission: Mapped[PermissionNames]
