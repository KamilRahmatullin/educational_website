from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    users: str = '/users'


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        env_nested_delimiter='__',  # in .env for example EDUCATION_SITE__DB__URL=
        env_prefix='EDUCATION_SITE__',
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
