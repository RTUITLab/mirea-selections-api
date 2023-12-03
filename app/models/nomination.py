from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field


class Nomination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    title: str
