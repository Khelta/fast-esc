import requests
import json

from collections import defaultdict

from src.database import get_session
from src.models.country import Country
from src.models.data_import import DataImportContest, DataImportSong
from src.routers.dataimport.contest import import_contest_data
from src.routers.dataimport.country import import_country_data
from src.routers.dataimport.song import import_song_data


BASE_URL = "https://raw.githubusercontent.com/Khelta/eurovision-scraper/refs/heads/master/data/"


def seed_database():
    seed_countries()
    seed_contest()
    seed_songs()


def seed_countries():
    session = next(get_session())
    r = requests.request("GET", BASE_URL + "country_codes.json")
    try:
        request_data = json.loads(r.text)
        model_data = [Country.model_validate(country) for country in request_data]
        import_country_data(session=session, data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")


def seed_contest():
    session = next(get_session())
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


def seed_songs():
    session = next(get_session())
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
