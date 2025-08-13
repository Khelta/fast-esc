import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

base_dir = os.path.dirname(__file__)
env_paths = [
    os.path.join("/etc/secrets", ".env"),
    os.path.join(base_dir, "../.env"),
]

env_path = next((path for path in env_paths if os.path.exists(path)), None)

if env_path:
    load_dotenv(dotenv_path=env_path, override=True)  # Override allows overriding existing env vars
    print(f"Loaded .env from {env_path}")

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(DATABASE_USERNAME,
                                                            DATABASE_PASSWORD,
                                                            DATABASE_HOST,
                                                            DATABASE_PORT,
                                                            DATABASE_NAME)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(DATABASE_URL)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
