from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.repositories.base import BaseRepository


class CharityProjectRepository(BaseRepository):
    """Репозиторий для работы с благотворительными проектами."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[str]:
        """Возвращает имя проекта по его названию или None, если не найден."""
        result = await session.execute(
            select(CharityProject.name).where(
                CharityProject.name == project_name
            )
        )
        return result.scalars().first()


charity_project_crud = CharityProjectRepository(CharityProject)
