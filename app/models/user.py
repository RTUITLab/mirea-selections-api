from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class PermissionNames(Enum):
    ADMIN = 'admin'

    VOTING_ADMIN = 'voting.admin'
    VOTING_ANALYTICS = 'voting.analytics'
    VOTING_EDITOR = 'voting.editor'

    USER_ADMIN = 'user.admin'
    USER_VIEWER = 'user.viewer'


class Permission(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PermissionNames
    title: str
    global_description: str
    local_description: str


class UserPermission(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    permission: PermissionNames
    voting_id: UUID | None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str

    permissions: list[UserPermission] = []
