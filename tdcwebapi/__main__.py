import uvicorn
from fastapi import FastAPI

from tdcwebapi import configurator  # FIXME: must be imported before anything else
from tdcwebapi.components.expenses.routes import router as router_expenses
from tdcwebapi.components.multiplayer.routes import router as router_multiplayer
from tdcwebapi.components.projects.routes import router as router_projects
from tdcwebapi.components.users.routes import router as router_users


app = FastAPI(title="TDC API")
app.include_router(router_expenses)
app.include_router(router_multiplayer)
app.include_router(router_projects)
app.include_router(router_users)


@app.get("/")
def root():
    return {"message": "Hello TDC API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
