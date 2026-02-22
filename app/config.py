from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Business Plan Pipeline"
    API_V1_STR: str = ""
    
    # Database
    # Use the Connection String from Supabase (Settings -> Database -> Connection String)
    DATABASE_URL: str

    # App Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Config
    GEMINI_API_KEY: str | None = None
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]

    # Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "Business Plan Pipeline"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    def get_database_url(self) -> str:
        return self.DATABASE_URL

settings = Settings()
