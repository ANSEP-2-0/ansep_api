# uvicorn main:app --reload --port 8001
import os
from fastapi import FastAPI
from routers import r_ms
from fastapi.middleware.cors import CORSMiddleware
from utils.api import origins


# APP
app = FastAPI()

app.include_router(r_ms.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


