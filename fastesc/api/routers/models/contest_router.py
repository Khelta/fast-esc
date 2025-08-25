from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract

from fastesc.api.dependencies import get_repository
from fastesc.api.models.errors import ErrorResponse
from fastesc.api.models.models import ContestPublic
from fastesc.database.models.models import Contest
from fastesc.database.models.models import Contest as DB_Contest
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/contests", tags=["contests"])

ContestRepository = Annotated[
    DatabaseRepository[Contest],
    Depends(get_repository(Contest))
]


@router.get("", response_model=list[ContestPublic])
async def get_contests(repository: ContestRepository, offset: int = 0, limit: int = 1):
    contests = await repository.filter(offset=offset, limit=limit)
    return [ContestPublic.model_validate(contest) for contest in contests]


@router.get("/{id}",
            response_model=ContestPublic,
            responses={
                404: {
                    "model": ErrorResponse,
                    "description": "Contest not found",
                    "content": {
                        "application/json": {
                            "example": {"detail": "Contest with id '123' not found."}
                        }
                    },
                }
            },
            )
async def get_contest_by_id(repository: ContestRepository, id: int):
    contest = await repository.get(id)
    if contest:
        return ContestPublic.model_validate(contest)
    raise HTTPException(status_code=404, detail=f"Contest with id '{id}' not found.")


@router.get("/by_year/{year}/{final}",
            response_model=ContestPublic,
            responses={
                404: {
                    "model": ErrorResponse,
                    "description": "Contest not found",
                    "content": {
                        "application/json": {
                            "example": {"detail": "Contest of year '2154' with final '0' not found."}
                        }
                    },
                }
            },
            )
async def get_contest_by_year(repository: ContestRepository, year: int, final: int):
    # TODO Remove sqlalchemy dependency
    contest = await repository.filter(DB_Contest.final == final, extract('year', DB_Contest.date) == year)
    if len(contest) == 1:
        return ContestPublic.model_validate(contest[0])
    raise HTTPException(status_code=404, detail=f"Contest of year '{year}' with final '{final}' not found.")
