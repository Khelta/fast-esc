from sqlmodel import Session, select

from fastesc.api.models import Person, PersonWithId


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
