from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, APIRouter

from .app import api

app = FastAPI()
app.include_router(api.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")

executor = ThreadPoolExecutor()

