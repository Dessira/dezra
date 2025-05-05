from typing import Union
from typing import Annotated

from fastapi import Depends, FastAPI
from .internal import admin
from .routers import items, users, shops, auth
from .database import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield  # Startup complete, app is running
    # Optional: Do cleanup after app shutdown here

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(shops.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
