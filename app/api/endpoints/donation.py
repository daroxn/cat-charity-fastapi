from typing import Annotated, List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.repositories import donation_crud
from app.schemas import (
    DonationCreate, DonationDB, DonationFullInfoDB
)
from app.services import check_invested_funds

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=List[DonationFullInfoDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
    dependencies=[Depends(current_superuser)],
    summary='Получить список всех пожертвований',
)
async def get_all_donations(
    session: SessionDep
):
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={'user_id'},
    dependencies=[Depends(current_user)],
    summary='Получить список пожертвований текущего пользователя',
)
async def get_my_reservations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    return await donation_crud.get_by_user(session, user)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    summary='Создать новое пожертвование',
)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep
):
    donation = await donation_crud.create(donation, session)

    await check_invested_funds(session)

    await session.refresh(donation)
    return donation
