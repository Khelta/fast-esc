from fastapi import FastAPI

from fastesc.api.routers.main import router

app = FastAPI()

app.include_router(router)
