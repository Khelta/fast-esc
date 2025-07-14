from sqlmodel import Field, Session, SQLModel, select


class SongBase(SQLModel):
    title: str = Field(index=True)

    artist_id: int = Field(foreign_key="artist.id")
    country_id: int = Field(foreign_key="country.id")


class Song(SongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SongWithId(SongBase):
    id: int


class SongPublic(SongBase):
    id: int


def get_or_create_song(session: Session, input_data: Song):
    if input_data.id:
        instance = session.get(Song, input_data.id)
    else:
        instance = session.exec(
            select(Song).where(
                Song.title == input_data.title
                and Song.artist_id == input_data.artist_id
                and Song.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = Song(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return SongWithId(**instance.model_dump())
