from typing import List
from uuid import uuid4

from fastapi import APIRouter

from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.components.projects.model import Project
from tdcwebapi.components.security import api as security


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)
queue = MessageQueueSingleton()

_general_uuid = uuid4()
_projects = {
    _general_uuid: Project(id=_general_uuid, name="Frais Généraux")
}
_clients_need_reload = False


@router.get("/", name="")
async def get(auth_result: str = security.http()) -> List[Project]:
    global _projects
    return list(_projects.values())


@router.post("/", name="")
async def new(auth_result: str = security.http()) -> Project:
    global _projects
    new_project = Project(id=uuid4(), name="New Project")
    _projects[new_project.id] = new_project
    await queue.messages.put("projects_reload")
    return new_project


@router.put("/", name="")
async def update(project: Project, auth_result: str = security.http()) -> None:
    global _projects
    await queue.messages.put("projects_reload")
    _projects[project.id] = project


@router.delete("/", name="")
async def remove(project: Project, auth_result: str = security.http()) -> None:
    global _projects
    await queue.messages.put("projects_reload")
    _projects.pop(project.id)
