from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: str

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> list[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
