import os

from dotenv import load_dotenv
from fastapi.security import APIKeyHeader

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

TEST_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(DATABASE_USERNAME,
                                                                 DATABASE_PASSWORD,
                                                                 DATABASE_HOST,
                                                                 DATABASE_PORT,
                                                                 "test")

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
