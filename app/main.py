from fastapi import FastAPI
from .routers import todos, auth, user
from . import database

app = FastAPI()


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(user.router)