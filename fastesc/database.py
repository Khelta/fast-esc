import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel

env_paths = [
    os.path.join("/etc/secrets", ".env"),
    os.path.join(os.getcwd(), ".env"),
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

DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(DATABASE_USERNAME,
                                                    DATABASE_PASSWORD,
                                                    DATABASE_HOST,
                                                    DATABASE_PORT,
                                                    DATABASE_NAME)

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
