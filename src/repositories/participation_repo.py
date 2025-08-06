from sqlmodel import Session, select

from src.models.participation import Participation, ParticipationWithId


def get_or_create_participation(session: Session, input_data: Participation):
    if input_data.id:
        instance = session.get(Participation, input_data.id)
    else:
        instance = session.exec(
            select(Participation).where(Participation.song_id == input_data.song_id,
                                        Participation.contest_id == input_data.contest_id)
        ).first()

    if not instance:
        instance = Participation(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ParticipationWithId(**instance.model_dump())
