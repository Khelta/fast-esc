from datetime import date as dateclass

from sqlmodel import Field, SQLModel


class ContestBase(SQLModel):
    date: dateclass = Field(index=True)
    final: int = Field(ge=0, le=2)

    location_id: int = Field(foreign_key="location.id")
    broadcaster_id: int = Field(foreign_key="broadcaster.id")


class Contest(ContestBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ContestWithId(ContestBase):
    id: int


class ContestPublic(ContestBase):
    id: int
