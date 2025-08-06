from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.database import get_session
from src.models.broadcaster import Broadcaster
from src.models.city import City
from src.models.contest import Contest
from src.models.data_import import DataImportContest
from src.models.host import Host
from src.models.location import Location
from src.models.person import Person
from src.repositories.broadcaster_repo import get_or_create_broadcaster
from src.repositories.city_repo import get_or_create_city
from src.repositories.contest_repo import get_or_create_contest
from src.repositories.country_repo import get_country_by_county_name
from src.repositories.host_repo import get_or_create_host
from src.repositories.location_repo import get_or_create_location
from src.repositories.person_repo import get_or_create_person

router = APIRouter(prefix="/data_import", tags=["import"])


@router.post("/contests/", response_model=list[DataImportContest])
def import_contest_data(
        *, session: Session = Depends(get_session), data: list[DataImportContest]
):
    for contest in data:
        DataImportContest.model_validate(contest)

        db_country = get_country_by_county_name(session, contest.country)
        if db_country is None:
            raise HTTPException(
                status_code=422,
                detail=f"Country '{contest.country}' not found in database.",
            )

        db_city = get_or_create_city(
            session, City(country_id=db_country.id, name=contest.city)
        )

        db_location = get_or_create_location(
            session, Location(name=contest.location, city_id=db_city.id)
        )

        db_broadcaster = get_or_create_broadcaster(
            session, Broadcaster(name=contest.broadcaster, country_id=db_country.id)
        )

        db_contest = get_or_create_contest(
            session,
            Contest(
                date=datetime.strptime(contest.date, "%d.%m.%Y").date(),
                final=contest.final,
                location_id=db_location.id,
                broadcaster_id=db_broadcaster.id,
            ),
        )

        if contest.hosts:
            for host_name in contest.hosts:
                db_person = get_or_create_person(session, Person(name=host_name))

                get_or_create_host(
                    session, Host(person_id=db_person.id, contest_id=db_contest.id)
                )

    return data
