from datetime import date
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter

from tdcwebapi.expenses.model import Expense
from tdcwebapi.projects.model import Project


_default_project = Project(
    id=uuid4(),
    name="Frais Généraux"
)


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)


@router.post("/")
def post(expense: Expense):
    return "OK"


@router.get("/")
def get(
        name: str | None = None,
        amount_min: float | None = None,
        amount_max: float | None = None,
        date_min: date | None = None,
        date_max: date | None = None,
        needs_refund: bool | None = None,
        refunded: bool | None = None,
        date_refund_min: date | None = None,
        date_refund_max: date | None = None
) -> List[Expense]:
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


@router.get("/{expense_id}")
def get(expense_id: UUID) -> Expense:
    return Expense(
        id=expense_id,
        caption="Achat tissu",
        amount=130.19,
        date_=date.today(),
        project=_default_project
    )