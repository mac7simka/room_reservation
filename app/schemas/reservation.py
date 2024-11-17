from datetime import datetime

from pydantic import BaseModel, root_validator, validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: str):
        if value <= datetime.now():
            raise ValueError('Начало бронирования меньше текущего времени')
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):

        if values['to_reserve'] < values['from_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class MeetingRoomDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        orm_mode = True
