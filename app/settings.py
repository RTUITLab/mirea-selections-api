from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    postgres_url: str
    memcached_server: str
    
    api_prefix: str = ""

    jwt_issuer: str
    jwt_secret: str
    
    oauth2_authorization_url: str
    oauth2_access_token_url: str
    oauth2_user_details_url: str
    oauth2_student_details_url: str
    oauth2_employee_details_url: str
    oauth2_client_id: str
    oauth2_client_secret: str


settings = Settings()
