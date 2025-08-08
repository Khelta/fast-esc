from sqlmodel import Session, select

from fastesc.models.artist_affiliation import ArtistAffiliation, ArtistAffiliationWithId


def get_or_create_artist_affiliation(session: Session, input_data: ArtistAffiliation):
    if input_data.id:
        instance = session.get(ArtistAffiliation, input_data.id)
    else:
        instance = session.exec(
            select(ArtistAffiliation).where(
                ArtistAffiliation.person_id == input_data.person_id,
                ArtistAffiliation.artist_id == input_data.artist_id,
                ArtistAffiliation.contest_id == input_data.contest_id
            )
        ).first()

    if not instance:
        instance = ArtistAffiliation(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return ArtistAffiliationWithId(**instance.model_dump())
