from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, HTTPException

from fastesc.api.dependencies import get_repository
from fastesc.api.models.errors import ErrorResponse
from fastesc.api.models.models import SongTextPublic, SongWordCountPublic, SongPublic
from fastesc.api.routers.helper import count_words
from fastesc.database.models.models import Song as DB_Song
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/songtext", tags=["song_text"])

SongRepository = Annotated[
    DatabaseRepository[DB_Song],
    Depends(get_repository(DB_Song))
]


@router.get("/find",
            response_model=SongTextPublic,
            responses={
                400: {
                    "model": ErrorResponse,
                    "description": "Text cannot be empty",
                    "content": {
                        "application/json": {
                            "example": {"detail": "Text cannot be empty"}
                        }
                    },
                }
            }, )
async def find_in_songtext(repository: SongRepository,
                           text: str,
                           case_sensitive: bool = False,
                           whole_word: bool = True,
                           offset: int = Query(0, ge=0),
                           limit: Optional[int] = Query(0, ge=0)) -> SongTextPublic:
    if text == "":
        raise HTTPException(status_code=400, detail=f"Text cannot be empty")

    songs = await repository.get_text_in_column("text",
                                                text,
                                                case_sensitive=case_sensitive,
                                                whole_word=whole_word,
                                                offset=offset,
                                                limit=limit)

    if not case_sensitive:
        text = text.lower()

    song_texts = [song.text for song in songs]
    word_counts = [count_words(text, song_text, case_sensitive, whole_word) for song_text in song_texts]

    songs = [{**(SongPublic.model_validate(song).model_dump()), "word_count": word_counts[index]} for index, song in
             enumerate(songs)]

    result = {
        "size": len(songs),
        "word_count": sum(word_counts),
        "songs": [SongWordCountPublic.model_validate(song) for song in songs]
    }

    return SongTextPublic.model_validate(result)


@router.get("",
            response_model=list[SongPublic],
            )
async def all_songs(repository: SongRepository,
                    offset: int = Query(0, ge=0),
                    limit: Optional[int] = Query(0, ge=0)) -> list[SongPublic]:
    songs = await repository.filter(offset=offset, limit=limit)
    return [SongPublic.model_validate(song) for song in songs]
