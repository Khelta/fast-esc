import json

import requests
from sqlmodel import Session

from fastesc.api.models import DataImportContest, DataImportSong
from fastesc.api.models.country import Country
from fastesc.routers.dataimport.contest_import_router import import_contest_data
from fastesc.routers.dataimport.country_import_router import import_country_data
from fastesc.routers.dataimport.song_import_router import import_song_data

BASE_URL = "https://raw.githubusercontent.com/Khelta/eurovision-scraper/refs/heads/master/data/"


def seed_database(session: Session):
    seed_countries(session)
    seed_contest(session)
    seed_songs(session)


def seed_countries(session: Session):
    r = requests.request("GET", BASE_URL + "country_codes.json")
    try:
        request_data = json.loads(r.text)
        model_data = [Country.model_validate(country) for country in request_data]
        import_country_data(session=session, data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")


def seed_contest(session: Session):
    r = requests.request("GET", BASE_URL + "contest.json")
    try:
        request_data = json.loads(r.text)
        model_data = [
            DataImportContest.model_validate(contest) for contest in request_data
        ]
        import_contest_data(session=session, data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")
        raise e


def seed_songs(session: Session):
    r = requests.request("GET", BASE_URL + "songs.json")
    try:
        request_data = json.loads(r.text)
        model_data = [
            DataImportSong.model_validate(contest) for contest in request_data
        ]
        import_song_data(session=session, data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")
        raise e
