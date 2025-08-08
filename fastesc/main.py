from fastapi import FastAPI

from fastesc.api.routers import song_import_router
from fastesc.api.routers.dataimport import country_import_router, contest_import_router, seed_import_router
from fastesc.api.routers.models import person_router
from fastesc.database import create_db_and_tables

app = FastAPI()

app.include_router(contest_import_router.router)
app.include_router(country_import_router.router)
app.include_router(person_router.router)
app.include_router(seed_import_router.router)
app.include_router(song_import_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
