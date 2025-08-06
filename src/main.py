from fastapi import FastAPI

from src.database import create_db_and_tables
from src.routers.dataimport import contest, country, song
from src.routers.models import person
from src.seed import seed_database

app = FastAPI()

app.include_router(country.router)
app.include_router(contest.router)
app.include_router(song.router)
app.include_router(person.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_database()
