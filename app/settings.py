from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    postgres_url: str
    jwt_secret: str
    api_prefix: str = ""


settings = Settings()
