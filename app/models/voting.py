from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.user import User
from app.models.nomination import Nomination, NominationCompact


class Voting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    creation_date: datetime = Field(default_factory=datetime.utcnow)
    title: str
    description: str
    active: bool = False

    start_date: datetime
    finish_date: datetime

    users: list[User] = []
    nominations: list[Nomination] = []


class CreateVotingReq(BaseModel):
    title: str
    description: str = ""
    start_date: datetime
    finish_date: datetime
    admin: UUID | None = None


class ActiveVotingResp(Voting):
    users: list[User] = Field(exclude=True)
    nominations: list[NominationCompact]

# TODO: PublishDate
