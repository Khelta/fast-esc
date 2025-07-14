from sqlmodel import Field, Session, SQLModel, select


class ArtistBase(SQLModel):
    name: str = Field(index=True)


class Artist(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ArtistWithId(ArtistBase):
    id: int


class ArtistPublic(ArtistBase):
    id: int


def get_or_create_artist(session: Session, input_data: Artist):
    if input_data.id:
        instance = session.get(Artist, input_data.id)
    else:
        instance = session.exec(
            select(Artist).where(Artist.name == input_data.name)
        ).first()

    if not instance:
        instance = Artist(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ArtistWithId(**instance.model_dump())
