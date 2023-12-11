from datetime import date
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Security

from tdcwebapi.expenses.model import Expense
from tdcwebapi.projects.model import Project
from tdcwebapi.security.token_verifier import TokenVerifier


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)
_verifier = TokenVerifier()

_default_project = Project(
    id=uuid4(),
    name="Frais Généraux"
)


@router.post("/")
def post(expense: Expense, auth_result: str = Security(_verifier.verify_http)):
    return "OK"


@router.get("/")
def get(auth_result: str = Security(_verifier.verify_http)) -> List[Expense]:
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
def get(expense_id: UUID, auth_result: str = Security(_verifier.verify_http)) -> Expense:
    return Expense(
        id=expense_id,
        caption="Achat tissu",
        amount=130.19,
        date_=date.today(),
        project=_default_project
    )


@router.get("/{project_id}/expenses")
def get_project(project_id: UUID, auth_result: str = Security(_verifier.verify_http)) -> List[Expense]:
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
