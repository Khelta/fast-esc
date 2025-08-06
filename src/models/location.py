from sqlmodel import Field, SQLModel


class LocationBase(SQLModel):
    name: str = Field(unique=True, index=True)

    city_id: int = Field(foreign_key="city.id")


class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class LocationWithId(LocationBase):
    id: int


class LocationPublic(LocationBase):
    id: int
