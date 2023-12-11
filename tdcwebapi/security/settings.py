from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


_ROOT_FOLDER = Path(__file__).parent.parent


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_algorithms: str

    class Config:
        env_file = _ROOT_FOLDER.joinpath(".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
