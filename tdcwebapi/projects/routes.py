from typing import List
from uuid import uuid4

from fastapi import APIRouter, Security

from tdcwebapi.projects.model import Project
from tdcwebapi.security.token_verifier import TokenVerifier


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)
_verifier = TokenVerifier()

_general_uuid = uuid4()
_projects = {
    _general_uuid: Project(id=_general_uuid, name="Frais Généraux")
}
_clients_need_reload = False


@router.get("/", name="")
def get(auth_result: str = Security(_verifier.verify_http)) -> List[Project]:
    global _projects
    return list(_projects.values())


@router.post("/", name="")
def new(auth_result: str = Security(_verifier.verify_http)) -> Project:
    global _projects
    new_project = Project(id=uuid4(), name="New Project")
    _projects[new_project.id] = new_project
    return new_project


@router.put("/", name="")
def update(project: Project, auth_result: str = Security(_verifier.verify_http)) -> None:
    global _projects
    _projects[project.id] = project


@router.delete("/", name="")
def remove(project: Project, auth_result: str = Security(_verifier.verify_http)) -> None:
    global _projects
    _projects.pop(project.id)
