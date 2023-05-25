import aiohttp


from fastapi import FastAPI, APIRouter

from app.api.api import router as api_router


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()


aiohttp_session = None
@app.on_event("startup")
async def startup_event():
    global aiohttp_session
    aiohttp_session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown_event():
    await aiohttp_session.close()


app.include_router(api_router)
