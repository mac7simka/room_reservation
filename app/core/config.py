from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Сервис поможет забронировать переговорку'
    database_url: str

    class Config:
        env_file: str = '.env'


settings = Settings()
