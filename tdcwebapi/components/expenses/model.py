from uuid import UUID
from datetime import date

from pydantic import BaseModel

from tdcwebapi.components.projects.model import Project


class Expense(BaseModel):
    id: UUID
    project: Project
    caption: str
    amount: float
    date_: date
    needs_refund: bool = False
    refunded: bool | None = None
    date_refund: date | None = None
