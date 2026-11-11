from typing import Annotated, List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.repositories import charity_project_crud
from app.schemas import (
    CharityProjectUpdate, CharityProjectDB, CharityProjectCreate
)
from app.api.validators import (
    check_project_name_exists, check_project_is_closed, check_project_exists,
    check_full_amount, check_invested_funds_exists
)
from app.services import (
    check_invested_funds, close_project_if_needed
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить список всех благотворительных проектов',
)
async def get_all_charity_projects(
    session: SessionDep
):
    """Только для суперюзеров."""
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создать новый благотворительный проект',
)
async def create_new_chariy_project(
    project: CharityProjectCreate,
    session: SessionDep
):
    """Только для суперюзеров."""
    await check_project_name_exists(project.name, session)
    new_project = await charity_project_crud.create(project, session)

    await check_invested_funds(session)

    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Обновить данные благотворительного проекта',
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    if project is not None:
        await check_project_is_closed(project_id, session)

    if obj_in.name is not None:
        await check_project_name_exists(obj_in.name, session)

    if obj_in.full_amount is not None:
        check_full_amount(project, obj_in)

    project = await charity_project_crud.update(
        project, obj_in, session
    )

    await close_project_if_needed(project, session)

    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Удалить благотворительный проект',
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    if project is not None:
        await check_invested_funds_exists(project_id, session)

    return await charity_project_crud.remove(project, session)
