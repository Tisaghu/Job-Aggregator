from pydantic import BaseSettings

class Settings(BaseSettings):
    adzuna_app_id: str
    adzuna_app_key: str

    class Config:
        env_file = ".env"

settings = Settings()
