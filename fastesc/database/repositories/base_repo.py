from typing import Generic, TypeVar, Any

from sqlalchemy import BinaryExpression, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload

from fastesc.database.models.base import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def add_lazy(self, query: Select[tuple[Any]]):
        relationships = [getattr(self.model, name) for name in dir(self.model)
                         if hasattr(getattr(self.model, name), 'property')
                         and hasattr(getattr(getattr(self.model, name), 'property'), "direction")]
        for relationship in relationships:
            query = query.options(lazyload(relationship))
        return query

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, id: int) -> Model | None:
        return await self.session.get(self.model, id)

    async def get_or_create(self, data: dict, lazy: bool=False) -> Model:
        query = select(self.model).filter_by(**data)

        if lazy:
            query = self.add_lazy(query)

        instance = await self.session.scalar(query)
        if instance:
            return instance
        else:
            return await self.create(data)

    async def get_by_dict(self, data: dict, lazy: bool=False) -> Model | None:
        query = select(self.model).filter_by(**data)

        if lazy:
            query = self.add_lazy(query)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def filter(
            self,
            *expressions: BinaryExpression,
            offset: int = 0,
            limit: int = None,
            lazy: bool=False

    ) -> list[Model]:
        query = select(self.model)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if expressions:
            query = query.where(*expressions)
        if lazy:
            query = self.add_lazy(query)
        return list(await self.session.scalars(query))
