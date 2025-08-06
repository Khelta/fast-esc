from sqlmodel import Field, SQLModel


class BroadcasterBase(SQLModel):
    name: str = Field(index=True)

    country_id: int = Field(foreign_key="country.id")


class Broadcaster(BroadcasterBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BroadcasterWithId(BroadcasterBase):
    id: int


class BroadcasterPublic(BroadcasterBase):
    id: int
