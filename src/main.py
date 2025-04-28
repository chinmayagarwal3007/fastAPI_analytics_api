from typing import Union
from fastapi import FastAPI
from .api.events.routing import router as event_router
from contextlib import asynccontextmanager
from .db import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_db()
    yield

app = FastAPI(lifespan = lifespan)
app.include_router(event_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healtz")
def read_api_health():
    return {"status": "ok"}