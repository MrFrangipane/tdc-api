from uuid import UUID

from pydantic import BaseModel


class Project(BaseModel):
    id: UUID
    name: str
    description: str = ""
