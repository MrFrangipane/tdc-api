from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter

from tdcwebapi.projects.model import Project


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.post("/")
def post(project: Project):
    return "OK"


@router.get("/")
def get(
        name: str | None = None,
) -> List[Project]:
    return [
        Project(id=uuid4(), name="Frais Généraux"),
        Project(id=uuid4(), name="Canal 211 #1"),
        Project(id=uuid4(), name="TMRLD 2024")
    ]


@router.get("/{project_id}")
def get(project_id: UUID) -> Project:
    return Project(id=uuid4(), name="Canal 211 #1")
