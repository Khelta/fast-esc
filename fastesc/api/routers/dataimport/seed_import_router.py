import json
from typing import Annotated

import requests
from fastapi import Depends, APIRouter

from fastesc.api.dependencies import get_repository
from fastesc.api.models.data_import import DataImportContest
from fastesc.api.models.data_import import DataImportSong
from fastesc.api.models.models import CountryBase
from fastesc.api.routers.dataimport.contest_import_router import import_contest_data
from fastesc.api.routers.dataimport.country_import_router import import_country_data
from fastesc.api.routers.dataimport.song_import_router import import_song_data
from fastesc.database.models.models import Affiliation as DB_Affiliation, Artist as DB_Artist, \
    Broadcaster as DB_Broadcaster, City as DB_City, Contest as DB_Contest, Country as DB_Country, \
    Location as DB_Location, Participation as DB_Participation, Person as DB_Person, Song as DB_Song
from fastesc.database.repositories.base_repo import DatabaseRepository

AffiliationRepository = Annotated[
    DatabaseRepository[DB_Affiliation],
    Depends(get_repository(DB_Affiliation))
]
ArtistRepository = Annotated[
    DatabaseRepository[DB_Artist],
    Depends(get_repository(DB_Artist))
]
BroadcasterRepository = Annotated[
    DatabaseRepository[DB_Broadcaster],
    Depends(get_repository(DB_Broadcaster))
]
CityRepository = Annotated[
    DatabaseRepository[DB_City],
    Depends(get_repository(DB_City))
]
ContestRepository = Annotated[
    DatabaseRepository[DB_Contest],
    Depends(get_repository(DB_Contest))
]
CountryRepository = Annotated[
    DatabaseRepository[DB_Country],
    Depends(get_repository(DB_Country))
]
LocationRepository = Annotated[
    DatabaseRepository[DB_Location],
    Depends(get_repository(DB_Location))
]
ParticipationRepository = Annotated[
    DatabaseRepository[DB_Participation],
    Depends(get_repository(DB_Participation))
]
PersonRepository = Annotated[
    DatabaseRepository[DB_Person],
    Depends(get_repository(DB_Person))
]
SongRepository = Annotated[
    DatabaseRepository[DB_Song],
    Depends(get_repository(DB_Song))
]

router = APIRouter(prefix="/data_import", tags=["import"])
BASE_URL = "https://raw.githubusercontent.com/Khelta/eurovision-scraper/refs/heads/master/data/"


async def seed_countries(country_repository: CountryRepository):
    r = requests.request("GET", BASE_URL + "country_codes.json")
    try:
        request_data = json.loads(r.text)
        model_data = [CountryBase.model_validate(country) for country in request_data]
        await import_country_data(repository=country_repository, data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")


async def seed_contest(affiliation_repository: AffiliationRepository,
                       broadcaster_repository: BroadcasterRepository,
                       city_repository: CityRepository,
                       contest_repository: ContestRepository,
                       country_repository: CountryRepository,
                       location_repository: LocationRepository,
                       person_repository: PersonRepository):
    r = requests.request("GET", BASE_URL + "contest.json")
    try:
        request_data = json.loads(r.text)
        model_data = [
            DataImportContest.model_validate(contest) for contest in request_data
        ]
        await import_contest_data(affiliation_repository=affiliation_repository,
                                  broadcaster_repository=broadcaster_repository,
                                  city_repository=city_repository,
                                  contest_repository=contest_repository,
                                  country_repository=country_repository,
                                  location_repository=location_repository,
                                  person_repository=person_repository,
                                  data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")
        raise e


async def seed_songs(affiliation_repository: AffiliationRepository,
                     artist_repository: ArtistRepository,
                     contest_repository: ContestRepository,
                     country_repository: CountryRepository,
                     participation_repository: ParticipationRepository,
                     person_repository: PersonRepository,
                     song_repository: SongRepository):
    r = requests.request("GET", BASE_URL + "songs.json")
    try:
        request_data = json.loads(r.text)
        model_data = [
            DataImportSong.model_validate(contest) for contest in request_data
        ]
        await import_song_data(affiliation_repository=affiliation_repository,
                               artist_repository=artist_repository,
                               contest_repository=contest_repository,
                               country_repository=country_repository,
                               participation_repository=participation_repository,
                               person_repository=person_repository,
                               song_repository=song_repository,
                               data=model_data)
    except requests.HTTPError as e:
        print(f"HTTP error occured: {e}")
        raise e


@router.get("/seed/", response_model=str)
async def seed_init_database(affiliation_repository: AffiliationRepository,
                             artist_repository: ArtistRepository,
                             broadcaster_repository: BroadcasterRepository,
                             city_repository: CityRepository,
                             contest_repository: ContestRepository,
                             country_repository: CountryRepository,
                             location_repository: LocationRepository,
                             participation_repository: ParticipationRepository,
                             person_repository: PersonRepository,
                             song_repository: SongRepository,
                             countries: bool = True,
                             contests: bool = True,
                             songs: bool = True,
                             ):
    if countries:
        await seed_countries(country_repository=country_repository)
    if contests:
        await seed_contest(affiliation_repository=affiliation_repository,
                           broadcaster_repository=broadcaster_repository,
                           city_repository=city_repository,
                           contest_repository=contest_repository,
                           country_repository=country_repository,
                           location_repository=location_repository,
                           person_repository=person_repository)
    if songs:
        await seed_songs(affiliation_repository=affiliation_repository,
                         artist_repository=artist_repository,
                         contest_repository=contest_repository,
                         country_repository=country_repository,
                         participation_repository=participation_repository,
                         person_repository=person_repository,
                         song_repository=song_repository)
    return "Seeding complete"
