from typing import Annotated, List
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TDC Web API")


class Expense(BaseModel):
    id: UUID
    caption: str
    amount: float


@app.get("/expenses/")
def read_expenses() -> List[Expense]:
    return [
        Expense(id=uuid4(), caption="Achat tissu", amount=130.19),
        Expense(id=uuid4(), caption="Achat lyres", amount=2503.0)
    ]


@app.post("/expenses/")
def post_expense(expense: Expense):
    return "OK"
