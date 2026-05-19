from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pocketbase_url: str
    visa_service_url: str
    mastercard_service_url: str
    nu_service_url: str
    nu_service_token: int
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)


settings = Settings()
