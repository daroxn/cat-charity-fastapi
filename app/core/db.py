from collections.abc import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy-моделей проекта."""


class CommonMixin:
    """Миксин с общими атрибутами для всех моделей.

    Автоматически задаёт имя таблицы по имени класса
    и добавляет первичный ключ `id`.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
