from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Nominant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str | None

    title: str
    short_description: str
    description: str

    video_url: str
