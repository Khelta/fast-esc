from sqlmodel import Field, SQLModel


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
