from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, select

if TYPE_CHECKING:
    from models.person import Person


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


def get_or_create_artist_affiliation(session: Session, input_data: ArtistAffiliation):
    if input_data.id:
        instance = session.get(ArtistAffiliation, input_data.id)
    else:
        instance = session.exec(
            select(ArtistAffiliation).where(
                ArtistAffiliation.person_id == input_data.person_id
                and ArtistAffiliation.artist_id == input_data.artist_id
                and ArtistAffiliation.contest_id == input_data.contest_id
            )
        ).first()

    if not instance:
        instance = ArtistAffiliation(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ArtistAffiliationWithId(**instance.model_dump())
