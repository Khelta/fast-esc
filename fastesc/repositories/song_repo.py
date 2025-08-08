from sqlmodel import Session, select

from fastesc.models.song import Song, SongWithId


def get_or_create_song(session: Session, input_data: Song):
    if input_data.id:
        instance = session.get(Song, input_data.id)
    else:
        instance = session.exec(
            select(Song).where(
                Song.title == input_data.title,
                Song.artist_id == input_data.artist_id,
                Song.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = Song(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return SongWithId(**instance.model_dump())
