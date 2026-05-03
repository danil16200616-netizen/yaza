from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

    @property
    def db_url(self) -> str:
        # Railway выдаёт postgres://, SQLAlchemy требует postgresql://
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
