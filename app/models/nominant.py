from uuid import UUID, uuid4
from random import randint
from slugify import slugify
from pydantic import BaseModel, ConfigDict, model_validator, Field


class Nominant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    slug: str = ""

    title: str
    short_description: str
    description: str

    video_url: str

    @model_validator(mode='after')
    def gen_slug(self) -> str:
        if self.slug == "":
            self.slug = slugify(f'{self.title} {randint(0, 9999)}')
            return self
        return self
