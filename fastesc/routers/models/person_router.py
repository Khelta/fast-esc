from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from fastesc.database import get_session
from fastesc.models.person import (
    Person,
    PersonCreate,
    PersonPublic,
    PersonPublicWithAffiliations,
)

router = APIRouter(prefix="/people", tags=["people"])


@router.get(
    "/",
    response_model=list[PersonPublic],
    description="Gets all people from the database.",
)
def get_people(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    people = session.exec(select(Person).offset(offset).limit(limit)).all()
    return people


@router.get(
    "/{person_id}",
    response_model=PersonPublicWithAffiliations,
    description="Gets a specific person given the id from the database.",
)
def get_person(*, session: Session = Depends(get_session), person_id: int):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.post("/", response_model=PersonPublic)
def get_or_create_person(
        *, session: Session = Depends(get_session), person: PersonCreate
):
    # Check if the person already exists
    existing_person = session.exec(
        select(Person).where(Person.name == person.name)
    ).first()
    if existing_person:
        return existing_person

    # If not, create a new person
    db_person = Person.model_validate(person)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person
