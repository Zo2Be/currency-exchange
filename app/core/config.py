from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 15
    payload: dict[str, str] = {}
    headers: dict[str, str] = {}
    sqlalchemy_database_url: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env")
