from fastapi import APIRouter

from tdcwebapi.components.authentication import api as authentication
from tdcwebapi.components.users.model import User


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", name="")
def get(user: User = authentication.for_request()) -> User:
    return user
