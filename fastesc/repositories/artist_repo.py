from sqlmodel import Session, select

from fastesc.models.artist import Artist, ArtistWithId


def get_or_create_artist(session: Session, input_data: Artist):
    if input_data.id:
        instance = session.get(Artist, input_data.id)
    else:
        instance = session.exec(
            select(Artist).where(Artist.name == input_data.name)
        ).first()

    if not instance:
        instance = Artist(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ArtistWithId(**instance.model_dump())
