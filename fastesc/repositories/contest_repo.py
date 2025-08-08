from sqlmodel import Session, select, func

from fastesc.api.models import Contest, ContestWithId


def get_or_create_contest(session: Session, input_data: Contest) -> ContestWithId:
    if input_data.id:
        instance = session.get(Contest, input_data.id)
    else:
        instance = session.exec(
            select(Contest).where(
                Contest.date == input_data.date and Contest.final == input_data.final
            )
        ).first()

    if not instance:
        instance = Contest(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ContestWithId(**instance.model_dump())


def get_contest_by_year_and_final(session: Session, year: int, final: int) -> ContestWithId | None:
    instance = session.exec(
        select(Contest).where(
            func.extract("year", Contest.date) == year, Contest.final == final
        )
    ).first()
    if instance is not None:
        return ContestWithId(**instance.model_dump())
    else:
        raise LookupError("No contest for the given year and final number.")
