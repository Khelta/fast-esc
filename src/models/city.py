from sqlmodel import Field, SQLModel


class CityBase(SQLModel):
    name: str = Field(index=True)
    country_id: int = Field(foreign_key="country.id")


class City(CityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CityWithId(CityBase):
    id: int


class CityPublic(CityBase):
    id: int
