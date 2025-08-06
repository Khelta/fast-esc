from sqlmodel import Session, select

from src.models.broadcaster import Broadcaster, BroadcasterWithId


def get_or_create_broadcaster(session: Session, input_data: Broadcaster):
    if input_data.id:
        instance = session.get(Broadcaster, input_data.id)
    else:
        instance = session.exec(
            select(Broadcaster).where(
                Broadcaster.name == input_data.name,
                Broadcaster.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = Broadcaster(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return BroadcasterWithId(**instance.model_dump())
