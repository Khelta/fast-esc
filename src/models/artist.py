from sqlmodel import Field, SQLModel


class ArtistBase(SQLModel):
    name: str = Field(index=True)


class Artist(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ArtistWithId(ArtistBase):
    id: int


class ArtistPublic(ArtistBase):
    id: int
