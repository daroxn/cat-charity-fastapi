from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentMixin


class CharityProject(InvestmentMixin):
    """Модель благотворительного проекта."""

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
