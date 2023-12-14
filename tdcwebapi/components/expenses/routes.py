from datetime import date
from uuid import UUID, uuid4

from fastapi import APIRouter

from tdcwebapi.components.authentication import api as authentication
from tdcwebapi.components.expenses.model import Expense
from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.components.projects.model import Project
from tdcwebapi.components.users.model import User


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)
_default_project = Project(
    id=uuid4(),
    name="Frais Généraux"
)
queue = MessageQueueSingleton()


@router.get("/{project_id}/expenses", name="")
async def get_project(project_id: UUID, user: User = authentication.for_request()) -> list[Expense]:
    await queue.messages.put("expenses_reload")
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
async def post(project_id: UUID, expense: Expense, user: User = authentication.for_request()) -> Expense:
    await queue.messages.put("expenses_reload")
    new_expense = Expense(
        id=uuid4(),
        caption="New Expense",
        amount=0,
        date_=date.today(),
        project=_default_project
    )
    return new_expense


@router.put("/", name="")
async def update(project: Expense, user: User = authentication.for_request()) -> None:
    await queue.messages.put("expenses_reload")


@router.delete("/", name="")
async def remove(project: Expense, user: User = authentication.for_request()) -> None:
    await queue.messages.put("expenses_reload")
