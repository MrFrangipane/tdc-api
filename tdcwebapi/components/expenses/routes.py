from datetime import date
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter

from tdcwebapi.components.expenses.model import Expense
from tdcwebapi.components.projects.model import Project
from tdcwebapi.components.security import api as security


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)
_default_project = Project(
    id=uuid4(),
    name="Frais Généraux"
)


@router.get("/{project_id}/expenses", name="")
def get_project(project_id: UUID, auth_result: str = security.http()) -> List[Expense]:
    return [
        Expense(
            id=uuid4(),
            caption="Achat tissu",
            amount=130.19,
            date_=date.today(),
            project=_default_project
        ),
        Expense(
            id=uuid4(),
            caption="Achat lyres",
            amount=2503.0,
            date_=date.today(),
            project=_default_project
        )
    ]


@router.post("/{project_id}/expenses", name="")
def post(project_id: UUID, expense: Expense, auth_result: str = security.http()) -> Expense:
    new_expense = Expense(
        id=uuid4(),
        caption="New Expense",
        amount=0,
        date_=date.today(),
        project=_default_project
    )
    return new_expense


@router.put("/", name="")
def update(project: Expense, auth_result: str = security.http()) -> None:
    pass


@router.delete("/", name="")
def remove(project: Expense, auth_result: str = security.http()) -> None:
    pass