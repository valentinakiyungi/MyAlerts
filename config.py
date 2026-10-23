from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CREDENTIALS_PATH: str = "credentials.json"
    TOKEN_PATH: str = "token.json"
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
