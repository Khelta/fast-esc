from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from fastesc.api.models import Artist
from fastesc.api.models import ArtistAffiliation
from fastesc.api.models import DataImportSong
from fastesc.api.models import Person
from fastesc.api.models import Song
from fastesc.api.models.participation import Participation
from fastesc.database import get_session
from fastesc.repositories.artist_affiliation_repo import get_or_create_artist_affiliation
from fastesc.repositories.artist_repo import get_or_create_artist
from fastesc.repositories.contest_repo import get_contest_by_year_and_final
from fastesc.repositories.country_repo import get_country_by_alpha2
from fastesc.repositories.participation_repo import get_or_create_participation
from fastesc.repositories.person_repo import get_or_create_person
from fastesc.repositories.song_repo import get_or_create_song

router = APIRouter(prefix="/data_import", tags=["import"])


@router.post("/songs/", response_model=list[DataImportSong])
def import_song_data(
        *, session: Session = Depends(get_session), data: list[DataImportSong]
):
    for entry in data:
        year = entry.year
        final = entry.final
        participations = entry.participations

        db_contest = get_contest_by_year_and_final(session, year, final)
        if db_contest is None:
            raise HTTPException(
                status_code=404,
                detail=f"Contest from '{year}' with final '{final}' not found in database.",
            )

        for participation in participations:

            db_country = get_country_by_alpha2(session, participation.country)
            if db_country is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"Country '{participation.country}' not found in database.",
                )
            # Just for type checking
            elif db_country.id is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Country '{participation.country}' has no id in database.",
                )

            db_artist = get_or_create_artist(session, Artist(name=participation.artist))

            db_song = get_or_create_song(
                session,
                Song(
                    title=participation.title, country_id=db_country.id, artist_id=db_artist.id
                ),
            )

            db_participation = get_or_create_participation(
                session,
                Participation(
                    song_id=db_song.id,
                    contest_id=db_contest.id,
                    place=participation.place,
                    running=participation.running,
                    points=participation.points,
                    jury_points=participation.jury_points,
                    public_points=participation.public_points,
                ),
            )

            if participation.people:
                for people_category in participation.people:
                    for person in participation.people[people_category]:
                        db_person = get_or_create_person(
                            session, Person(name=person)
                        )

                        get_or_create_artist_affiliation(
                            session,
                            ArtistAffiliation(
                                person_id=db_person.id,
                                artist_id=db_artist.id,
                                contest_id=db_contest.id,
                                role=people_category,
                            ),
                        )

    return [d.model_dump() for d in data]
