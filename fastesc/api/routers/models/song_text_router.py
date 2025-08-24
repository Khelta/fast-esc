from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from fastesc.api.dependencies import get_repository
from fastesc.api.models.models import SongPublic, SongTextPublic
from fastesc.database.models.models import Song as DB_Song
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/songtext", tags=["song_text"])

SongRepository = Annotated[
    DatabaseRepository[DB_Song],
    Depends(get_repository(DB_Song))
]


@router.get("", response_model=SongTextPublic)
async def find_in_songtext(repository: SongRepository,
                           text: str,
                           case_sensitive: bool = False,
                           whole_word: bool = True,
                           offset: int = Query(0, ge=0),
                           limit: Optional[int] = Query(0, ge=0)) -> SongTextPublic:
    songs = await repository.get_text_in_column("text",
                                                text,
                                                case_sensitive=case_sensitive,
                                                whole_word=whole_word,
                                                offset=offset,
                                                limit=limit)

    result = {
        "size": len(songs),
        "songs": [SongPublic.model_validate(song) for song in songs]
    }

    return SongTextPublic.model_validate(result)
