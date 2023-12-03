import uuid
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base_schema import Base
from app.schemas.user_permissions import UserPermission

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

    permissions = relationship(UserPermission, viewonly=True)
