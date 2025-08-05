from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, Session, SQLModel, select

from src.models.artist_affiliation import ArtistAffiliationPublic

if TYPE_CHECKING:
    from src.models.artist_affiliation import ArtistAffiliation


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


def get_or_create_person(session: Session, input_data: Person):
    if input_data.id:
        instance = session.get(Person, input_data.id)
    else:
        instance = session.exec(
            select(Person).where(Person.name == input_data.name)
        ).first()

    if not instance:
        instance = Person(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return PersonWithId(**instance.model_dump())
