from sqlmodel import Field, Session, SQLModel, select


class PersonBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Person(PersonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PersonWithId(PersonBase):
    id: int


class PersonPublic(PersonBase):
    id: int


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
