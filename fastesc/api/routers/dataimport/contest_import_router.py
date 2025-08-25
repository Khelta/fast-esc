from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from fastesc.api.dependencies import get_repository, verify_api_key
from fastesc.api.models.data_import import DataImportContest
from fastesc.api.models.functions import add_id
from fastesc.api.models.models import CountryBase, CityBase, LocationBase, BroadcasterBase, ContestBase, PersonBase
from fastesc.database.models.models import Broadcaster as DB_Broadcaster, City as DB_City, Contest as DB_Contest, \
    Country as DB_Country, Location as DB_Location, Person as DB_Person, \
    Affiliation as DB_Affiliation
from fastesc.database.repositories.base_repo import DatabaseRepository

AffiliationRepository = Annotated[
    DatabaseRepository[DB_Affiliation],
    Depends(get_repository(DB_Affiliation))
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
PersonRepository = Annotated[
    DatabaseRepository[DB_Person],
    Depends(get_repository(DB_Person))
]

BroadcasterWithId = add_id(BroadcasterBase)
CityWithId = add_id(CityBase)
ContestWithId = add_id(ContestBase)
CountryWithId = add_id(CountryBase)
LocationWithId = add_id(LocationBase)
PersonWithId = add_id(PersonBase)

router = APIRouter(prefix="/data_import", tags=["import"])


@router.post("/contests/", response_model=list[DataImportContest])
async def import_contest_data(
        affiliation_repository: AffiliationRepository,
        broadcaster_repository: BroadcasterRepository,
        city_repository: CityRepository,
        contest_repository: ContestRepository,
        country_repository: CountryRepository,
        location_repository: LocationRepository,
        person_repository: PersonRepository,
        data: list[DataImportContest],
        token: str = Depends(verify_api_key),
):
    for contest_data in data:
        DataImportContest.model_validate(contest_data)

        db_country = await country_repository.get_by_dict({"name": contest_data.country}, lazy=True)
        if db_country is None:
            raise HTTPException(
                status_code=422,
                detail=f"Country '{contest_data.country}' not found in database.",
            )
        country = CountryWithId.model_validate(db_country)

        db_city: DB_City = await (
            city_repository.get_or_create({"name": contest_data.city, "country_id": country.id}, lazy=True))
        city = CityWithId.model_validate(db_city)

        db_location: DB_Location = await location_repository.get_or_create(
            {"name": contest_data.location, "city_id": city.id}, lazy=True)
        location = LocationWithId.model_validate(db_location)

        db_broadcaster: DB_Broadcaster = await broadcaster_repository.get_or_create(
            {"name": contest_data.broadcaster, "country_id": country.id}, lazy=True
        )
        broadcaster = BroadcasterWithId.model_validate(db_broadcaster)

        db_contest = await contest_repository.get_or_create(
            {
                "date": datetime.strptime(contest_data.date, "%d.%m.%Y").date(),
                "final": contest_data.final,
                "location_id": location.id,
                "broadcaster_id": broadcaster.id
            }, lazy=True
        )
        contest = ContestWithId.model_validate(db_contest)

        if contest_data.hosts:
            for host_name in contest_data.hosts:
                db_person = await person_repository.get_or_create({"name": host_name}, lazy=True)
                person = PersonWithId.model_validate(db_person)

                await affiliation_repository.get_or_create({"role": "HOST",
                                                            "person_id": person.id,
                                                            "contest_id": contest.id}, lazy=True)

    return data
