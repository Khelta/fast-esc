from sqlmodel import Field, SQLModel

class CountryBase(SQLModel):
    name: str = Field(index=True)
    alpha2: str = Field(index=True, max_length=2)


class Country(CountryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CountryPublic(CountryBase):
    id: int


class CountryWithId(CountryBase):
    id: int
