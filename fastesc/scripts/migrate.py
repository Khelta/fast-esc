import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from fastesc.database.models.base import Base
from fastesc.db import DATABASE_URL

logger = logging.getLogger()


async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    # To ensure all models are registered, import them here

    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
