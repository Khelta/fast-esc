from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.person import Person


class ArtistAffiliationBase(SQLModel):
    role: str = Field(index=True)

    person_id: int = Field(foreign_key="person.id")
    artist_id: int = Field(foreign_key="artist.id")
    contest_id: int = Field(foreign_key="contest.id")


class ArtistAffiliation(ArtistAffiliationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    person: Optional["Person"] = Relationship(back_populates="affiliations")


class ArtistAffiliationWithId(ArtistAffiliationBase):
    id: int


class ArtistAffiliationPublic(ArtistAffiliationBase):
    id: int
