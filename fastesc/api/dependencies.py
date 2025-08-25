from collections.abc import Callable

from fastapi import Depends, Security, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastesc.configuration import api_key_header, API_KEY
from fastesc.database.models.base import Base
from fastesc.database.repositories.base_repo import DatabaseRepository
from fastesc.db import get_db_session


def get_repository(
        model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)

    return func


def verify_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = api_key_header.removeprefix("Bearer ").strip()
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
