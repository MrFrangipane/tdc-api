import asyncio
from typing import List
from uuid import uuid4

from fastapi import APIRouter, WebSocket
from websockets.exceptions import ConnectionClosedError

from tdcwebapi.projects.model import Project


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

_general_uuid = uuid4()
_projects = {
    _general_uuid: Project(id=_general_uuid, name="Frais Généraux")
}
_clients_need_reload = False


@router.get("/")
def get() -> List[Project]:
    global _projects
    return list(_projects.values())


@router.post("/")
def new() -> Project:
    global _projects
    global _clients_need_reload
    new_project = Project(id=uuid4(), name="New Project")
    _projects[new_project.id] = new_project
    _clients_need_reload = True
    return new_project


@router.put("/")
def update(project: Project) -> None:
    global _projects
    _projects[project.id] = project


@router.delete("/")
def remove(project: Project) -> None:
    global _projects
    global _clients_need_reload
    _clients_need_reload = True
    _projects.pop(project.id)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global _clients_need_reload
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(0.01)

            if _clients_need_reload:
                await websocket.send_text("projects_reload")
                _clients_need_reload = False
            else:
                await websocket.send_text("")

    except ConnectionClosedError:
        pass
