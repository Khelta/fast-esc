from sqlmodel import Field, Session, SQLModel, select


class ParticipationBase(SQLModel):
    song_id: int = Field(foreign_key="song.id", index=True)
    contest_id: int = Field(foreign_key="contest.id", index=True)

    place: int | None = Field(default=None, index=True)
    run_order: int | None = Field(default=None, index=True)

    points: int | None = Field(default=None)
    jury_points: int | None = Field(default=None)
    public_points: int | None = Field(default=None)


class Participation(ParticipationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ParticipationWithId(ParticipationBase):
    id: int


class ParticipationPublic(ParticipationBase):
    id: int


def get_or_create_participation(session: Session, input_data: Participation):
    if input_data.id:
        instance = session.get(Participation, input_data.id)
    else:
        instance = session.exec(
            select(Participation).where(
                Participation.song_id == input_data.song_id
                and Participation.contest_id == input_data.contest_id
            )
        ).first()

    if not instance:
        instance = Participation(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ParticipationWithId(**instance.model_dump())
