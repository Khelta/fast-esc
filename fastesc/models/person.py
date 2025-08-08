from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from fastesc.models.artist_affiliation import ArtistAffiliationPublic

if TYPE_CHECKING:
    from fastesc.models.artist_affiliation import ArtistAffiliation


class PersonBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Person(PersonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    affiliations: list["ArtistAffiliation"] = Relationship(back_populates="person")


class PersonCreate(PersonBase):
    pass


class PersonWithId(PersonBase):
    id: int


class PersonPublic(PersonBase):
    id: int


class PersonPublicWithAffiliations(PersonPublic):
    affiliations: list[ArtistAffiliationPublic] = []
