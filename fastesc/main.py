from fastapi import FastAPI

from fastesc.api.routers.main import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the API. Visit /docs for documentation."}
