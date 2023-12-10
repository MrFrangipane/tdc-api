from fastapi import FastAPI

from tdcwebapi.expenses.routes import router as router_expenses
from tdcwebapi.projects.routes import router as router_projects


app = FastAPI(title="TDC API")
app.include_router(router_expenses)
app.include_router(router_projects)


@app.get("/")
def root():
    return {"message": "Hello TDC API"}
