from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Сервис поможет забронировать переговорку'

    class Config:
        env_file: str = '.env'


settings = Settings()
