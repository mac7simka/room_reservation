from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections
)
from app.core.db import get_async_session
from app.models.reservation import Reservation
from app.schemas.reservation import (
    ReservationCreate, ReservationDB, ReservationUpdate
)
from app.crud.reservation import reservation_crud
from app.core.user import current_superuser, current_user
from app.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        **reservation.dict(), session=session
    )
    reservation = await reservation_crud.create(reservation, session, user)
    return reservation


@router.get(
        '/',
        response_model=list[ReservationDB],
        dependencies=[Depends(current_superuser)],
    )
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session),
) -> list[Reservation]:
    """Только для суперюзеров."""
    all_reservation = await reservation_crud.get_multi(session)
    return all_reservation


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для суперюзеров или создателей объекта бронирования."""
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Для суперюзеров или создателей объекта бронирования."""
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.dict(),
        # id обновляемого объекта бронирования,
        reservation_id=reservation_id,
        # id переговорки.
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаем объект класса ReservationUpdate, как и треб..
        obj_in=obj_in,
        session=session,
    )
    return reservation


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
        user: User = Depends(current_user)
):
    # Сразу можно добавить докстринг для большей информативности.
    """Получает список всех бронирований для текущего пользователя."""
    # Вызываем созданный метод.
    reservations = await reservation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
