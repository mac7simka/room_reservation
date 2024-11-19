from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Сервис поможет забронировать переговорку'
    secret: str = 'SECRET'
    database_url: str
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file: str = '.env'


settings = Settings()
