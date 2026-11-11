from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import charity_project_crud, donation_crud


def close_if_fully_invested(obj) -> None:
    """Закрывает объект, если он полностью инвестирован.

    Устанавливает флаг `fully_invested` и дату закрытия,
    если внесённая сумма равна требуемой.
    """
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def close_project_if_needed(project, session: AsyncSession) -> None:
    """Закрывает проект, если после обновления он полностью инвестирован.

    Вызывает `close_if_fully_invested`, сохраняет изменения
    и обновляет состояние объекта из базы данных.
    """
    if (
        project.full_amount == project.invested_amount
        and not project.fully_invested
    ):
        close_if_fully_invested(project)
        await session.commit()
        await session.refresh(project)


async def check_invested_funds(session: AsyncSession) -> None:
    """Распределяет нераспределённые пожертвования по открытым проектам.

    Проходит по всем открытым проектам и незакрытым пожертвованиям,
    переносит средства и закрывает полностью инвестированные объекты.
    После распределения фиксирует изменения в базе данных.
    """
    projects = await charity_project_crud.get_open(session)
    donations = await donation_crud.get_open(session)

    for project in projects:
        for donation in donations:
            project_remaining = project.full_amount - project.invested_amount
            donation_remaining = (
                donation.full_amount - donation.invested_amount
            )

            if project_remaining <= 0:
                break
            if donation_remaining <= 0:
                continue

            amount = min(project_remaining, donation_remaining)
            project.invested_amount += amount
            donation.invested_amount += amount

            close_if_fully_invested(project)
            close_if_fully_invested(donation)

    await session.commit()
