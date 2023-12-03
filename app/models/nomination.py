from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.user import User
from app.models.nominant import Nominant


class Nomination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    title: str

    nominants: list[Nominant] = []


class Vote(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    nominant_id: UUID
    nomination_id: UUID
    voted_date: datetime = Field(default_factory=datetime.utcnow)

    voter: User | None = None


class UserVote(Vote):
    voter: User | None = Field(exclude=True)

class UserNomination(Nomination):
    model_config = ConfigDict(from_attributes=True)

    vote: UserVote | None = None


class NominationCompact(Nomination):
    nominants: list[Nominant] = Field(exclude=True)
