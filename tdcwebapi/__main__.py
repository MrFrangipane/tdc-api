from fastapi import FastAPI

from tdcwebapi import configurator  # must be imported before anything else (could be better)
from tdcwebapi.components.expenses.routes import router as router_expenses
from tdcwebapi.components.projects.routes import router as router_projects
from tdcwebapi.components.multiplayer.routes import router as router_multiplayer


app = FastAPI(title="TDC API")
app.include_router(router_multiplayer)
app.include_router(router_projects)
app.include_router(router_expenses)


@app.get("/")
def root():
    return {"message": "Hello TDC API"}
