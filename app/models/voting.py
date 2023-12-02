from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.user import User
from app.models.nomination import Nomination


class Voting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = uuid4()
    creation_date: datetime = datetime.now()
    title: str
    description: str | None

    publish_date: datetime | None
    start_date: datetime | None
    finish_date: datetime | None

    users: list[User]
    nominations: list[Nomination]


class Voter(BaseModel):
    id: str
    name: str
    email: str
    unit: str


class Vote(BaseModel):
    vote_date: datetime = datetime.now()
    voting_id: str
    nominant_id: str
    voter: Voter
