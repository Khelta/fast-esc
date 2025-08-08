from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastesc.database.models.base import Base
from fastesc.database.repositories.base_repo import DatabaseRepository
from fastesc.db import get_db_session


def get_repository(
        model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)

    return func
