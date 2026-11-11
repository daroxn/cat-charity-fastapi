from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_project_name_exists(
    project_name: str,
    session: AsyncSession
) -> None:
    """Проверяет, что проект с таким именем ещё не существует.

    Вызывает HTTP 400, если имя уже занято.
    """
    project = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_is_closed(
    project_id: int,
    session: AsyncSession
) -> None:
    """Проверяет, что проект ещё не закрыт.

    Вызывает HTTP 400, если проект уже полностью инвестирован.
    """
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект уже закрыт.'
        )


def check_full_amount(
    project: CharityProject,
    obj_in: CharityProjectUpdate
) -> None:
    """Проверяет, что новая требуемая сумма не меньше уже вложенной.

    Вызывает HTTP 400, если `full_amount` меньше `invested_amount`.
    """
    if (
        obj_in.full_amount is not None
        and obj_in.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )


async def check_invested_funds_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверяет, что в проект ещё не были внесены средства.

    Возвращает проект, если средства не вносились.
    Вызывает HTTP 400, если `invested_amount > 0`.
    """
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверяет, что проект с указанным ID существует.

    Возвращает объект проекта или вызывает HTTP 404.
    """
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не существует.'
        )
    return project
