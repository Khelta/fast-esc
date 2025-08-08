from fastapi import FastAPI

from fastesc.database import create_db_and_tables
from fastesc.routers.dataimport import contest_import_router, country_import_router, song_import_router, \
    seed_import_router
from fastesc.routers.models import person_router

app = FastAPI()

app.include_router(contest_import_router.router)
app.include_router(country_import_router.router)
app.include_router(person_router.router)
app.include_router(seed_import_router.router)
app.include_router(song_import_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
