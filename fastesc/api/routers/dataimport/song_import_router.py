from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract

from fastesc.api.dependencies import get_repository
from fastesc.api.models.data_import import DataImportSong
from fastesc.api.models.functions import add_id
from fastesc.api.models.models import CountryBase, ArtistBase, SongBase, ContestBase, ParticipationBase, PersonBase, \
    AffiliationBase
from fastesc.database.models.models import Affiliation as DB_Affiliation, Artist as DB_Artist, Contest as DB_Contest, \
    Country as DB_Country, \
    Person as DB_Person, Participation as DB_Participation, Song as DB_Song
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/data_import", tags=["import"])

ArtistRepository = Annotated[
    DatabaseRepository[DB_Artist],
    Depends(get_repository(DB_Artist))
]
AffiliationRepository = Annotated[
    DatabaseRepository[DB_Affiliation],
    Depends(get_repository(DB_Affiliation))
]
ContestRepository = Annotated[
    DatabaseRepository[DB_Contest],
    Depends(get_repository(DB_Contest))
]

CountryRepository = Annotated[
    DatabaseRepository[DB_Country],
    Depends(get_repository(DB_Country))
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

AffiliationWithId = add_id(AffiliationBase)
ArtistWithId = add_id(ArtistBase)
ContestWithId = add_id(ContestBase)
CountryWithId = add_id(CountryBase)
ParticipationWithId = add_id(ParticipationBase)
PersonWithId = add_id(PersonBase)
SongWithId = add_id(SongBase)


@router.post("/songs/", response_model=list[DataImportSong])
async def import_song_data(
        affiliation_repository: AffiliationRepository,
        artist_repository: ArtistRepository,
        contest_repository: ContestRepository,
        country_repository: CountryRepository,
        participation_repository: ParticipationRepository,
        person_repository: PersonRepository,
        song_repository: SongRepository,
        data: list[DataImportSong]
):
    for entry in data:
        year = entry.year
        final = entry.final
        participations = entry.participations

        # TODO Remove sqlalchemy dependency
        db_contest: DB_Contest = await contest_repository.filter(
            DB_Contest.final == final, extract('year', DB_Contest.date) == year
        )
        if len(db_contest) != 1:
            raise HTTPException(
                status_code=404,
                detail=f"Contest from '{year}' with final '{final}' not found in database.",
            )
        contest = ContestWithId.model_validate(db_contest[0])

        for participation_data in participations:

            db_country = await country_repository.filter(DB_Country.alpha2 == participation_data.country[:2])
            if len(db_country) != 1:
                raise HTTPException(
                    status_code=422,
                    detail=f"Country '{participation_data.country}' not found in database.",
                )
            country = CountryWithId.model_validate(db_country[0])

            db_artist = await artist_repository.get_or_create({"name": participation_data.artist})
            artist = ArtistWithId.model_validate(db_artist)

            db_song = await song_repository.get_or_create(
                {"title": participation_data.title, "country_id": country.id, "artist_id": artist.id})
            song = SongWithId.model_validate(db_song)

            db_participation = await participation_repository.get_or_create(
                {"song_id": song.id, "contest_id": contest.id, "place": participation_data.place,
                 "running": participation_data.running,
                 "points": participation_data.points,
                 "jury_points": participation_data.jury_points,
                 "public_points": participation_data.public_points, })
            participation = ParticipationWithId.model_validate(db_participation)

            if participation_data.people:
                for people_category in participation_data.people:
                    for person_name in participation_data.people[people_category]:
                        db_person = await person_repository.get_or_create({"name": person_name})
                        person = PersonWithId.model_validate(db_person)

                        db_affiliation = await affiliation_repository.get_or_create({"person_id": person.id,
                                                                                     "artist_id": artist.id,
                                                                                     "contest_id": contest.id,
                                                                                     "role": people_category})
                        AffiliationWithId.model_validate(db_affiliation)

    return [d.model_dump() for d in data]
