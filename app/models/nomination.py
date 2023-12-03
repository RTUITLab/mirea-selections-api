from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field

from app.models.nominant import Nominant


class Nomination(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    title: str

    nominants: list[Nominant] = []
