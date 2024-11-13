from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text

app = FastAPI()
Base = declarative_base()


class SecretMessage(BaseModel):
    # Опишите Pydantic-схему для зашифрованных сообщений.
    # Все поля - обязательные.
    title: str
    message: str


class ReadyNews(Base):
    # Опишите модель SQLAlchemy для хранения данных в БД.
    # Дополнительных классов создавать не нужно.
    # Таблицу назовите `news`, в ней должен быть столбец id.
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    message = Column(Text)


def decoder(data: dict[str, str]) -> dict[str, str]:
    """
    Сверхсекретный декодер.

    Здесь всё работает, ничего менять не надо!
    """
    decoded_data = {}
    for key, value in data.items():
        decoded_str = (chr(int(chunk)) for chunk in value.split('-'))
        decoded_data[key] = ''.join(decoded_str)
    return decoded_data


@app.post('/super-secret-base')
def reciever(encoded_news: SecretMessage):

    # Передайте сообщение в декодер.
    news: dict[str, str] = decoder(encoded_news.dict())

    # Создайте переменную ready_news - объект класса ReadyNews
    # из дешифрованного сообщения.
    ready_news = ReadyNews(**news)

    # Здесь мог бы быть код, сохраняющий сообщение в базу данных,
    # но его писать не надо.

    # Эндпоинт возвращает объект класса ReadyNews.
    # Здесь ничего менять не надо.
    return ready_news
