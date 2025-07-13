from datetime import date as dateClass

from sqlmodel import Field, Session, SQLModel, select


class ContestBase(SQLModel):
    date: dateClass = Field(index=True)
    final: int = Field()

    location_id: int = Field(foreign_key="location.id")
    broadcaster_id: int = Field(foreign_key="broadcaster.id")


class Contest(ContestBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ContestWithId(ContestBase):
    id: int


class ContestPublic(ContestBase):
    id: int


def get_or_create_contest(session: Session, input_data: Contest):
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
