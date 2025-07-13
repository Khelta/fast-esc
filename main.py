from fastapi import FastAPI

from database import create_db_and_tables
from routers.dataimport import contest, country

app = FastAPI()

app.include_router(country.router)
app.include_router(contest.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
