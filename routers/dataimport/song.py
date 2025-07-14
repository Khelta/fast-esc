from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.artist import Artist, get_or_create_artist
from models.artist_affiliation import (
    ArtistAffiliation,
    get_or_create_artist_affiliation,
)
from models.contest import get_contest_by_year_and_final
from models.country import Country
from models.data_import import DataImportSong
from models.participation import Participation, get_or_create_participation
from models.person import Person, get_or_create_person
from models.song import Song, get_or_create_song

router = APIRouter(prefix="/data_import")


@router.post("/songs/", response_model=list[DataImportSong])
def import_song_data(
    *, session: Session = Depends(get_session), data: dict[str, list[DataImportSong]]
):
    for year in data:
        for song in data[year]:
            DataImportSong.model_validate(song)

            db_country = session.exec(
                select(Country).where(
                    Country.alpha2 == song.country[:2]
                    if len(song.country) <= 3
                    else Country.name == song.country
                )
            ).first()
            if db_country is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"Country '{song.country}' not found in database.",
                )
            # Just for type checking
            elif db_country.id is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Country '{song.country}' has no id in database.",
                )

            db_artist = get_or_create_artist(session, Artist(name=song.artist))

            db_song = get_or_create_song(
                session,
                Song(
                    title=song.title, country_id=db_country.id, artist_id=db_artist.id
                ),
            )

            try:
                y = int(year)
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail=f"Year '{year}' is not an acceptable year.",
                )
            print("HELLO", y)
            db_contest = get_contest_by_year_and_final(session, y, song.final)
            if db_contest is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Contest from '{year}' with final '{song.final}' not found in database.",
                )

            get_or_create_participation(
                session,
                Participation(
                    song_id=db_song.id,
                    contest_id=db_contest.id,
                    place=song.place,
                    run_order=song.running,
                    points=song.points,
                    jury_points=song.jury_points,
                    public_points=song.public_points,
                ),
            )

            if song.people:
                for people_category in song.people:
                    if people_category == "ARTIST":
                        pass
                    else:
                        for person in song.people[people_category]:
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

    return data
