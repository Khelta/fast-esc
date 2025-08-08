from sqlmodel import Session, select

from fastesc.models.host import Host, HostWithId


def get_or_create_host(session: Session, input_data: Host):
    if input_data.id:
        instance = session.get(Host, input_data.id)
    else:
        instance = session.exec(
            select(Host).where(
                Host.contest_id == input_data.contest_id,
                Host.person_id == input_data.person_id
            )
        ).first()

    if not instance:
        instance = Host(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return HostWithId(**instance.model_dump())
